<?php

namespace DreamSoft\Controllers\Components;

use DreamSoft\Core\Component;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigDetailPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigDiscountPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigIncrease;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPaperPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrice;
use DreamSoft\Models\PrintShopProduct\PrintShopStaticPrice;
use DreamSoft\Models\Order\DpOrder;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\Tax\Tax;
use DreamSoft\Models\Price\BasePrice;
use Exception;

class CalculatorCollect extends Component
{
    protected $CalculateStorage;
    protected $PrintShopConfigIncrease;
    protected $PrintShopConfigDetailPrice;
    protected $PrintShopConfigPaperPrice;
    protected $PrintShopConfigDiscountPrice;
    protected $PrintShopConfigPrice;
    protected $PrintShopStaticPrice;
    protected $DpOrder;
    protected $UserCalc;
    protected $BasePrice;
    protected $Tax;
    private $CalculateAdapter;
    private $userID;
    private $priceTypes = [];
    private $countBasePrice = false;
    private $selectedTechnology;
    private $commonOptions = [];
    private $attributeFactories = [];

    public function __construct()
    {
        parent::__construct();
        $this->CalculateStorage = CalculateStorage::getInstance();
        $this->PrintShopConfigIncrease = PrintShopConfigIncrease::getInstance();
        $this->PrintShopConfigDetailPrice = PrintShopConfigDetailPrice::getInstance();
        $this->PrintShopConfigPaperPrice = PrintShopConfigPaperPrice::getInstance();
        $this->PrintShopConfigDiscountPrice = PrintShopConfigDiscountPrice::getInstance();
        $this->PrintShopConfigPrice = PrintShopConfigPrice::getInstance();
        $this->PrintShopStaticPrice = PrintShopStaticPrice::getInstance();
        $this->DpOrder = DpOrder::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->BasePrice = BasePrice::getInstance();
        $this->CalculateAdapter = CalculateAdapter::getInstance();
        $this->Tax = Tax::getInstance();
    }

    public function getUserID()
    {
        return $this->userID;
    }

    public function setUserID($userID)
    {
        $this->userID = $userID;
    }

    public function getPriceTypes()
    {
        return $this->priceTypes;
    }

    public function setPriceTypes($priceTypes)
    {
        $this->priceTypes = $priceTypes;
    }

    public function isCountBasePrice()
    {
        return $this->countBasePrice;
    }

    public function setCountBasePrice($countBasePrice)
    {
        $this->countBasePrice = $countBasePrice;
    }

    public function getSelectedTechnology()
    {
        return $this->selectedTechnology;
    }

    public function setSelectedTechnology($selectedTechnology)
    {
        $this->selectedTechnology = $selectedTechnology;
    }

    public function getCommonOptions()
    {
        return $this->commonOptions;
    }

    public function setCommonOptions($commonOptions)
    {
        $this->commonOptions = $commonOptions;
    }

    public function getAttributeFactories()
    {
        return $this->attributeFactories;
    }

    public function setAttributeFactories($attributeFactories)
    {
        $this->attributeFactories = $attributeFactories;
    }

    public function calculate($products)
    {
        $this->setCommonOptions($this->searchCommonOptions($products));
        foreach ($products as $product) {
            $calculations[$product['calcID']] = array_map(function ($calcProduct) use ($product) {
                return $this->calcPrice(
                    $calcProduct['groupID'],
                    $calcProduct['typeID'],
                    $calcProduct['formatID'],
                    $calcProduct['formatWidth'],
                    $calcProduct['formatHeight'],
                    $calcProduct['pages'],
                    $product['volume'],
                    $calcProduct['attributes'],
                    $product['orderID'],
                    $product['calcID'],
                    $calcProduct['printTypeID'],
                    $calcProduct['workspaceID']
                );
            }, $product['calcProducts']);
        }

        return $this->sumAttributeFactories();
    }

    public function restorePrices($products)
    {
        $this->setCommonOptions($this->searchCommonOptions($products));
        $updated = 0;

        foreach ($products as $product) {
            if ($product['beforeReCountPriceID']) {
                $priceID = $product['beforeReCountPriceID'];
                if ($this->UserCalc->update($product['calcID'], 'priceID', $priceID) &&
                    $this->UserCalc->update($product['calcID'], 'beforeReCountPriceID', null)) {
                    $updated++;
                }
            }
        }

        return $updated > 0;
    }

    private function searchCommonOptions($products)
    {
        if (!$products) {
            return [];
        }
        $commonOptions = [];
        $allUsedOptions = [];

        foreach ($products as $product) {
            foreach ($product['calcProducts'] as $calcProduct) {
                foreach ($calcProduct['attributes'] as $attribute) {
                    if (in_array($attribute['optID'], $allUsedOptions)) {
                        $commonOptions[] = $attribute['optID'];
                    } else {
                        $allUsedOptions[] = $attribute['optID'];
                    }
                }
            }
        }

        return $commonOptions;
    }

