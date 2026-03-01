<?php

namespace DreamSoft\Controllers\Components;

use DreamSoft\Libs\DataUtils;
use DreamSoft\Libs\Debugger;
use DreamSoft\Models\PrintShopConfig\{
    PrintShopConfigEfficiency,
    PrintShopConfigEfficiencySideRelations,
    PrintShopConfigEfficiencySpeed,
    PrintShopConfigEfficiencySpeedChanges,
    PrintShopConfigOption,
    PrintShopConfigPrice
};
use DreamSoft\Models\ProductionPath\{
    Device,
    DevicePrice,
    DeviceSideRelations,
    DeviceSpeed,
    DeviceSpeedChange,
    OptionControllerOperationDevice
};
use DreamSoft\Libs\Singleton;
use Exception;

class CalculatorDevices extends Singleton
{
    protected $PrintShopConfigPrice;
    protected $PrintShopConfigOption;
    private $OptionControllerOperationDevice;
    private $Device;
    private $DeviceSpeed;
    private $DeviceSpeedChange;
    private $DeviceSideRelations;
    private $DevicePrice;
    private $PrintShopConfigEfficiency;
    private $PrintShopConfigEfficiencySpeed;
    private $PrintShopConfigEfficiencySpeedChanges;
    private $PrintShopConfigEfficiencySideRelations;

    protected function __construct()
    {
        parent::__construct();
        $this->Device = Device::getInstance();
        $this->DevicePrice = DevicePrice::getInstance();
        $this->DeviceSpeed = DeviceSpeed::getInstance();
        $this->DeviceSpeedChange = DeviceSpeedChange::getInstance();
        $this->PrintShopConfigEfficiency = PrintShopConfigEfficiency::getInstance();
        $this->PrintShopConfigEfficiencySpeed = PrintShopConfigEfficiencySpeed::getInstance();
        $this->PrintShopConfigEfficiencySpeedChanges = PrintShopConfigEfficiencySpeedChanges::getInstance();
        $this->PrintShopConfigEfficiencySideRelations = PrintShopConfigEfficiencySideRelations::getInstance();
        $this->DeviceSideRelations = DeviceSideRelations::getInstance();
        $this->OptionControllerOperationDevice = OptionControllerOperationDevice::getInstance();
        $this->PrintShopConfigPrice = PrintShopConfigPrice::getInstance();
        $this->PrintShopConfigOption = PrintShopConfigOption::getInstance();
    }

    public function calculateDeviceDetails($attrID, $optID, $controllerID, $sheets, $area, $length, $count, $projectSheets, $fullProjectsSheets, $sheetCuts, $sheetsAfterCut, $totalSheetFolds, $thickness, $stiffness, $grammage, $formatWidth, $formatHeight, $pages, $totalWeight, $workspace, &$finalPriceText, $devicesArray = null)
    {
        $finalPriceText['calculateDeviceDetails'][] = "calculateDeviceDetails($attrID, $optID, $controllerID, sheets=$sheets, area=$area, length=$length, count=$count, projectSheets=$projectSheets, fullProjectsSheets=$fullProjectsSheets, sheetCuts=$sheetCuts, sheetsAfterCut=$sheetsAfterCut, totalSheetFolds=$totalSheetFolds, thickness=$thickness, stiffness=$stiffness, grammage=$grammage, formatWidth=$formatWidth, formatHeight=$formatHeight)";
        $totalPrice = $totalExpense = $totalTime = 0;
        $workUnits = [];
        $devices = [];
        $devicesIds = $devicesArray ?? array_column($this->OptionControllerOperationDevice->getByOptionController($optID, $controllerID), 'deviceID');

        $option = $this->PrintShopConfigOption->customGet($optID);
        $repeatedOperationsCount = $option['repeatedOperationsCount'];

        if (empty($devicesIds)) {
            Debugger::getInstance()->addWarning("Declared man hours use but no device found attrID=$attrID, optID=$optID, controllerID=$controllerID");
        }

        foreach ($devicesIds as $deviceID) {
            $deviceInfo = $this->getDeviceInfo($deviceID, $attrID, $optID, $controllerID);
            if (!$deviceInfo['workUnit']) {
                continue;
            }
            $finalPriceText['deviceID'][] = $deviceID;
            $finalPriceText['workUnit'][] = $deviceInfo['workUnit'];
            $devices[] = ['ID' => $deviceID, 'name' => $deviceInfo['name']];
            $workUnits[] = $deviceInfo['workUnit'];

            $calculationUnit = $this->getCalculationUnit($deviceInfo['workUnit'], $sheets, $area, $length, $count, $projectSheets, $sheetsAfterCut, $totalWeight, $workspace);

            $deviceSpeed = $this->getSpeedForVolume($deviceID, $calculationUnit, $attrID, $optID, $controllerID);
            $finalPriceText['deviceSpeed'][] = $deviceSpeed;
            $deviceSpeed *= $this->getSpeedChange($grammage, $thickness, $stiffness, $totalSheetFolds, $projectSheets, $sheetCuts, $deviceID, $optID, $attrID, $controllerID);
            $finalPriceText['speedChange'][] = $this->getSpeedChangePercent($deviceSpeed);

            $deviceSpeed *= $this->getSpeedChangeByRelation($formatWidth, $formatHeight, $deviceID, $optID, $attrID, $controllerID);
            $finalPriceText['speedChangeByRelation'][] = $this->getSpeedChangePercent($deviceSpeed);

            $workingHourPrice = $this->DevicePrice->getPriceForAmount($deviceID, $calculationUnit) * 100;
            $operationTime = $this->calculateOperationTime($deviceInfo, $calculationUnit, $thickness);
            $finalPriceText['operationTime'][] = "{$operationTime} min";

            $workTime = $this->calculateWorkTime($deviceInfo['workUnit'], $operationTime, $calculationUnit, $deviceSpeed, $repeatedOperationsCount, $projectSheets);
            $totalPrice += $workTime / 3600 * $workingHourPrice;
            $totalTime += $workTime;

            $expense = $this->DevicePrice->getExpenseForAmount($deviceID, $calculationUnit) * 100;
            $totalExpense += $this->calculateTotalExpense($expense, $calculationUnit, $deviceSpeed, $operationTime, $repeatedOperationsCount);
        }
        return ['devicePrice' => $totalPrice, 'deviceExpense' => $totalExpense, 'deviceTime' => $totalTime, 'workUnits' => $workUnits, 'devices' => $devices];
    }

