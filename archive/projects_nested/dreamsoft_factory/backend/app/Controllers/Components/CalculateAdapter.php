<?php

namespace DreamSoft\Controllers\Components;

use DreamSoft\Core\Component;

class CalculateAdapter extends Component
{
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * @param $pages
     * @param $oneSide
     * @param $doublePage
     * @return int
     */
    public function getAmountPages($pages, $oneSide, $doublePage)
    {
        if ($oneSide) {
            $pages *= 2;
        }

        if ($doublePage) {
            $pages /= 2;
        }

        return $pages % 2 ? ++$pages : $pages;
    }

    /**
     * @param $workspaceWidth
     * @param $workspaceHeight
     * @param $formatWidth
     * @param $formatHeight
     * @param $format
     * @return array
     */
    public function getAreaPerSheetForStandard($workspaceWidth, $workspaceHeight, $formatWidth, $formatHeight, $format)
    {
        $horizontal = floor($workspaceWidth / $formatWidth) * floor($workspaceHeight / $formatHeight);
        $vertical = floor($workspaceWidth / $formatHeight) * floor($workspaceHeight / $formatWidth);

        $isHorizontal = $horizontal >= $vertical;
        $max = $isHorizontal ? $horizontal : $vertical;
        $longSide = $isHorizontal ? floor($workspaceWidth / $formatWidth) : floor($workspaceWidth / $formatHeight);
        $shortSide = $isHorizontal ? floor($workspaceHeight / $formatHeight) : floor($workspaceHeight / $formatWidth);
        $isDoubledPages = Calculator::isDoubledPages($format);

        return compact('max', 'shortSide', 'longSide', 'isHorizontal', 'formatWidth', 'formatHeight', 'isDoubledPages');
    }

    /**
     * @param $area
     * @param $workspaceWidth
     * @param $formatWidth
     * @param $formatHeight
     * @return float|int
     */
    public function getUsedHeight($area, $workspaceWidth, $formatWidth, $formatHeight)
    {
        $horizontalWidth = floor($workspaceWidth / $formatWidth);
        $verticalWidth = floor($workspaceWidth / $formatHeight);

        $isHorizontal = $horizontalWidth > $verticalWidth || ($horizontalWidth == $verticalWidth && $formatWidth > $formatHeight);
        $rowHeight = $isHorizontal ? $formatHeight : $formatWidth;
        $perRow = $isHorizontal ? $horizontalWidth : $verticalWidth;

        return ($area / $perRow) * $rowHeight;
    }

    /**
     * @param $pages
     * @param $volume
     * @return float|int
     */
    public function getAreaForRolled($pages, $volume)
    {
        return $pages / 2 * $volume;
    }

    /**
     * @param $usedHeight
     * @param $workspaceHeight
     * @return float
     */
    public function getSheetsForRolled($usedHeight, $workspaceHeight)
    {
        return ceil($usedHeight / $workspaceHeight);
    }

    /**
     * @param $pages
     * @param $perSheet
     * @param $volume
     * @return float|int
     */
    public function getSheetsForStandard($pages, $perSheet, $volume)
    {
        return ($pages / ($perSheet * 2)) * $volume;
    }

    /**
     * @param $pages
     * @param $perSheet
     * @param $volume
     * @return float|int
     */
    public function getSheetsForStandardPrintRotated($pages, $perSheet, $volume)
    {
        $area = $pages / 2;
        $sheets = $area / $perSheet;
        $sheets *= $volume;

        return $sheets;
    }

    /**
     * @param $volume
     * @param $increase
     * @param $rows
     * @return float
     */
    public function addSetIncreaseToVolume($volume, $increase, $rows)
    {
        if ($increase) {
            $volume += ceil(intval($increase) / $rows);
        }
        return $volume;
    }

    /**
     * @param $volume
     * @param $increase
     * @return float
     */
    public function addSetIncreaseToVolumeTotal($volume, $increase)
    {
        if ($increase) {
            $volume += ceil(intval($increase));
        }
        return $volume;
    }

    /**
     * @param $formatWidth
     * @param $formatHeight
     * @return float|int
     */
    public function calculateSize($formatWidth, $formatHeight)
    {
        return ($formatWidth / 1000) * ($formatHeight / 1000);
    }