    private function calcPrice($groupID, $typeID, $formatID, $formatWidth, $formatHeight, $pages, $volume, $attributes, $orderID, $calculateID, $printTypeID, $workspaceID)
    {
        $printTypes = $this->getPrintTypes($formatID, $volume);
        $doublePage = $this->CalculateStorage->getDoublePage($groupID, $typeID);
        $similarPages = $this->CalculateStorage->getSimilarPages($groupID, $typeID);
        $setIncrease = $this->CalculateStorage->getIncrease('set', $volume, $formatID);
        $optionProperties = $this->getOptionsProperties($attributes, $pages, $doublePage);
        $format = $this->CalculateStorage->getFormat($formatID);
        $order = $this->DpOrder->get('ID', $orderID);

        if ($order['userID']) {
            $this->setUserID($order['userID']);
        }

        $calcPrices = [];
        $discountGroups = $this->getDiscountGroups($order['userID']);

        foreach ($printTypes as $printType) {
            if ($printType['printTypeID'] != $printTypeID) {
                continue;
            }

            $selectedTechnology = $this->getSelectedTechnology();
            $noCounting = $selectedTechnology && $selectedTechnology['ID'] != $printType['pricelistID'];
            $rows = $this->getFormatRows($format);
            $workspaces = $this->getWorkspaces($printType['workspaceID'], $printType['printTypeID']);

            foreach ($workspaces as $workspace) {
                if (intval($workspace['ID']) != $workspaceID) {
                    continue;
                }

                $calcAllSheets = $this->getAllSheets($workspace, $pages, $volume, $optionProperties['oneSide'], $optionProperties['printRotated'], $doublePage, $formatWidth, $formatHeight, $format);
                $sheets = $calcAllSheets['sheets'];

                if ($sheets === null) {
                    continue;
                }

                $projectSheet = $this->getProjectSheets($workspace, $pages, $similarPages, $doublePage, $optionProperties, $formatWidth, $formatHeight, $format);
                $area = $this->getArea($volume, $rows, $optionProperties['rollLength'], $setIncrease, $format['slope'], $formatWidth, $formatHeight);
                $perimeter = $this->getPerimeter($volume, $formatWidth, $formatHeight);
                $copiesOnAllSheets = $this->getCopiesOnAllSheets($volume, $pages, $optionProperties['oneSide'], $doublePage);
                $totalArea = $this->getTotalArea($workspace, $volume, $optionProperties['rollLength'], $setIncrease, $formatWidth, $formatHeight);
                $totalSheetFolds = $this->getTotalSheetFolds($calcAllSheets['perSheet'], $optionProperties['oneSide']);
                $sheetIncrease = $this->CalculateStorage->getIncrease('sheet', $sheets, $formatID);

                $price = 0;
                $expense = 0;
                $basePrice = 0;
                $options = ['pages' => intval($pages)];

                foreach ($attributes as $attribute) {
                    $AttributeProcessFactory = new AttributeProcessFactory();
                    $AttributeProcessFactory->setVolume($volume);
                    $AttributeProcessFactory->setAttributeID($attribute['attrID']);
                    $AttributeProcessFactory->setOptionID($attribute['optID']);
                    $AttributeProcessFactory->setPrintTypeID($printType['printTypeID']);
                    $AttributeProcessFactory->setPriceListID($printType['pricelistID']);
                    $AttributeProcessFactory->setWorkspace($workspace);
                    $AttributeProcessFactory->setSheets($sheets);
                    $AttributeProcessFactory->setProjectSheet($projectSheet);
                    $AttributeProcessFactory->setArea($area);
                    $AttributeProcessFactory->setPerimeter($perimeter);
                    $AttributeProcessFactory->setAttributePages($attribute['attrPages']);
                    $AttributeProcessFactory->setPages($pages);
                    $AttributeProcessFactory->setSize($optionProperties['size']);
                    $AttributeProcessFactory->setCopiesOnAllSheets($copiesOnAllSheets);
                    $AttributeProcessFactory->setTotalArea($totalArea);
                    $AttributeProcessFactory->setTotalSheetFolds($totalSheetFolds);
                    $AttributeProcessFactory->setSheetIncrease($sheetIncrease);
                    $AttributeProcessFactory->setSetIncrease($setIncrease);
                    $AttributeProcessFactory->setFormatWidth($formatWidth);
                    $AttributeProcessFactory->setFormatHeight($formatHeight);
                    $AttributeProcessFactory->setMaxFolds($optionProperties['maxFolds']);
                    $AttributeProcessFactory->setExpense(false);
                    $AttributeProcessFactory->setCalculateID($calculateID);

                    $attributePrice = $this->attributePrice($AttributeProcessFactory);

                    if (in_array($attribute['optID'], $this->getCommonOptions())) {
                        $this->addToAttributeFactories($AttributeProcessFactory, $attributePrice);
                    }

                    if ($discountGroups) {
                        $this->setCountBasePrice(true);
                        $attributePriceBase = $this->attributePrice($AttributeProcessFactory);
                        $this->setCountBasePrice(false);
                        $basePrice += $attributePriceBase['finalPrice'];
                    } else {
                        $basePrice += $attributePrice['finalPrice'];
                    }

                    $price += $attributePrice['finalPrice'];
                    $AttributeProcessFactory->setExpense(true);
                    $attributeExpense = $this->attributePrice($AttributeProcessFactory);
                    $expense += $attributeExpense['finalPrice'];
                    $options[$attribute['attrID']] = intval($attribute['optID']);
                    $options['volumes'] = intval($volume);

                    if ($attributePrice['finalPrice'] === null) {
                        $excludedPrintType = true;
                        break;
                    }
                }

                if ($excludedPrintType) {
                    continue;
                }

                $this->PrintShopStaticPrice->setGroupID($groupID);
                $this->PrintShopStaticPrice->setTypeID($typeID);
                $this->PrintShopStaticPrice->setFormatID($formatID);

                if ($staticPrice = $this->PrintShopStaticPrice->getStaticPrice($options)) {
                    $price = $staticPrice;
                    $basePrice = $staticPrice;
                    $staticExpense = $this->PrintShopStaticPrice->getStaticExpense($options);
                    if ($staticExpense) {
                        $expense = $staticExpense;
                    }
                }

                $setPriceIncrease = $this->CalculateStorage->getIncrease('setPrice', $volume, $formatID);
                if ($setPriceIncrease) {
                    $price += floatval($setPriceIncrease) * $volume;
                    $basePrice += floatval($setPriceIncrease) * $volume;
                }

                $pricePercentageIncrease = $this->CalculateStorage->getIncrease('ptcPrice', $volume, $formatID);
                if ($pricePercentageIncrease) {
                    $price *= 1 + floatval($pricePercentageIncrease / 100);
                    $basePrice *= 1 + floatval($pricePercentageIncrease / 100);
                }

                $calcPrices[] = [
                    'price' => $price,
                    'expense' => $expense,
                    'basePrice' => $basePrice,
                    'noCounting' => $noCounting,
                    'printType' => $printType,
                    'workspace' => $workspace
                ];
            }
        }

        $price = null;
        $expense = null;
        $basePrice = null;
        $printType = null;
        $workspace = null;

        foreach ($calcPrices as $eachPrice) {
            if ($eachPrice['noCounting']) {
                continue;
            }
            if ($eachPrice['price'] < $price || $price === null) {
                $price = $eachPrice['price'];
                $basePrice = $eachPrice['basePrice'];
                $expense = $eachPrice['expense'];
                $printType = $eachPrice['printType'];
                $workspace = $eachPrice['workspace'];
            }
        }

        $attributeDiscount = $basePrice - $price;

        return [
            'price' => $price,
            'expense' => $expense,
            'basePrice' => $basePrice,
            'attributeDiscount' => $attributeDiscount,
            'printType' => $printType,
            'workspace' => $workspace
        ];
    }

