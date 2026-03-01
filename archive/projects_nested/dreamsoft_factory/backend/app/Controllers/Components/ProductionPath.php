<?php
/**
 * Created by PhpStorm.
 * User: Rafał
 * Date: 30-05-2018
 * Time: 12:48
 */

namespace DreamSoft\Controllers\Components;

use DreamSoft\Models\Order\OrderConfig;
use DreamSoft\Models\PrintShopUser\UserData;
use DreamSoft\Models\ProductionPath\Operator;
use DreamSoft\Models\ProductionPath\Ongoing;
use DreamSoft\Models\ProductionPath\Operation;
use DreamSoft\Models\ProductionPath\OperationDevice;
use DreamSoft\Models\ProductionPath\PrintTypeDevice;
use DreamSoft\Models\ProductionPath\OperationOptionController;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Core\Component;
use DreamSoft\Controllers\Components\CalculateStorage;
use DreamSoft\Controllers\Components\CalculatorDevices;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Controllers\Components\Calculator;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionDescription;
use DreamSoft\Models\PrintShopUser\UserCalcProductAttribute;
use DreamSoft\Models\ProductionPath\OperationOption;
use DreamSoft\Libs\Debugger;

/**
 * Class ProductionPath
 * @package DreamSoft\Controllers\Components
 */
class ProductionPath extends Component
{
    /**
     * @var Operator
     */
    private $Operator;

    public $useModels = array();

    /**
     * @var Operation
     */
    protected $Operation;
    /**
     * @var OrderConfig
     */
    protected $OrderConfig;
    /**
     * @var Ongoing
     */
    protected $Ongoing;
    /**
     * @var OperationDevice
     */
    protected $OperationDevice;
    /**
     * @var PrintTypeDevice
     */
    protected $PrintTypeDevice;
    /**
     * @var UserData
     */
    protected $UserData;
    /**
     * @var OperationOptionController
     */
    protected $OperationOptionController;
    /**
     * @var DpProduct
     */
    protected $DpProduct;
    /**
     * @var CalculateStorage
     */
    private $CalculateStorage;
    /**
     * @var CalculatorDevices
     */
    private $CalculatorDevices;
    /**
     * @var UserCalcProduct
     */
    protected $UserCalcProduct;
     /**
     * @var Calculator
     */
    protected $Calculator;
     /**
     * @var UserCalc
     */
    protected $UserCalc;
    /**
     * @var CalculateAdapter
     */
    private $CalculateAdapter;
    /**
     * @var PrintShopConfigOptionDescription
     */
    private $PrintShopConfigOptionDescription;
    /**
     * @var UserCalcProductAttribute
     */
    private $UserCalcProductAttribute;
    /**
     * @var OperationOption
     */
    private $OperationOption;

    /**
     * ProductionPath constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->Operator = Operator::getInstance();
        $this->Ongoing = Ongoing::getInstance();
        $this->Operation = Operation::getInstance();
        $this->OrderConfig = OrderConfig::getInstance();
        $this->OperationDevice = OperationDevice::getInstance();
        $this->PrintTypeDevice = PrintTypeDevice::getInstance();
        $this->UserData = UserData::getInstance();
        $this->OperationOptionController = OperationOptionController::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->CalculateStorage = CalculateStorage::getInstance();
        $this->CalculatorDevices = CalculatorDevices::getInstance();
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->Calculator = Calculator::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->CalculateAdapter = CalculateAdapter::getInstance();
        $this->PrintShopConfigOptionDescription = PrintShopConfigOptionDescription::getInstance();
        $this->UserCalcProductAttribute = UserCalcProductAttribute::getInstance();
        $this->OperationOption = OperationOption::getInstance();
    }

    /**
     *
     */
    public function getAllOperators()
    {
        $operators = $this->Operator->getAll();
    }

    /**
     * @param array $params
     * @return array
     */
    public function doPath($params = array())
    {
        $appVersion = 0;
        if (isset($params['appVersion'])) {
            $appVersion = $params['appVersion'];
        }

        if ($appVersion == 0) {
            return $this->pathToOrder($params);
        }

        return $this->pathToProduct($params);

    }