    /**
     * @param $formatWidth
     * @param $formatHeight
     * @param $slope
     * @return float|int
     */
    public function calculateSizeNet($formatWidth, $formatHeight, $slope)
    {
        $reducedWidth = $formatWidth - $slope * 2;
        $reducedHeight = $formatHeight - $slope * 2;

        return ($reducedWidth / 1000) * ($reducedHeight / 1000);
    }

    /**
     * @param $size
     * @param $maxRollLength
     * @param $formatWidth
     * @param $rollSlipIncrease
     * @return float|int
     */
    public function calculateSizeForRollPrint($size, $maxRollLength, $formatWidth, $rollSlipIncrease)
    {
        $length = $this->getLengthForRoll($size, $formatWidth);
        $numberOfRolls = $this->getNumberOfRolls($length, $maxRollLength);

        if ($rollSlipIncrease) {
            $increase = ($formatWidth / 10) * ($rollSlipIncrease * $numberOfRolls);
            $size += $increase / 10000;
        }

        return $size;
    }

    /**
     * @param $length
     * @param $maxRollLength
     * @return float
     */
    public function getNumberOfRolls($length, $maxRollLength)
    {
        return ceil($length / $maxRollLength);
    }

    /**
     * @param $size
     * @param $formatWidth
     * @return float|int
     */
    public function getLengthForRoll($size, $formatWidth)
    {
        return ($size * 10000) / ($formatWidth / 10);
    }

    /**
     * @param $formatWidth
     * @param $formatHeight
     * @param $workspaceWidth
     * @param $volume
     * @return float|int
     */
    public function getLengthForTotalArea($formatWidth, $formatHeight, $workspaceWidth, $volume)
    {
        $horizontalWidth = floor($workspaceWidth / $formatWidth);
        $verticalWidth = floor($workspaceWidth / $formatHeight);

        $length = $horizontalWidth > $verticalWidth 
            ? $formatHeight * ceil($volume / $horizontalWidth) 
            : $formatWidth * ceil($volume / $verticalWidth);

        return $length;
    }

    /**
     * @param $length
     * @param $workspace
     * @return mixed
     */
    public function addPaperHeightForTotalArea($length, $workspace)
    {
        if ($workspace['paperHeight']) {
            $length += $workspace['paperHeight'] - $workspace['height'];
        }

        return $length;
    }

    /**
     * @param $length
     * @param $maxRollLength
     * @return float
     */
    public function getNumberOfRollsForTotalArea($length, $maxRollLength)
    {
        return ceil($length / 10 / $maxRollLength);
    }

    /**
     * @param $length
     * @param $rollSlipIncrease
     * @param $numberOfRolls
     * @return float|int
     */
    public function addRollSlipIncrease($length, $rollSlipIncrease, $numberOfRolls)
    {
        return $rollSlipIncrease ? $length + $rollSlipIncrease * $numberOfRolls * 10 : $length;
    }

    /**
     * @param $length
     * @param $workspace
     * @return float|int
     */
    public function calculateTotalArea($length, $workspace)
    {
        return ($length / 1000) * ($workspace['paperWidth'] / 1000);
    }

    /**
     * @param $basicUnitOfSheets
     * @param $noRoundSheets
     * @return float
     */
    public function getFullProjectSheets($basicUnitOfSheets, $noRoundSheets)
    {
        $fullNoRoundSheets = floor($noRoundSheets);
        return $fullNoRoundSheets > 0 ? ceil(($fullNoRoundSheets * $basicUnitOfSheets) / $fullNoRoundSheets) : 0;
    }

    /**
     * @param $noRoundSheets
     * @return float
     */
    public function getModuloFromNoRoundSheets($noRoundSheets)
    {
        return $noRoundSheets - floor($noRoundSheets);
    }

    /**
     * @param $noRoundSheets
     * @return float|int
     */
    public function getNoRoundProjectSheet($noRoundSheets)
    {
        return $noRoundSheets > 0.5 
            ? 1 
            : ($noRoundSheets > 0.25 ? 0.5 : 0.25);
    }

    /**
     * @param $modulo
     * @param $noRoundSheets
     * @return float|int
     */
    public function getNoRoundProjectSheetWithModulo($modulo, $noRoundSheets)
    {
        return $modulo == 0 
            ? floor($noRoundSheets) 
            : ($modulo > 0.25 ? floor($noRoundSheets) + 0.5 : floor($noRoundSheets) + 0.25);
    }