    private function sumAttributeFactories()
    {
        $attributeFactories = $this->getAttributeFactories();
        $updated = 0;

        if ($attributeFactories) {
            foreach ($attributeFactories as $key => $factories) {
                if (count($factories) > 1) {
                    $SumAttributeProcessFactory = new AttributeProcessFactory();
                    $sumRegularPrice = 0;
                    $aggregateCalculations = [];
                    $aggregateAttributePrices = [];

                    foreach ($factories as $factory) {
                        $currentFactory = $factory['factory'];
                        $sumRegularPrice += $factory['regularPrice'];
                        $aggregateCalculations[] = $factory['calculationID'];
                        $aggregateAttributePrices[$factory['calculationID']] = $factory['regularPrice'];

                        if ($currentFactory->getAttributePages() > 0) {
                            continue;
                        }

                        $SumAttributeProcessFactory->setOptionID($currentFactory->getOptionID());
                        $SumAttributeProcessFactory->setAttributeID($currentFactory->getAttributeID());
                        $SumAttributeProcessFactory->setVolume(
                            intval($SumAttributeProcessFactory->getVolume()) + $currentFactory->getVolume()
                        );
                        $SumAttributeProcessFactory->setPrintTypeID($currentFactory->getPrintTypeID());
                        $SumAttributeProcessFactory->setPriceListID($currentFactory->getPriceListID());
                        $SumAttributeProcessFactory->setWorkspace($currentFactory->getWorkspace());
                        $SumAttributeProcessFactory->setSheets(floatval($SumAttributeProcessFactory->getSheets()) + $currentFactory->getSheets());
                        $SumAttributeProcessFactory->setProjectSheet(floatval($SumAttributeProcessFactory->getProjectSheet()) + $currentFactory->getProjectSheet());

                        $area = $SumAttributeProcessFactory->getArea();
                        $currentArea = $currentFactory->getArea();
                        $newArea = [
                            'size' => floatval($area['size']) + $currentArea['size'],
                            'sizeNet' => floatval($area['sizeNet']) + $currentArea['sizeNet']
                        ];
                        $SumAttributeProcessFactory->setArea($newArea);

                        $SumAttributeProcessFactory->setPerimeter(floatval($SumAttributeProcessFactory->getPerimeter()) + $currentFactory->getPerimeter());
                        $SumAttributeProcessFactory->setPages(intval($SumAttributeProcessFactory->getPages()) + $currentFactory->getPages());
                        $SumAttributeProcessFactory->setSize(floatval($SumAttributeProcessFactory->getSize()) + $currentFactory->getSize());
                        $SumAttributeProcessFactory->setCopiesOnAllSheets(intval($SumAttributeProcessFactory->getCopiesOnAllSheets()) + $currentFactory->getCopiesOnAllSheets());
                        $SumAttributeProcessFactory->setTotalArea($SumAttributeProcessFactory->getTotalArea() + $currentFactory->getTotalArea());
                        $SumAttributeProcessFactory->setTotalSheetFolds(floatval($SumAttributeProcessFactory->getTotalSheetFolds()) + $currentFactory->getTotalSheetFolds());
                        $SumAttributeProcessFactory->setSheetIncrease($currentFactory->getSheetIncrease());
                        $SumAttributeProcessFactory->setSetIncrease($currentFactory->getSetIncrease());
                        $SumAttributeProcessFactory->setFormatWidth(intval($currentFactory->getFormatWidth()));
                        $SumAttributeProcessFactory->setFormatHeight(intval($currentFactory->getFormatHeight()));
                        $SumAttributeProcessFactory->setMaxFolds(intval($SumAttributeProcessFactory->getMaxFolds()) + $currentFactory->getMaxFolds());
                    }

                    $sumAttrPrice = $this->attributePrice($SumAttributeProcessFactory);
                    $calculations = $this->UserCalc->customGetByList($aggregateCalculations);

                    foreach ($calculations as $calculation) {
                        $volumeRatio = $SumAttributeProcessFactory->getVolume() / $calculation['volume'];
                        $newAttributePrice = 0;

                        foreach ($sumAttrPrice['priceComponents'] as $priceComponent) {
                            $newAttributePrice += $priceComponent['partialPrice'] / $volumeRatio;
                        }

                        $calcPrice = $this->BasePrice->get('ID', $calculation['calcPriceID']);
                        $calculationPriceWithoutAttribute = $calcPrice['price'] - round($aggregateAttributePrices[$calculation['ID']], 0);
                        $newCalculatePrice = $calculationPriceWithoutAttribute + $newAttributePrice;

                        if ($this->updatePrice($calculation['priceID'], $calculation['ID'], $newCalculatePrice)) {
                            $updated++;
                        }
                    }
                }
            }
        }

        return $updated > 0;
    }