    /**
     * @param $params
     * @return array
     */
    private function pathToOrder($params)
    {
        $itemID = $params['itemID'];
        $orderConfig = $this->OrderConfig->get('orderID', $itemID);
        if ($orderConfig && $orderConfig['planed'] == 1) {
            return array('response' => false, 'info' => 'production_already_planned');
        }

        $operations = $this->Operation->getByOrderID($itemID);

        $ongoings = array();
        $order = 1;
        foreach ($operations as $o) {
            $operationID = $o['ID'];

            $controllers = $this->OperationOptionController->getSelectedControllers($o['optionID'], $operationID);
            if ($controllers && count($controllers) && $o['controllerID']) {
                if (!in_array($o['controllerID'], $controllers)) {
                    continue;
                }
            }

            $devices = $this->OperationDevice->getDevices($operationID);
            $deviceID = NULL;
            $orderOnDevice = NULL;
            if (!empty($devices)) {
                foreach ($devices as $d) {
                    $userData = $this->UserData->get('orderID', $itemID);
                    $exist = $this->PrintTypeDevice->exist($userData['printTypeID'], $d['deviceID']);
                    if ($exist) {
                        $deviceID = $d['deviceID'];
                        $orderOnDevice = intval($this->Ongoing->getMaxDeviceOrder($deviceID)) + 1;
                        break;
                    }
                }
                if (!$deviceID) {
                    foreach ($devices as $d) {
                        $printTypesList = $this->PrintTypeDevice->getByDeviceID($d['deviceID']);
                        if (empty($printTypesList)) {
                            $deviceID = $d['deviceID'];
                            $orderOnDevice = intval($this->Ongoing->getMaxDeviceOrder($deviceID)) + 1;
                            break;
                        }
                    }
                }
            }

            $lastID = $this->Ongoing->create(
                compact('itemID', 'operationID', 'order', 'deviceID', 'orderOnDevice', 'appVersion')
            );
            if ($lastID > 0) {
                $ongoings[] = $this->Ongoing->get('ID', $lastID);
            }
            unset($operationID);
            $order++;
        }
        if (!empty($ongoings)) {
            $planed = 1;
            $this->OrderConfig->create(compact('orderID', 'planed'));
        }

        return $ongoings;
    }