    private function getCalculationUnit($workUnit, $sheets, $area, $length, $count, $projectSheets, $sheetsAfterCut, $totalWeight, $workspace)
    {
        switch ($workUnit) {
            case 'sheet':
                return $sheets;
            case 'squareMeter':
                return $area;
            case 'squareMetersForPages':
                return $area * $pages;
            case 'perimeter':
                return $length;
            case 'set':
                return $count;
            case 'projectSheets':
                return $projectSheets;
            case 'every_sheet_separate':
                return $sheets;
            case 'folds':
            case 'collectingFolds':
                return $sheetCuts ? $sheetsAfterCut : $sheets;
            case 'weight':
                return $totalWeight * $count;
            case 'packageWeight':
                $prices = $this->PrintShopConfigPrice->getByPriceType('packageWeight');
                if (count($prices) != 1) {
                    throw new Exception('Must be one price for price type packageWeight');
                }
                return ceil($totalWeight / $prices[0]['amount']) * $count;
            case 'cutSharp':
                return ($workspace['longSideSheets'] + $workspace['shortSideSheets'] + 2) * $sheets;
            case 'cutClipping':
                return (($workspace['longSideSheets'] + $workspace['shortSideSheets'] + 2) * 2 - 4) * $sheets;
            default:
                return 0;
        }
    }

    private function calculateOperationTime($deviceInfo, $calculationUnit, $thickness)
    {
        $stackHeight = $deviceInfo['printedStackHeight'] ?: $deviceInfo['stackHeight'];
        $stackingTime = self::getStackingTime($deviceInfo['stackImpositionTime'], $stackHeight, $calculationUnit, $thickness);
        $finalPriceText['stackingTime'][] = "{$stackingTime} min";
        $finalPriceText['transportTime'][] = "{$deviceInfo['transportTime']} min";
        return $deviceInfo['deviceTime'] + $stackingTime + $deviceInfo['transportTime'];
    }

    private function calculateWorkTime($workUnit, $operationTime, $calculationUnit, $deviceSpeed, $repeatedOperationsCount, $projectSheets)
    {
        switch ($workUnit) {
            case 'projectSheets':
            case 'every_sheet_separate':
                return $operationTime * $projectSheets * 60 + $calculationUnit / $deviceSpeed * 3600 * $repeatedOperationsCount;
            default:
                return $operationTime * 60 + $calculationUnit / $deviceSpeed * 3600 * $repeatedOperationsCount;
        }
    }

    private function calculateTotalExpense($expense, $calculationUnit, $deviceSpeed, $operationTime, $repeatedOperationsCount)
    {
        return $expense * $calculationUnit / $deviceSpeed * $repeatedOperationsCount + $expense * $operationTime / 60;
    }

    private function getDeviceInfo($deviceId, $attrID, $optID, $controllerID)
    {
        $deviceInfo = $this->Device->get('ID', $deviceId);
        $this->PrintShopConfigEfficiency->setAttrID($attrID);
        $this->PrintShopConfigEfficiency->setOptID($optID);
        $this->PrintShopConfigEfficiency->setControllerID($controllerID);
        $optionDeviceInfo = $this->PrintShopConfigEfficiency->customGet();
        $fields = ['workUnit', 'deviceTime', 'stackImpositionTime', 'stackHeight', 'printedStackHeight', 'transportTime', 'name'];
        $return = [];
        foreach ($fields as $field) {
            $return[$field] = $optionDeviceInfo[$field] ?? $deviceInfo[$field];
        }
        return $return;
    }