    private function updatePrice($priceID, $calculationID, $newValue)
    {
        $price = $this->BasePrice->get('ID', $priceID);

        if ($price['price'] <= $newValue) {
            return false;
        }

        $calculation = $this->UserCalc->customGet($calculationID);

        if (!$calculation['beforeReCountPriceID']) {
            $newPriceID = $this->BasePrice->copy($priceID);
            $this->UserCalc->update($calculation['ID'], 'beforeReCountPriceID', $priceID);
            $this->UserCalc->update($calculation['ID'], 'priceID', $newPriceID);
        } else {
            $newPriceID = $priceID;
        }

        $tax = $this->Tax->customGet($price['taxID']);
        $taxValue = 1 + (intval($tax['value']) / 100);
        $grossPrice = $newValue * $taxValue;
        $saved = 0;

        if ($this->BasePrice->update($newPriceID, 'price', $newValue)) {
            $saved++;
        }
        if ($this->BasePrice->update($newPriceID, 'grossPrice', $grossPrice)) {
            $saved++;
        }

        return $saved > 0;
    }

    private function addToAttributeFactories($AttributeProcessFactory, $price)
    {
        if ($price['finalPrice'] === null || $price['finalPrice'] <= 0) {
            return;
        }

        $attributeFactories = $this->getAttributeFactories();
        $workspace = $AttributeProcessFactory->getWorkspace();
        $key = $AttributeProcessFactory->getOptionID() . '-' . $AttributeProcessFactory->getPrintTypeID() . '-' . $workspace['ID'];

        if (isset($attributeFactories[$key])) {
            $firstFactoryArray = current($attributeFactories[$key]);
            $firstFactory = $firstFactoryArray['factory'];

            if ($firstFactory->getPriceListID() !== $AttributeProcessFactory->getPriceListID()) {
                return;
            }

            $priceList = $this->CalculateStorage->getPriceList($firstFactory->getPriceListID());

            if (!$priceList['allowJoinProcess']) {
                return;
            }
        }

        $attributeFactories[$key][] = [
            'factory' => $AttributeProcessFactory,
            'regularPrice' => $price['finalPrice'],
            'priceComponents' => $price['priceComponents'],
            'calculationID' => $AttributeProcessFactory->getCalculateID()
        ];
        $this->setAttributeFactories($attributeFactories);
    }

    private function getPrintTypes($formatID, $volume)
    {
        $printTypes = $this->CalculateStorage->getPrintTypes($formatID);

        foreach ($printTypes as $key => $printType) {
            if (($printType['minVolume'] !== null && $volume < $printType['minVolume']) ||
                ($printType['maxVolume'] !== null && $volume > $printType['maxVolume'])) {
                unset($printTypes[$key]);
            }
        }

        return $printTypes;
    }

    private function getWorkspaces($workspaceID, $printTypeID)
    {
        if ($workspaceID) {
            $workspace = $this->CalculateStorage->getWorkspace($workspaceID);
            $workspace['workspaceID'] = $workspace['ID'];
            return [$workspace];
        } else {
            return $this->CalculateStorage->getWorkspacesCluster($printTypeID);
        }
    }

    private function getOptionsProperties($attributes, $pages, $doublePage)
    {
        $optionsProperties = [
            'oneSide' => null,
            'size' => null,
            'maxFolds' => null,
            'printRotated' => 0,
            'rollLength' => null
        ];

        foreach ($attributes as $attr) {
            $option = $this->CalculateStorage->getOption($attr['optID']);

            if ($option['oneSide'] == 1) {
                $optionsProperties['oneSide'] = true;
            }

            if (doubleval($option['sizePage']) > 0) {
                $optionsProperties['size'] += $this->calculateProductThickness($pages, $option['sizePage'], $doublePage);
            }

            if ($option['rollLength'] > 0) {
                $optionsProperties['rollLength'] = $option['rollLength'];
            }

            if (isset($option['printRotated']) && $option['printRotated'] == 1) {
                $optionsProperties['printRotated'] = 1;
            }

            if (isset($option['maxFolds']) && $option['maxFolds'] !== null) {
                $optionsProperties['maxFolds'] = $option['maxFolds'];
            }
        }

        return $optionsProperties;
    }

    private function calculateProductThickness($pages, $pageSize, $doublePage)
    {
        $pageSize = doubleval($pageSize);
        $sheets = $pages / 2;

        if ($doublePage) {
            $sheets /= 2;
        }

        return $sheets * $pageSize;
    }

    private function getAllSheets($workspace, $pages, $volume, $oneSide, $printRotated, $doublePage, $formatWidth, $formatHeight, $format)
    {
        $pages = $this->CalculateAdapter->getAmountPages($pages, $oneSide, $doublePage);
        $perSheet = null;

        switch ($workspace['type']) {
            case 3:
                $sheets = 1;
                break;
            case 2:
                $area = $this->CalculateAdapter->getAreaForRolled($pages, $volume);
                $usedHeight = $this->CalculateAdapter->getUsedHeight($area, $workspace['width'], $formatWidth, $formatHeight);
                $sheets = ceil($usedHeight / $workspace['height']);
                break;
            default:
                $areaPerSheetForStandardResult = $this->CalculateAdapter->getAreaPerSheetForStandard($workspace['width'], $workspace['height'], $formatWidth, $formatHeight, $format);
                $perSheet = $areaPerSheetForStandardResult['max'];

                if ($perSheet == 0) {
                    return null;
                }

                if (!$printRotated) {
                    $sheets = ceil($this->CalculateAdapter->getSheetsForStandard($pages, $perSheet, $volume));
                } else {
                    $sheets = ceil($this->CalculateAdapter->getSheetsForStandardPrintRotated($pages, $perSheet, $volume) * 2) / 2;
                }
                break;
        }

        return ['sheets' => $sheets, 'perSheet' => $perSheet];
    }

    private function getFormatRows($format)
    {
        return $format['rows'] > 1 ? intval($format['rows']) : 1;
    }

    private function getProjectSheets($workspace, $pages, $similarPages, $doublePage, $optionProperties, $formatWidth, $formatHeight, $format)
    {
        if ($similarPages) {
            return 1;
        }

        $sheetsInfo = $this->getAllSheets($workspace, $pages, 1, $optionProperties['oneSide'], $optionProperties['printRotated'], $doublePage, $formatWidth, $formatHeight, $format);
        return $sheetsInfo['sheets'];
    }