    /**
     * @param $params
     * @return array
     */
    private function pathToProduct($params)
    {
        $orderID = $params['itemID'];
        $appVersion = $params['appVersion'];

        $orderConfig = $this->OrderConfig->get('orderID', $orderID);
        if ($orderConfig && $orderConfig['planed'] == 1) {
            return array('response' => false, 'info' => 'production_already_planned');
        }

        $products = $this->DpProduct->getOrdersProducts(array($orderID));

        if($params['update'] && $params['baseID'] && $params['update'] == 1){
            if(sizeof($products) > 0){
                $baseID = $params['baseID'];
                $version = $this->UserCalc->getMaxVersion($baseID);
                $oldUserCalc = $this->UserCalc->getByBaseIDAndVersion($baseID, ($version-1));
                $oldUserCalcProduct = $this->UserCalcProduct->get('calcID', $oldUserCalc['ID']);
                $delete = $this->Ongoing->delete('itemID', $oldUserCalcProduct['ID']);
            }
        }

        $productionTasks = array();
        foreach ($products as $product) {
            $productionTasks[$product['ID']] = $this->DpProduct->searchOperationsForProducts($product['productID']);
        }

        $ongoings = array();
        $sortContainer = array();
        foreach ($productionTasks as $productID => $operations) {

            foreach ($operations as $operation) {

                $operationID = $operation['ID'];

                $controllers = $this->OperationOptionController->getSelectedControllers($operation['optID'], $operationID);
                if ($controllers && count($controllers) && $operation['controllerID']) {
                    if (!in_array($operation['controllerID'], $controllers)) {
                        continue;
                    }
                }

                $devices = $this->OperationDevice->getDevices($operationID);
                $deviceID = NULL;
                $orderOnDevice = NULL;

                if (!empty($devices)) {

                    $matchedDevices = array();

                    foreach ($devices as $d) {

                        switch (intval($operation['attributeType'])) {
                            case ATTRIBUTE_TYPE_STANDARD:
                                $matchedDevices[] = $d;
                                break;
                            case ATTRIBUTE_TYPE_PRINT:
                                $exist = $this->PrintTypeDevice->exist($operation['printTypeID'], $d['deviceID']);
                                if ($exist) {
                                    $matchedDevices[] = $d;
                                }
                                break;
                            case ATTRIBUTE_TYPE_PAPER:
                                $matchedDevices[] = $d;
                                break;
                        }

                    }

                    if ($matchedDevices) {
                        $bestDevice = $this->selectLessBusyDevice($matchedDevices);
                        $deviceID = $bestDevice['deviceID'];
                        $orderOnDevice = intval($bestDevice['count']) + 1;

                    }
                }

                if (!$deviceID) {
                    continue;
                }

                $itemID = $operation['calcProductID'];

                $existID = $this->Ongoing->checkExist($itemID, $operationID);

                if ($existID) {
                    continue;
                }

                if (!array_key_exists($operation['calcProductID'], $sortContainer)) {
                    $sortContainer[$operation['calcProductID']] = 1;
                } else {
                    $sortContainer[$operation['calcProductID']]++;
                }

                $inProgress = 0;
                if ($sortContainer[$operation['calcProductID']] === 1) {
                    $inProgress = 1;
                }

                $order = $sortContainer[$operation['calcProductID']];

                $created = date(DATE_FORMAT);

                $lastID = $this->Ongoing->create(
                    compact(
                        'itemID',
                        'operationID',
                        'order',
                        'deviceID',
                        'orderOnDevice',
                        'appVersion',
                        'inProgress',
                        'created'
                    )
                );

                if ($lastID > 0) {
                    
                    //add saving estimatedTime
                    $userCalcProduct = $this->UserCalcProduct->get('ID', $itemID);
                    $userCalc = $this->UserCalc->get('ID', $userCalcProduct['calcID']);
                    $userAttributes = $this->UserCalcProductAttribute->get('calcProductID', $userCalcProduct['ID'], true);

                    foreach($userAttributes as $userAttribute){
                        $attrID = $userAttribute['attrID'];
                        $optID = $userAttribute['optID'];
                        $controllerID = $userAttribute['controllerID'];
                        $operations = $this->OperationOption->get('optionID', $optID, true);
                        foreach($operations as $operation){
                            if($operationID == $operation['operationID']){
                                $attr = $this->CalculateStorage->getAttribute($attrID);
                                $sheets = $userCalcProduct['sheets'];
                                $option = $this->CalculateStorage->getOption($optID);
                                $rollLength = NULL;
                                if ($option['rollLength'] > 0) {
                                    $rollLength = $option['rollLength'];
                                }
                                $volume = $userCalc['volume'];
                                $setIncrease = $this->CalculateStorage->getIncrease('set', $volume, $userCalcProduct['formatID']);
                                $workspace = $this->CalculateStorage->getWorkspace($userCalcProduct['workspaceID']);
                                $format = $this->CalculateStorage->getFormat($userCalcProduct['formatID'],$userCalcProduct);
                                $totalArea = $this->Calculator->getTotalArea($workspace, $volume, $rollLength, $setIncrease, $format);

                                $perimeter = $this->Calculator->_perimeter($volume, $format);

                                $projectSheets = $userCalcProduct['projectSheets'];

                                $pages = $userCalcProduct['pages'];
                                $oneSide = false;
                                if ($option['oneSide'] == 1) {
                                    $oneSide = true;
                                }
                                $optionsArray[] = $optID;
                                $printRotated = 0;
                                if ($this->CalculateStorage->getPrintRotated($userCalcProduct['printTypeID'], $optionsArray)) {
                                    $printRotated = 1;
                                }
                                $doublePage = $this->CalculateStorage->getDoublePage($userCalcProduct['groupID'], $userCalcProduct['typeID']);
                                //TODO: make sure of proper working selectedUseForSheet
                                $selectedUseForSheet = false;
                                $selectedUseForSheet = $workspace['printTypeWorkspaceSettings']['usePerSheet'];
                                $projectSheetsInfo = $this->Calculator->getProjectSheets(
                                    $workspace,
                                    $pages,
                                    $oneSide,
                                    $printRotated,
                                    $doublePage,
                                    $selectedUseForSheet,
                                    $format
                                );
                                $calcAllSheets = $this->Calculator->getAllSheets(
                                    $workspace,
                                    $pages,
                                    $volume,
                                    $oneSide,
                                    $printRotated,
                                    $doublePage,
                                    $selectedUseForSheet,
                                    $format
                                );

                                if ($calcAllSheets['areaPerSheetForStandardResult']) {
                                    $workspace['longSideSheets'] = $calcAllSheets['areaPerSheetForStandardResult']['longSide'];
                                    $workspace['shortSideSheets'] = $calcAllSheets['areaPerSheetForStandardResult']['shortSide'];
                                }

                                $fullProjectsSheets = $this->CalculateAdapter->getInfoForFullProjectSheets(
                                    $projectSheetsInfo['noRoundSheets'],
                                    $calcAllSheets['sheets'],
                                    $userCalcProduct['projectSheets']
                                );

                                $sheetCuts = 0;
                                $maxFolds = null;
                                if (isset($option['maxFolds']) && $option['maxFolds'] !== null) {
                                    $maxFolds = $option['maxFolds'];
                                }
                                $uzytkipersheet = $calcAllSheets['perSheet'];
                                
                                $folds = ceil(log($uzytkipersheet, 2));
                                if ($maxFolds !== null && $maxFolds > 0) {
                                    while ($folds > $maxFolds) {
                                        $folds--;
                                        $sheetCuts++;
                                    }
                                }

                                $sheetsAfterCut = $sheets * Calculator::getStraightCutsPieces($sheetCuts);

                                $totalSheetFolds = $folds;
                                if ($sheetCuts > 0) {
                                    $totalSheetFolds *= $sheetCuts * 2;
                                }

                                $size = $this->CalculateAdapter->calculateSize($userCalcProduct['formatWidth'], $userCalcProduct['formatHeight']);

                                $paperInfo['weight']=$option['weight'];
                                $this->PrintShopConfigOptionDescription->setOptID($optID);
                                $this->PrintShopConfigOptionDescription->setAttrID($attrID);
                                $paperInfo['stiffness']=$this->PrintShopConfigOptionDescription->getByTypeName('stiffness');

                                $finalPriceText=[];

                                $deviceDetails = $this->CalculatorDevices->calculateDeviceDetails($attrID, $optID, $controllerID, $sheets, $totalArea, $perimeter, $volume, $projectSheets, $fullProjectsSheets, $sheetCuts, $sheetsAfterCut, $totalSheetFolds, $size, $paperInfo['stiffness'], $paperInfo['weight'], $userCalcProduct['formatWidth'], $userCalcProduct['formatHeight'], $pages, $userCalc['weight'],  $workspace, $finalPriceText, [$deviceID]);
                                $deviceTime = $deviceDetails['deviceTime'];
                                //==========
                                $this->Ongoing->update($lastID, 'estimatedTime', $deviceTime);
                            }
                        }
                    }

                    $ongoings[] = $this->Ongoing->get('ID', $lastID);
                }
                unset($operationID);
            }
        }


        return $ongoings;

    }

    /**
     * @param $devices
     * @return bool|array
     */
    private function selectLessBusyDevice($devices)
    {
        if (!$devices) {
            return false;
        }
        $leader = array();
        foreach ($devices as $device) {
            if (empty($leader)) {
                $leader = $device;
                continue;
            }
            if ($device['count'] < $leader['count']) {
                $leader = $device;
            }
        }

        if (!array_key_exists('count', $leader)) {
            return false;
        }

        return $leader;
    }

}