    /**
     * @param $projectSheets
     * @param $noRoundSheets
     * @return float|int|null
     */
    public function getInfoForPartProjectSheetsAmount($projectSheets, $noRoundSheets)
    {
        return $noRoundSheets > 0 
            ? ($noRoundSheets > 1 ? floor($noRoundSheets) : floor($projectSheets)) 
            : $projectSheets;
    }

    /**
     * @param $noRoundSheets
     * @param $sheets
     * @return float|int|null
     */
    public function getPartProjectSheets($noRoundSheets, $sheets)
    {
        $partProjectSheets = [];

        if (($noRoundSheets - ceil($noRoundSheets)) != 0) {
            $modulo = $this->getModuloFromNoRoundSheets($noRoundSheets);

            if (fmod($modulo, 0.125) == 0) {
                while ($modulo > 0) {
                    if ($modulo >= 0.5) {
                        $partProjectSheets['0.5'] = ceil($sheets / $noRoundSheets / 2);
                        $modulo -= 0.5;
                    } elseif ($modulo >= 0.25) {
                        $partProjectSheets['0.25'] = ceil($sheets / $noRoundSheets / 4);
                        $modulo -= 0.25;
                    } elseif ($modulo >= 0.125) {
                        $partProjectSheets['0.125'] = ceil($sheets / $noRoundSheets / 8);
                        $modulo -= 0.125;
                    } else {
                        break;
                    }
                }
            } else {
                $partProjectSheets['0.33'] = ceil(($modulo * $sheets / $noRoundSheets));
            }
        }

        return $partProjectSheets;
    }

    /**
     * @param $noRoundSheets
     * @param $sheets
     * @param $projectSheets
     * @return float|null
     */
    public function getInfoForFullProjectSheets($noRoundSheets, $sheets, $projectSheets)
    {
        if ($noRoundSheets > 0) {
            $basicUnitOfSheets = $sheets / $noRoundSheets;
            return $this->getFullProjectSheets($basicUnitOfSheets, $noRoundSheets);
        }

        $basicUnitOfSheets = $sheets / $projectSheets;
        return ceil((floor($projectSheets) * $basicUnitOfSheets) / floor($projectSheets));
    }

    /**
     * @param $noRoundSheets
     * @param $projectSheets
     * @return float|int|null
     */
    public function getInfoNoRoundedProjectSheets($noRoundSheets, $projectSheets)
    {
        if ($noRoundSheets > 0) {
            if ($noRoundSheets > 1) {
                $modulo = $this->getModuloFromNoRoundSheets($noRoundSheets);
                return $this->getNoRoundProjectSheetWithModulo($modulo, $noRoundSheets);
            }

            return $this->getNoRoundProjectSheet($noRoundSheets);
        }

        return $projectSheets;
    }

    /**
     * @param $noRoundSheets
     * @return float|null
     */
    public function getInfoForValueOfPartInProjectSheets($noRoundSheets)
    {
        if ($noRoundSheets > 0 && $noRoundSheets > 1) {
            return $this->getModuloFromNoRoundSheets($noRoundSheets);
        }

        return null;
    }

    /**
     * @param $formatID
     * @param $printTypeID
     * @param $workspaceID
     * @param $printTypeWorkspaces
     * @return null|array
     */
    public function getPrintTypeWorkspaceSettings($formatID, $printTypeID, $workspaceID, $printTypeWorkspaces)
    {
        if ($printTypeWorkspaces &&
            isset($printTypeWorkspaces[$formatID][$printTypeID][$workspaceID]) &&
            $printTypeWorkspaces[$formatID][$printTypeID][$workspaceID]) {
            $printTypeWorkspace = $printTypeWorkspaces[$formatID][$printTypeID][$workspaceID];

            return [
                'usePerSheet' => $printTypeWorkspace['usePerSheet'],
                'operationDuplication' => $printTypeWorkspace['operationDuplication']
            ];
        }

        return null;
    }

    /**
     * @param $workspace
     * @param $option
     * @return int|null
     */
    public function getRepeatedOperationsNumber($workspace, $option)
    {
        if (intval($option['repeatedOperation']) === 1 &&
            $workspace['printTypeWorkspaceSettings']['operationDuplication'] > 0) {
            return intval($workspace['printTypeWorkspaceSettings']['operationDuplication']);
        }

        return null;
    }

    /**
     * @param $value
     * @param $volume
     * @return float|int
     */
    public function multiplicationByVolume($value, $volume = null)
    {
        return $volume ? $value * $volume : $value;
    }
}