    private function getArea($volume, $rows, $maxRollLength, $setIncrease, $slope, $formatWidth, $formatHeight)
    {
        $volume = $this->CalculateAdapter->addSetIncreaseToVolume($volume, $setIncrease, $rows);
        $size = $this->CalculateAdapter->calculateSize($formatWidth, $formatHeight) * $volume;
        $sizeNet = $this->CalculateAdapter->calculateSizeNet($formatWidth, $formatHeight, $slope) * $volume;

        if ($maxRollLength !== null) {
            $length = $this->CalculateAdapter->getLengthForRoll($size, $formatWidth);
            $numberOfRolls = $this->CalculateAdapter->getNumberOfRolls($length, $maxRollLength);
            $rollSlipIncrease = $this->CalculateStorage->getIncrease('rollSlip', $numberOfRolls);
            $size = $this->CalculateAdapter->calculateSizeForRollPrint($size, $maxRollLength, $formatWidth, $rollSlipIncrease);
        }

        return ['size' => $size, 'sizeNet' => $sizeNet];
    }

    private function getPerimeter($volume, $formatWidth, $formatHeight)
    {
        $width = $formatWidth / 1000;
        $height = $formatHeight / 1000;
        $perimeter = ($width * 2 + $height * 2) * $volume;
        return $perimeter;
    }

    private function getCopiesOnAllSheets($volume, $pages, $oneSide, $doublePage)
    {
        $copiesOnAllSheets = $oneSide && $pages > 2 ? $pages : $pages / 2;
        if ($doublePage) {
            $copiesOnAllSheets /= 2;
        }
        return $copiesOnAllSheets * $volume;
    }

    private function getTotalArea($workspace, $volume, $maxRollLength, $setIncrease, $formatWidth, $formatHeight)
    {
        $volume = $this->CalculateAdapter->addSetIncreaseToVolumeTotal($volume, $setIncrease);
        $length = $this->CalculateAdapter->getLengthForTotalArea($formatWidth, $formatHeight, $workspace['width'], $volume);
        $length = $this->CalculateAdapter->addPaperHeightForTotalArea($length, $workspace);

        if ($maxRollLength !== null) {
            $numberOfRolls = $this->CalculateAdapter->getNumberOfRollsForTotalArea($length, $maxRollLength);
            $rollSlipIncrease = $this->CalculateStorage->getIncrease('rollSlip', $numberOfRolls);
            $length = $this->CalculateAdapter->addRollSlipIncrease($length, $rollSlipIncrease, $numberOfRolls);
        }

        return $this->CalculateAdapter->calculateTotalArea($length, $workspace);
    }

    private function getTotalSheetFolds($copiesOnSheet, $maxFolds)
    {
        $sheetCuts = 0;
        $folds = log($copiesOnSheet, 2);

        while ($maxFolds !== null && $folds > $maxFolds) {
            $folds--;
            $sheetCuts++;
        }

        $totalSheetFolds = $folds;
        if ($sheetCuts > 0) {
            $totalSheetFolds *= $sheetCuts * 2;
        }

        return $totalSheetFolds;
    }