    private function getSpeedForVolume($deviceId, $calculationUnit, $attrID, $optID, $controllerID)
    {
        $this->PrintShopConfigEfficiencySpeed->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySpeed->setOptID($optID);
        $this->PrintShopConfigEfficiencySpeed->setControllerID($controllerID);
        $speeds = $this->PrintShopConfigEfficiencySpeed->getOrderedList();
        if (empty($speeds)) {
            $speeds = $this->DeviceSpeed->getListByDevice($deviceId);
        }
        usort($speeds, fn($a, $b) => $a['volume'] <=> $b['volume']);
        $speeds = array_map(fn($item) => ['value' => $item['speed'], 'volume' => $item['volume']], $speeds);
        return DataUtils::linearApproximation($speeds, $calculationUnit);
    }

    private function getSpeedChange($grammage, $thickness, $stiffness, $sheetFolds, $projectSheets, $cutUse, $deviceID, $optID, $attrID, $controllerID)
    {
        $this->PrintShopConfigEfficiencySpeedChanges->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySpeedChanges->setOptID($optID);
        $this->PrintShopConfigEfficiencySpeedChanges->setControllerID($controllerID);
        $speedChanges = $this->PrintShopConfigEfficiencySpeedChanges->getOrderedList();
        if (empty($speedChanges)) {
            $speedChanges = $this->DeviceSpeedChange->getOrderedList($deviceID);
        }

        $flatten = [];
        $keyNames = ['grammage', 'stiffness', 'thickness', 'sheetFolds', 'projectSheets', 'cutUse'];
        foreach ($speedChanges as $sc) {
            foreach ($keyNames as $kn) {
                if ($sc["{$kn}Min"] && $sc["{$kn}Max"]) {
                    $flatten[] = array_intersect_key($sc, array_flip(["{$kn}Min", "{$kn}Max", 'efficiencyChange']));
                }
            }
        }
        $speedChanges = $flatten;

        usort($speedChanges, fn($a, $b) => $a['efficiencyChange'] <=> $b['efficiencyChange']);
        $percentage = 1;
        $hits = [];
        foreach ($speedChanges as $speedChange) {
            self::checkLimits($grammage, 'grammage', $speedChange, $percentage, $hits);
            self::checkLimits($thickness, 'thickness', $speedChange, $percentage, $hits);
            self::checkLimits($stiffness, 'stiffness', $speedChange, $percentage, $hits);
            self::checkLimits($sheetFolds, 'sheetFolds', $speedChange, $percentage, $hits);
            self::checkLimits($projectSheets, 'projectSheets', $speedChange, $percentage, $hits);
            self::checkLimits($cutUse, 'cutUse', $speedChange, $percentage, $hits);
        }
        return $percentage;
    }

    private static function checkLimits($toCompare, $name, $speedChange, &$percentage, &$hits)
    {
        if (empty($hits[$name]) && $speedChange["${name}Min"] && $speedChange["${name}Max"]) {
            if ($toCompare >= $speedChange["${name}Min"] && $toCompare <= $speedChange["${name}Max"]) {
                $hits[$name] = true;
                $percentage *= (1 + $speedChange['efficiencyChange'] / 100);
            }
        }
    }

    private function getSpeedChangeByRelation($formatWidth, $formatHeight, $deviceID, $optID, $attrID, $controllerID)
    {
        $percentage = 1;
        $relation = $formatHeight / $formatWidth;

        $this->PrintShopConfigEfficiencySideRelations->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySideRelations->setOptID($optID);
        $this->PrintShopConfigEfficiencySideRelations->setControllerID($controllerID);
        $sideRelations = $this->PrintShopConfigEfficiencySideRelations->getOrderedListByRelation();
        if (empty($sideRelations)) {
            $sideRelations = $this->DeviceSideRelations->getOrderedListByRelation($deviceID);
        }
        $sideRelations = DataUtils::uniqueRecords($sideRelations, ['relation', 'efficiencyChange']);
        usort($sideRelations, fn($a, $b) => $b['relation'] <=> $a['relation']);
        foreach ($sideRelations as $sideRelation) {
            if ($relation >= $sideRelation['relation']) {
                $percentage *= (1 + $sideRelation['efficiencyChange'] / 100);
                break;
            }
        }
        return $percentage;
    }

    private static function getStackingTime($stackImpositionTime, $stackHeight, $sheets, $thickness)
    {
        if (!$stackHeight) {
            return 0;
        }
        return $sheets * $thickness / $stackHeight * $stackImpositionTime;
    }

    private function getSpeedChangePercent($speedChange)
    {
        return ($speedChange - 1) * 100;
    }
}