    private function attributePrice($AttributeProcessFactory)
    {
        $AttributeProcessFactoryCopy = clone $AttributeProcessFactory;
        $workspace = $AttributeProcessFactoryCopy->getWorkspace();
        $workspaceID = $workspace['ID'];

        $valuesWithIncreases = $this->addIncreases(
            $AttributeProcessFactoryCopy->getSheets(),
            $AttributeProcessFactoryCopy->getVolume(),
            $AttributeProcessFactoryCopy->getSheetIncrease(),
            $AttributeProcessFactoryCopy->getSetIncrease(),
            $AttributeProcessFactoryCopy->getProjectSheet()
        );

        $AttributeProcessFactoryCopy->setSheets($valuesWithIncreases['sheets']);
        $AttributeProcessFactoryCopy->setVolume($valuesWithIncreases['volume']);
        $attribute = $this->CalculateStorage->getAttribute($AttributeProcessFactoryCopy->getAttributeID());

        $controllerID = $this->getControllerID(
            $attribute,
            $AttributeProcessFactoryCopy->getPriceListID(),
            $AttributeProcessFactoryCopy->getPrintTypeID(),
            $workspaceID
        );

        if (!$controllerID) {
            return false;
        }

        $this->PrintShopConfigIncrease->setAttrID($AttributeProcessFactoryCopy->getAttributeID());
        $this->PrintShopConfigIncrease->setOptID($AttributeProcessFactoryCopy->getOptionID());
        $this->PrintShopConfigIncrease->setControllerID($controllerID);

        $increases = $this->getAttributeIncreases(
            $AttributeProcessFactoryCopy->getSheets(),
            $AttributeProcessFactoryCopy->getProjectSheet()
        );
        $AttributeProcessFactoryCopy->setSheets($increases['sheets']);

        $finalPrice = 0;
        $this->PrintShopConfigDetailPrice->setAttrID($AttributeProcessFactoryCopy->getAttributeID());
        $this->PrintShopConfigDetailPrice->setOptID($AttributeProcessFactoryCopy->getOptionID());
        $this->PrintShopConfigDetailPrice->setControllerID($controllerID);

        if ($attribute['function'] == 'standard') {
            $this->PrintShopConfigDetailPrice->setControllerID($AttributeProcessFactoryCopy->getPriceListID());
        }

        $detailPrice = $this->CalculateStorage->getDetailPrice();

        if ($detailPrice['excluded']) {
            return null;
        }

        $priceComponents = [];
        $option = $this->CalculateStorage->getOption($AttributeProcessFactoryCopy->getOptionID());
        $weight = $attribute['type'] == ATTRIBUTE_TYPE_PAPER ? $this->getWeightOfPaper($option, $workspace, $AttributeProcessFactoryCopy->getSheets()) : false;
        $paperPrice = $this->getPaperPrice($attribute, $AttributeProcessFactoryCopy->getOptionID(), $weight, $AttributeProcessFactoryCopy->isExpense());

        if ($paperPrice) {
            $priceComponents[] = [
                'range' => $weight,
                'amount' => 1,
                'percentage' => false,
                'function' => 'paper',
                'partialPrice' => round($paperPrice, 0)
            ];
            $finalPrice += $paperPrice;
        }

        $discountGroups = $this->getDiscountGroups($this->getUserID());
        $discountPriceTypes = $discountGroups ? $this->CalculateStorage->getDiscountPriceTypes() : null;

        if ($discountPriceTypes) {
            foreach ($discountPriceTypes as &$discountPriceType) {
                $discountPriceType['discounted'] = true;
            }
            unset($discountPriceType);
        }

        $this->PrintShopConfigPrice->setAttrID($AttributeProcessFactoryCopy->getAttributeID());
        $this->PrintShopConfigPrice->setOptID($AttributeProcessFactoryCopy->getOptionID());
        $this->PrintShopConfigPrice->setControllerID($controllerID);
        $priceTypes = $discountPriceTypes && !$this->isCountBasePrice() ? $discountPriceTypes : $this->CalculateStorage->getPriceTypes();
        $this->setPriceTypes($priceTypes);

        $percentagePrice = [];

        foreach ($priceTypes as $priceType) {
            $priceComponent = $this->prepareValuesForPrice($priceType['function'], $AttributeProcessFactoryCopy);
            $priceComponent['function'] = $priceType['function'];

            if ($AttributeProcessFactoryCopy->isExpense()) {
                $price = $this->searchMatchingExpense($priceComponent['range'], $priceType);
                if (!$priceComponent['percentage']) {
                    $finalPrice += $price['expense'] * $priceComponent['amount'];
                } else {
                    $percentagePrice[] = [
                        'value' => $price['expense'],
                        'type' => $priceComponent['percentageType']
                    ];
                }
            } else {
                $price = $this->searchMatchingPrice($priceComponent['range'], $priceComponent['volume'], $priceType);
                if (!$priceComponent['percentage']) {
                    $partialPrice = $price['value'] * $priceComponent['amount'];
                    $priceComponent['partialPrice'] = $partialPrice;
                    $finalPrice += $partialPrice;
                } else {
                    $percentagePrice[] = [
                        'value' => $price['value'],
                        'type' => $priceComponent['percentageType']
                    ];
                }
                $priceComponents[] = $priceComponent;
            }
        }

        if ($AttributeProcessFactoryCopy->isExpense()) {
            $finalPrice += $detailPrice['startUp'] !== null ? $detailPrice['startUp'] : 0;
        } else {
            if ($detailPrice['basePrice'] !== null) {
                $finalPrice += $detailPrice['basePrice'];
                $priceComponents[] = [
                    'function' => 'basePrice',
                    'partialPrice' => $detailPrice['basePrice']
                ];
            }
            if ($detailPrice['minPrice'] !== null && $detailPrice['minPrice'] > $finalPrice) {
                $finalPrice = $detailPrice['minPrice'];
                $priceComponents = [['function' => 'basePrice', 'partialPrice' => $detailPrice['minPrice']]];
            }
        }

        foreach ($percentagePrice as $each) {
            if ($each['type'] == 1) {
                $finalPrice *= 1 + (doubleval($each['value']) / 100);
            } elseif ($each['type'] == 2) {
                $finalPrice *= doubleval($each['value']) / 100;
            }
        }

        return [
            'finalPrice' => $finalPrice,
            'priceComponents' => $priceComponents
        ];
    }

    private function prepareValuesForPrice($priceTypeFunction, $AttributeProcessFactory)
    {
        $result = ['percentage' => false];

        $totalFolds = $AttributeProcessFactory->getSheets() * $AttributeProcessFactory->getTotalSheetFolds();
        $lengthOfSides = $this->getLengthOfSides($AttributeProcessFactory->getFormatWidth(), $AttributeProcessFactory->getFormatHeight());
        $totalSheetsArea = $this->getTotalSheetsArea($AttributeProcessFactory->getWorkspace(), $AttributeProcessFactory->getSheets());
        $area = $AttributeProcessFactory->getArea();

        switch ($priceTypeFunction) {
            case 'sheet':
                return $this->calculateSheet($AttributeProcessFactory->getSheets(), $AttributeProcessFactory->getVolume(), $AttributeProcessFactory->getAttributePages());
            case 'set':
                return $this->calculateSet($AttributeProcessFactory->getVolume(), $AttributeProcessFactory->getAttributePages());
            case 'projectSheets':
                return ['range' => $AttributeProcessFactory->getProjectSheet(), 'amount' => $AttributeProcessFactory->getProjectSheet()];
            case 'squareMeter':
            case 'squareMeter_cm':
                $size = $area['size'];
                return ['range' => $size, 'amount' => $priceTypeFunction === 'squareMeter_cm' ? $size * 10000 : $size];
            case 'perimeter':
            case 'perimeter_cm':
                $perimeter = $AttributeProcessFactory->getPerimeter() * ($AttributeProcessFactory->getAttributePages() > 1 ? $AttributeProcessFactory->getAttributePages() : 1);
                return ['range' => $perimeter, 'amount' => $priceTypeFunction === 'perimeter_cm' ? $perimeter * 100 : $perimeter];
            case 'allSheetsRangeVolume':
                return ['range' => $AttributeProcessFactory->getVolume(), 'amount' => $AttributeProcessFactory->getSheets()];
            case 'allPages':
            case 'allPagesRangeVolume':
                $amount = $AttributeProcessFactory->getAttributePages() * $AttributeProcessFactory->getVolume();
                return ['range' => $priceTypeFunction === 'allPagesRangeVolume' ? $AttributeProcessFactory->getVolume() : $amount, 'amount' => $amount];
            case 'setRangeSheet':
                return ['range' => $AttributeProcessFactory->getSheets(), 'amount' => $AttributeProcessFactory->getVolume()];
            case 'setRangeSize':
                return ['range' => $AttributeProcessFactory->getSize(), 'amount' => $AttributeProcessFactory->getVolume()];
            case 'setMultiplication':
                return ['range' => $AttributeProcessFactory->getVolume(), 'amount' => null, 'percentage' => true, 'percentageType' => 1];
            case 'longSide':
            case 'longSide_cm':
                $longSide = $lengthOfSides['longSide'] * ($AttributeProcessFactory->getAttributePages() > 1 ? $AttributeProcessFactory->getAttributePages() : 1);
                return ['range' => $longSide / 1000 * ($priceTypeFunction === 'longSide_cm' ? 100 : 1), 'amount' => $longSide / 1000 * $AttributeProcessFactory->getVolume() * ($priceTypeFunction === 'longSide_cm' ? 100 : 1)];
            case 'shortSide':
            case 'shortSide_cm':
                $shortSide = $lengthOfSides['shortSide'] * ($AttributeProcessFactory->getAttributePages() > 1 ? $AttributeProcessFactory->getAttributePages() : 1);
                return ['range' => $shortSide / 1000 * ($priceTypeFunction === 'shortSide_cm' ? 100 : 1), 'amount' => $shortSide / 1000 * $AttributeProcessFactory->getVolume() * ($priceTypeFunction === 'shortSide_cm' ? 100 : 1)];
            case 'allAreasLength':
            case 'allAreasLength_cm':
                $length = (($AttributeProcessFactory->getFormatWidth() * 2) + ($AttributeProcessFactory->getFormatHeight() * 2)) / 1000 * ceil($AttributeProcessFactory->getCopiesOnAllSheets());
                $length *= $AttributeProcessFactory->getAttributePages() > 1 ? $AttributeProcessFactory->getAttributePages() : 1;
                return ['range' => $length * ($priceTypeFunction === 'allAreasLength_cm' ? 100 : 1), 'amount' => $length * ($priceTypeFunction === 'allAreasLength_cm' ? 100 : 1)];
            case 'alluzytki':
                return $this->calculateAllCopiesOnAllSheets($AttributeProcessFactory->getCopiesOnAllSheets(), $AttributeProcessFactory->getAttributePages());
            case 'paintRangeVolume':
                return ['range' => $AttributeProcessFactory->getVolume(), 'amount' => 0]; // @TODO check file ink volume
            case 'setRangePages':
                return ['range' => $AttributeProcessFactory->getPages(), 'amount' => $AttributeProcessFactory->getVolume()];
            case 'totalArea':
            case 'totalArea_cm':
                $totalArea = $AttributeProcessFactory->getTotalArea();
                return ['range' => $totalArea, 'amount' => $totalArea * ($priceTypeFunction === 'totalArea_cm' ? 10000 : 1)];
            case 'folds':
                return ['range' => $totalFolds, 'amount' => $totalFolds];
            case 'totalSheetsArea':
            case 'totalSheetsArea_cm':
                return ['range' => $totalSheetsArea, 'amount' => $totalSheetsArea * ($priceTypeFunction === 'totalSheetsArea_cm' ? 10000 : 1)];
            case 'totalSheetsAreaRangeSheets':
            case 'totalSheetsAreaRangeSheets_cm':
                return ['range' => $AttributeProcessFactory->getSheets(), 'amount' => $totalSheetsArea * ($priceTypeFunction === 'totalSheetsAreaRangeSheets_cm' ? 10000 : 1)];
            case 'collectingFolds':
                $maxFolds = $AttributeProcessFactory->getMaxFolds();
                $range = $maxFolds == 3 ? intval($AttributeProcessFactory->getSheets()) : ($maxFolds == 2 ? intval($AttributeProcessFactory->getSheets()) * 2 : intval($AttributeProcessFactory->getSheets()) * 4);
                return ['range' => $range, 'amount' => $range];
            case 'lengthForWidth':
            case 'lengthForWidth_cm':
                $formatHeight = $AttributeProcessFactory->getFormatHeight();
                $length = $formatHeight * ($AttributeProcessFactory->getAttributePages() > 1 ? $AttributeProcessFactory->getAttributePages() : 1) / 1000;
                return ['range' => $length * ($priceTypeFunction === 'lengthForWidth_cm' ? 100 : 1), 'amount' => $length * $AttributeProcessFactory->getVolume() * ($priceTypeFunction === 'lengthForWidth_cm' ? 100 : 1)];
            case 'lengthForHeight':
            case 'lengthForHeight_cm':
                $formatHeight = $AttributeProcessFactory->getFormatHeight();
                $length = $formatHeight * ($AttributeProcessFactory->getAttributePages() > 1 ? $AttributeProcessFactory->getAttributePages() : 1) / 1000;
                return ['range' => $length * ($priceTypeFunction === 'lengthForHeight_cm' ? 100 : 1), 'amount' => $length * $AttributeProcessFactory->getVolume() * ($priceTypeFunction === 'lengthForHeight_cm' ? 100 : 1)];
            case 'squareMeterNet':
            case 'squareMeterNet_cm':
                $sizeNet = $area['sizeNet'];
                return ['range' => $sizeNet, 'amount' => $sizeNet * ($priceTypeFunction === 'squareMeterNet_cm' ? 10000 : 1)];
            case 'squareMetersForPages':
            case 'squareMetersForPages_cm':
                $squareForPages = $this->calculateSquareForPages($area, $AttributeProcessFactory->getPages());
                return ['range' => $squareForPages, 'amount' => $squareForPages * ($priceTypeFunction === 'squareMetersForPages_cm' ? 10000 : 1)];
            case 'setPercentage':
                return ['range' => $AttributeProcessFactory->getVolume(), 'amount' => null, 'percentage' => true, 'percentageType' => 2];
            case 'bundle':
                return $this->calculateBundle($AttributeProcessFactory->getVolume(), $AttributeProcessFactory->getAttributePages());
            case 'package':
                return $this->calculatePackage($AttributeProcessFactory->getAttributePages());
            case 'setVolumes':
                return $this->calculateSetVolumes($AttributeProcessFactory->getVolume());
            case 'allSheetsVolumes':
                return ['range' => $AttributeProcessFactory->getVolume(), 'amount' => 1];
            default:
                throw new Exception('Price type function not set');
        }
    }

    private function calculateAllPages($pages, $volume, $attributeAmount = null)
    {
        return ['range' => $attributeAmount !== null ? $attributeAmount * $volume : $pages * $volume, 'amount' => $attributeAmount !== null ? $attributeAmount * $volume : $pages * $volume];
    }

    private function calculateAllPagesRangeVolume($pages, $volume, $attributeAmount = null)
    {
        return ['range' => $volume, 'amount' => $attributeAmount !== null ? $attributeAmount * $volume : $pages * $volume];
    }

    private function calculateSheet($sheets, $volume, $attributeAmount = null)
    {
        return ['range' => $attributeAmount !== null ? $attributeAmount : $sheets, 'amount' => $attributeAmount !== null ? $volume * $attributeAmount : $sheets];
    }

    private function calculateSet($volume, $attributeAmount = null)
    {
        return ['range' => $attributeAmount !== null ? $volume * $attributeAmount : $volume, 'amount' => $attributeAmount !== null ? $volume * $attributeAmount : $volume];
    }

    private function calculateSquareForPages($area, $pages)
    {
        return $area['size'] * $pages;
    }

    private function calculateAllCopiesOnAllSheets($uzytki, $attributeAmount = null)
    {
        return ['range' => $uzytki, 'amount' => $attributeAmount ? $uzytki * $attributeAmount : $uzytki];
    }

    private function calculateBundle($volume, $attributeAmount)
    {
        $bundleValue = $attributeAmount > 0 ? ceil($volume / $attributeAmount) : 1;
        return ['range' => $bundleValue, 'amount' => $bundleValue];
    }

    private function calculatePackage($attributeAmount)
    {
        return ['range' => $attributeAmount > 0 ? $attributeAmount : 1, 'amount' => $attributeAmount > 0 ? $attributeAmount : 1];
    }

    private function calculateSetVolumes($volume)
    {
        return ['range' => $volume, 'amount' => 1];
    }

    private function searchMatchingPrice($range, $volume, $priceType)
    {
        $price = $priceType['discounted'] ? $this->PrintShopConfigDiscountPrice->customGet($priceType['priceType'], $range) : $this->PrintShopConfigPrice->customGet($priceType['priceType'], $range);

        if (in_array($priceType['function'], ['setVolumes', 'allSheetsVolumes']) && isset($price['lastRangePrice']) && $price['amount'] < $volume) {
            $price['value'] = $volume * $price['lastRangePrice'];
        }

        return $price;
    }

    private function searchMatchingExpense($range, $priceType)
    {
        return $priceType['discounted'] ? $this->PrintShopConfigDiscountPrice->getExpense($priceType['priceType'], $range) : $this->PrintShopConfigPrice->getExpense($priceType['priceType'], $range);
    }

    private function addIncreases($sheets, $volume, $sheetIncrease, $setIncrease, $projectSheets)
    {
        $sheets += intval($sheetIncrease);
        $volume += intval($setIncrease);
        $sheets += intval($setIncrease) * $projectSheets;

        return compact('volume', 'sheets');
    }

    private function getLengthOfSides($formatWidth, $formatHeight)
    {
        $longSide = max($formatWidth, $formatHeight);
        $shortSide = min($formatWidth, $formatHeight);

        return compact('longSide', 'shortSide');
    }

    private function getControllerID($attribute, $priceListID, $printTypeID, $workspaceID)
    {
        switch ($attribute['function']) {
            case 'standard':
                return $priceListID;
            case 'print':
                return $printTypeID;
            case 'paper':
                return $workspaceID;
            default:
                $this->debug('Undefined attrType function');
                return false;
        }
    }

    private function getAttributeIncreases($sheets, $projectSheets)
    {
        $increases = $this->CalculateStorage->getConfigIncreaseCluster();

        foreach ($increases as $increase) {
            if ($increase['function'] == 'sheet') {
                $range = $sheets;
                $amount = 1;
            } elseif ($increase['function'] == 'sheetForProjectSheet') {
                $range = ceil($projectSheets);
                $amount = ceil($projectSheets);
            } else {
                continue;
            }

            $increase = $this->CalculateStorage->getConfigIncrease($increase['increaseType'], $range);
            $sheets += floatval($increase['value']) * $amount;
        }

        return compact('sheets');
    }

    private function getTotalSheetsArea($workspace, $sheets)
    {
        return ($workspace['paperWidth'] / 1000) * ($workspace['paperHeight'] / 1000) * $sheets;
    }

    private function getPaperPrice($attribute, $optionID, $weight, $expense = false)
    {
        if (!$weight || $attribute['function'] !== 'paper') {
            return false;
        }

        $this->PrintShopConfigPaperPrice->setOptID($optionID);
        $connect = $this->CalculateStorage->getConnectOption($optionID);

        if ($expense) {
            $result = !$connect ? $this->CalculateStorage->getPaperPrice('expense', $weight) : $this->CalculateStorage->getPaperPrice('connectExpense', $weight, $connect['connectOptionID']);
            return $result['expense'] * $weight;
        } else {
            $result = !$connect ? $this->CalculateStorage->getPaperPrice('price', $weight) : $this->CalculateStorage->getPaperPrice('connectPrice', $weight, $connect['connectOptionID']);
            return $result['value'] * $weight;
        }
    }

    private function getWeightOfPaper($option, $workspace, $sheets)
    {
        $sheetArea = $workspace['paperWidth'] * $workspace['paperHeight'] / 1000000;
        return ($option['weight'] / 1000) * $sheetArea * $sheets;
    }

    private function getDiscountGroups($userID)
    {
        return $this->CalculateStorage->getUserDiscountGroups($userID);
    }
}
