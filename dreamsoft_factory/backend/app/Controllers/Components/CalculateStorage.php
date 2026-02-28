<?php

namespace DreamSoft\Controllers\Components;

use DreamSoft\Models\Discount\UserDiscountGroup;
use DreamSoft\Models\PrintShop\PrintShopFormatPrintType;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttribute;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttributeRange;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigConnectOption;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigConnectPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigDetailPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigDiscountPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigIncrease;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOption;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPaperPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPriceList;
use DreamSoft\Models\PrintShopProduct\PrintShopFormat;
use DreamSoft\Models\PrintShopProduct\PrintShopIncrease;
use DreamSoft\Models\PrintShopProduct\PrintShopPage;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigWorkspace;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrintTypeWorkspace;
use DreamSoft\Models\PrintShopProduct\PrintShopPrintTypeWorkspace;
use DreamSoft\Core\Component;
use DreamSoft\Models\Upload\UploadFile;

class CalculateStorage extends Component
{
    public $useModels = [
        'PrintShopConfigAttribute',
        'PrintShopConfigAttributeRange',
        'PrintShopConfigOption',
        'PrintShopFormatPrintType',
        'PrintShopConfigPriceList',
        'PrintShopConfigPrice',
        'PrintShopConfigDetailPrice',
        'PrintShopConfigIncrease',
        'PrintShopConfigConnectOption',
        'PrintShopConfigPaperPrice',
        'PrintShopConfigConnectPrice',
        'PrintShopConfigDiscountPrice',
    ];

    protected $PrintShopType;
    protected $PrintShopPage;
    protected $PrintShopConfigAttribute;
    protected $PrintShopConfigAttributeRange;
    protected $PrintShopConfigOption;
    protected $PrintShopFormatPrintType;
    protected $PrintShopFormat;
    protected $PrintShopConfigPriceList;
    protected $PrintShopConfigWorkspace;
    protected $PrintShopConfigPrintTypeWorkspace;
    protected $PrintShopConfigDetailPrice;
    protected $PrintShopIncrease;
    protected $PrintShopConfigIncrease;
    protected $PrintShopConfigConnectOption;
    protected $PrintShopConfigPaperPrice;
    protected $PrintShopConfigConnectPrice;
    protected $PrintShopConfigDiscountPrice;
    protected $PrintShopConfigPrice;
    protected $UploadFile;
    protected $UserDiscountGroup;
    protected $PrintShopPrintTypeWorkspace;

    private $types = [];
    private $formats = [];
    private $options = [];
    private $attributes = [];
    private $workspaces = [];
    private $pagesRanges = [];
    private $attributesCluster = [];
    private $optionsCluster = [];
    private $attributeRangesCluster = [];
    private $doublePages = [];
    private $similarPages = [];
    private $printTypesCluster = [];
    private $priceListCluster = [];
    private $iconsCluster = [];
    private $workspacesCluster = [];
    private $printRotatedEntities = [];
    private $increases = [];
    private $configIncreases = [];
    private $configIncreasesCluster = [];
    private $connectOptions = [];
    private $paperPrices = [];
    private $detailPrices = [];
    private $userDiscountGroupsCluster = [];
    private $discountPriceTypesCluster = [];
    private $priceTypesCluster = [];
    private $priceLists = [];
    private $printTypeWorkspaceCluster = [];

    public function __construct()
    {
        parent::__construct();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->PrintShopPage = PrintShopPage::getInstance();
        $this->PrintShopConfigAttribute = PrintShopConfigAttribute::getInstance();
        $this->PrintShopConfigAttributeRange = PrintShopConfigAttributeRange::getInstance();
        $this->PrintShopConfigOption = PrintShopConfigOption::getInstance();
        $this->PrintShopFormatPrintType = PrintShopFormatPrintType::getInstance();
        $this->PrintShopFormat = PrintShopFormat::getInstance();
        $this->PrintShopConfigPriceList = PrintShopConfigPriceList::getInstance();
        $this->PrintShopConfigPrice = PrintShopConfigPrice::getInstance();
        $this->PrintShopConfigWorkspace = PrintShopConfigWorkspace::getInstance();
        $this->PrintShopConfigPrintTypeWorkspace = PrintShopConfigPrintTypeWorkspace::getInstance();
        $this->PrintShopConfigDetailPrice = PrintShopConfigDetailPrice::getInstance();
        $this->PrintShopIncrease = PrintShopIncrease::getInstance();
        $this->PrintShopConfigIncrease = PrintShopConfigIncrease::getInstance();
        $this->PrintShopConfigConnectOption = PrintShopConfigConnectOption::getInstance();
        $this->PrintShopConfigPaperPrice = PrintShopConfigPaperPrice::getInstance();
        $this->PrintShopConfigConnectPrice = PrintShopConfigConnectPrice::getInstance();
        $this->UploadFile = UploadFile::getInstance();
        $this->UserDiscountGroup = UserDiscountGroup::getInstance();
        $this->PrintShopConfigDiscountPrice = PrintShopConfigDiscountPrice::getInstance();
        $this->PrintShopPrintTypeWorkspace = PrintShopPrintTypeWorkspace::getInstance();
    }

    public function getType($typeID)
    {
        if (isset($this->types[$typeID])) {
            return $this->types[$typeID];
        } else {
            $type = $this->PrintShopType->get('ID', $typeID);
            if ($type) {
                $this->types[$typeID] = $type;
                return $type;
            } else {
                $this->debug('Type Not found!', $typeID);
                return false;
            }
        }
    }

    public function getFormat($formatID, $product)
    {
        if (isset($this->formats[$formatID])) {
            $format = $this->formats[$formatID];
        } else {
            $format = $this->PrintShopFormat->customGet($formatID);
            if ($format) {
                $this->formats[$formatID] = $format;
            } else {
                $this->debug('Format Not found!', $formatID);
                return false;
            }
        }
        if ($format['custom']) {
            if (!$product['width'] || !$product['height']) {
                if ($product['formatWidth']) {
                    $format['width'] = $product['formatWidth'];
                    $format['height'] = $product['formatHeight'];
                }
            } else {
                $format['width'] = $product['width'];
                $format['height'] = $product['height'];
            }
        }
        return $format;
    }

    public function getPriceList($priceListID)
    {
        if (isset($this->priceLists[$priceListID])) {
            return $this->priceLists[$priceListID];
        } else {
            $priceList = $this->PrintShopConfigPriceList->get('ID', $priceListID);
            if ($priceList) {
                $this->priceLists[$priceListID] = $priceList;
                return $priceList;
            } else {
                $this->debug('Price list Not found!', $priceListID);
                return false;
            }
        }
    }

    public function getOption($optionID)
    {
        if (isset($this->options[$optionID])) {
            return $this->options[$optionID];
        } else {
            $option = $this->PrintShopConfigOption->customGet($optionID);
            if ($option) {
                $this->options[$optionID] = $option;
                return $option;
            } else {
                $this->debug('Option Not found!', $optionID);
                return false;
            }
        }
    }

    public function getAttribute($attributeID)
    {
        if (isset($this->attributes[$attributeID])) {
            return $this->attributes[$attributeID];
        } else {
            $attribute = $this->PrintShopConfigAttribute->customGet($attributeID);
            if ($attribute) {
                $this->attributes[$attributeID] = $attribute;
                return $attribute;
            } else {
                $this->debug('Attribute Not found!', $attributeID);
                return false;
            }
        }
    }

    public function setOptionsByList($aggregateOptions)
    {
        if (!$aggregateOptions) {
            return false;
        }

        $filteredOptions = array_filter($aggregateOptions, function ($optionID) {
            return !isset($this->options[$optionID]);
        });

        $options = $this->PrintShopConfigOption->customGetByList($filteredOptions);
        if (!$options) {
            return false;
        }

        foreach ($options as $option) {
            $this->options[$option['ID']] = $option;
        }

        return true;
    }

    public function getPagesRange($groupID, $typeID)
    {
        $key = "$groupID $typeID";

        if (isset($this->pagesRanges[$key])) {
            return $this->pagesRanges[$key];
        } else {
            $pageRange = $this->PrintShopPage->getPagesRange($groupID, $typeID);
            if ($pageRange) {
                $this->pagesRanges[$key] = $pageRange;
                return $pageRange;
            } else {
                return false;
            }
        }
    }

    public function getAttributesCluster($aggregateAttributes)
    {
        $key = md5(json_encode($aggregateAttributes));

        if (isset($this->attributesCluster[$key])) {
            return $this->attributesCluster[$key];
        } else {
            $attributes = $this->PrintShopConfigAttribute->getByList($aggregateAttributes);
            if ($attributes) {
                $this->attributesCluster[$key] = $attributes;
                return $attributes;
            } else {
                return false;
            }
        }
    }

    public function getTotalWeight($attributes, $sheetsArea, $volume, $perimeter, $netPerimeter, $format, $controllerID)
    {
        $totalWeight = 0;
        foreach ($attributes as $attr) {
            $attribute = $this->getAttribute($attr['attrID']);
            $activeOption = $this->getOption($attr['optID']);
            $this->PrintShopConfigPrice->setAttrID($attr['attrID']);
            $this->PrintShopConfigPrice->setOptID($attr['optID']);
            $this->PrintShopConfigPrice->setControllerID($controllerID);

            if ($attribute['type'] == 3 && $activeOption['weight'] !== null) {
                $totalWeight += round($sheetsArea * $activeOption['weight'] / 1000, 2);
            }
            if ($activeOption['itemWeight'] !== null) {
                $totalWeight += round($volume * $activeOption['itemWeight'] / 1000, 2);
            }
            if ($activeOption['weightPerMeter']) {
                $totalWeight += $this->getWeightPerMeter(
                    $this->PrintShopConfigPrice->getUsingPriceTypes(), 
                    $perimeter, 
                    $activeOption['weightPerMeter'] / 1000, 
                    $netPerimeter, 
                    $format['width'] - ($format['slope'] * 2), 
                    $format['height'] - ($format['slope'] * 2), 
                    max($format['width'], $format['height']), 
                    min($format['width'], $format['height']), 
                    $volume
                );
            }
        }
        return $totalWeight;
    }

    public function getAttributeRangesCluster($aggregateRange)
    {
        $key = md5(json_encode($aggregateRange));

        if (isset($this->attributeRangesCluster[$key])) {
            return $this->attributeRangesCluster[$key];
        } else {
            $attributeRanges = $this->PrintShopConfigAttributeRange->getByList($aggregateRange);
            if ($attributeRanges) {
                $this->attributeRangesCluster[$key] = $attributeRanges;
                return $attributeRanges;
            } else {
                return false;
            }
        }
    }

    public function getDoublePage($groupID, $typeID)
    {
        $key = "$groupID $typeID";

        if (isset($this->doublePages[$key])) {
            return $this->doublePages[$key];
        } else {
            $doublePages = $this->PrintShopPage->getDoublePage($groupID, $typeID);
            if ($doublePages) {
                $this->doublePages[$key] = $doublePages;
                return $doublePages;
            } else {
                return false;
            }
        }
    }

    public function getSimilarPages($groupID, $typeID)
    {
        $key = "$groupID $typeID";

        if (isset($this->similarPages[$key])) {
            return $this->similarPages[$key];
        } else {
            $similarPages = $this->PrintShopPage->getPagesSimilar($groupID, $typeID);
            if ($similarPages) {
                $this->similarPages[$key] = $similarPages;
                return $similarPages;
            } else {
                return false;
            }
        }
    }

    public function getOptionsCluster($aggregateOptions)
    {
        $key = md5(json_encode($aggregateOptions));

        if (isset($this->optionsCluster[$key])) {
            return $this->optionsCluster[$key];
        } else {
            $options = $this->PrintShopConfigOption->customGetByList($aggregateOptions);
            if ($options) {
                $this->optionsCluster[$key] = $options;
                return $options;
            } else {
                return false;
            }
        }
    }

    public function getPrintTypes($formatID)
    {
        if (isset($this->printTypesCluster[$formatID])) {
            return $this->printTypesCluster[$formatID];
        } else {
            $printTypes = $this->PrintShopFormatPrintType->getByFormatID($formatID);
            if ($printTypes) {
                $this->printTypesCluster[$formatID] = $printTypes;
                return $printTypes;
            } else {
                return false;
            }
        }
    }

    public function getPriceListCluster($aggregatePriceLists)
    {
        $key = md5(json_encode($aggregatePriceLists));

        if (isset($this->priceListCluster[$key])) {
            return $this->priceListCluster[$key];
        } else {
            $priceLists = $this->PrintShopConfigPriceList->getByList($aggregatePriceLists);
            if ($priceLists) {
                $this->priceListCluster[$key] = $priceLists;
                return $priceLists;
            } else {
                return false;
            }
        }
    }

    public function getIconsCluster($aggregateIcons)
    {
        $key = md5(json_encode($aggregateIcons));

        if (isset($this->iconsCluster[$key])) {
            return $this->iconsCluster[$key];
        } else {
            $icons = $this->UploadFile->getFileByList($aggregateIcons);
            if ($icons) {
                $this->iconsCluster[$key] = $icons;
                return $icons;
            } else {
                return false;
            }
        }
    }

    public function getWorkspace($workspaceID)
    {
        if (isset($this->workspaces[$workspaceID])) {
            return $this->workspaces[$workspaceID];
        } else {
            $workspace = $this->PrintShopConfigWorkspace->get('ID', $workspaceID);
            if ($workspace) {
                $this->workspaces[$workspaceID] = $workspace;
                return $workspace;
            } else {
                $this->debug('Workspace Not found!', $workspaceID);
                return false;
            }
        }
    }

    public function setWorkSpaceByList($aggregateWorkspaces)
    {
        if (!$aggregateWorkspaces) {
            return false;
        }

        $filteredWorkspaces = array_filter($aggregateWorkspaces, function ($workspaceID) {
            return !isset($this->workspaces[$workspaceID]);
        });

        $workspaces = $this->PrintShopConfigWorkspace->getByList($filteredWorkspaces);
        if (!$workspaces) {
            return false;
        }

        foreach ($workspaces as $workspace) {
            $this->workspaces[$workspace['ID']] = $workspace;
        }

        return true;
    }

    public function getWorkspacesCluster($printTypeID)
    {
        if (isset($this->workspacesCluster[$printTypeID])) {
            return $this->workspacesCluster[$printTypeID];
        } else {
            $workspaces = $this->PrintShopConfigPrintTypeWorkspace->getByPrintTypeID($printTypeID);
            if ($workspaces) {
                $this->workspacesCluster[$printTypeID] = $workspaces;
                return $workspaces;
            } else {
                return false;
            }
        }
    }

    public function getPrintRotated($printTypeID, $optionsArray)
    {
        $key = "$printTypeID-" . md5(json_encode($optionsArray));

        if (isset($this->printRotatedEntities[$key])) {
            return $this->printRotatedEntities[$key];
        } else {
            $printRotated = $this->PrintShopConfigDetailPrice->getControllerPrintRotated($printTypeID, $optionsArray) &&
                !$this->PrintShopConfigOption->getPrintRotated($printTypeID, $optionsArray);
            if ($printRotated) {
                $this->printRotatedEntities[$key] = $printRotated;
                return $printRotated;
            } else {
                return false;
            }
        }
    }

    public function getIncrease($type, $amount, $formatID = null)
    {
        if (empty($this->increases)) {
            foreach ($this->PrintShopIncrease->getAll() as $row) {
                $key = "$row[type]-$row[amount]-$row[formatID]";
                $this->increases[$key] = $row;
            }
        }
        $key = "$type-$amount-$formatID";
        return $this->increases[$key] ?? false;
    }

    public function getConfigIncreaseCluster()
    {
        $controllerID = $this->PrintShopConfigIncrease->getControllerID();
        $attributeID = $this->PrintShopConfigIncrease->getAttrID();
        $optionID = $this->PrintShopConfigIncrease->getOptID();
        $key = "$controllerID-$attributeID-$optionID";

        if (isset($this->configIncreasesCluster[$key])) {
            return $this->configIncreasesCluster[$key];
        } else {
            $increases = $this->PrintShopConfigIncrease->getUsingIncreaseTypes();
            if ($increases) {
                $this->configIncreasesCluster[$key] = $increases;
                return $increases;
            } else {
                return false;
            }
        }
    }

    public function getConfigIncrease($increaseType, $amount)
    {
        $controllerID = $this->PrintShopConfigIncrease->getControllerID();
        $optionID = $this->PrintShopConfigIncrease->getOptID();
        $key = "$controllerID-$optionID-$increaseType-$amount";

        if (isset($this->configIncreases[$key])) {
            return $this->configIncreases[$key];
        } else {
            $increase = $this->PrintShopConfigIncrease->customGet($increaseType, $amount);
            if ($increase) {
                $this->configIncreases[$key] = $increase;
                return $increase;
            } else {
                return false;
            }
        }
    }

    public function getRelatedConfigIncreases($groupID, $typeID, $attr, $printTypeID, $workspace, $pricelistID, $attributesInfo)
    {
        $related = $this->PrintShopConfigIncrease->getRelatedIncreases($groupID, $typeID, $attr, $printTypeID, $workspace, $pricelistID, $attributesInfo);
        return $related && count($related) > 0 ? $related : false;
    }

    public function getConnectOption($optionID)
    {
        if (isset($this->connectOptions[$optionID])) {
            return $this->connectOptions[$optionID];
        } else {
            $connectOption = $this->PrintShopConfigConnectOption->get('optionID', $optionID);
            if ($connectOption) {
                $this->connectOptions[$optionID] = $connectOption;
                return $connectOption;
            } else {
                return false;
            }
        }
    }

    public function getPaperPrice($type, $weight, $connectOptionID = null)
    {
        $optionID = $this->PrintShopConfigPaperPrice->getOptID();
        $key = $connectOptionID ? "$type-" . md5($weight) . "-$connectOptionID" : "$type-" . md5($weight) . "-$optionID";

        if (isset($this->paperPrices[$key])) {
            return $this->paperPrices[$key];
        } else {
            switch ($type) {
                case 'expense':
                    $paperPrice = $this->PrintShopConfigPaperPrice->getExpenseFromWeight($weight);
                    break;
                case 'connectExpense':
                    $paperPrice = $this->PrintShopConfigConnectPrice->getExpenseFromWeight($connectOptionID, $weight);
                    break;
                case 'price':
                    $paperPrice = $this->PrintShopConfigPaperPrice->getPriceFromWeight($weight);
                    break;
                case 'connectPrice':
                    $paperPrice = $this->PrintShopConfigConnectPrice->getPriceFromWeight($connectOptionID, $weight);
                    break;
                default:
                    $paperPrice = false;
                    break;
            }

            if ($paperPrice) {
                $this->paperPrices[$key] = $paperPrice;
                return $paperPrice;
            } else {
                return false;
            }
        }
    }

    public function getDetailPrice()
    {
        $attributeID = $this->PrintShopConfigDetailPrice->getAttrID();
        $optionID = $this->PrintShopConfigDetailPrice->getOptID();
        $controllerID = $this->PrintShopConfigDetailPrice->getControllerID();
        $key = "$attributeID-$optionID";
        if ($controllerID) {
            $key .= "-$controllerID";
        }

        if (isset($this->detailPrices[$key])) {
            return $this->detailPrices[$key];
        } else {
            $detailPrice = $this->PrintShopConfigDetailPrice->customGet();
            if ($detailPrice) {
                $this->detailPrices[$key] = $detailPrice;
                return $detailPrice;
            } else {
                return false;
            }
        }
    }

    public function getUserDiscountGroups($userID)
    {
        $domainID = $this->UserDiscountGroup->getDomainID();
        $key = "$userID-$domainID";

        if (isset($this->userDiscountGroupsCluster[$key])) {
            return $this->userDiscountGroupsCluster[$key];
        } else {
            $discountGroups = $this->UserDiscountGroup->getByUser($userID);
            if ($discountGroups) {
                $this->userDiscountGroupsCluster[$key] = $discountGroups;
                return $discountGroups;
            } else {
                return false;
            }
        }
    }

    public function getDiscountPriceTypes()
    {
        $attributeID = $this->PrintShopConfigDiscountPrice->getAttrID();
        $optionID = $this->PrintShopConfigDiscountPrice->getOptID();
        $controllerID = $this->PrintShopConfigDiscountPrice->getControllerID();
        $key = "$attributeID-$optionID";
        if ($controllerID) {
            $key .= "-$controllerID";
        }

        $discountGroups = $this->PrintShopConfigDiscountPrice->getDiscountGroups();
        $aggregateDiscountGroup = array_column($discountGroups, 'discountGroupID');

        $key .= '-' . md5(json_encode($aggregateDiscountGroup));

        if (isset($this->discountPriceTypesCluster[$key])) {
            return $this->discountPriceTypesCluster[$key];
        } else {
            $discountPriceTypes = $this->PrintShopConfigDiscountPrice->getUsingPriceTypes();
            if ($discountPriceTypes) {
                $this->discountPriceTypesCluster[$key] = $discountPriceTypes;
                return $discountPriceTypes;
            } else {
                return false;
            }
        }
    }

    public function getPriceTypes()
    {
        $attributeID = $this->PrintShopConfigPrice->getAttrID();
        $optionID = $this->PrintShopConfigPrice->getOptID();
        $controllerID = $this->PrintShopConfigPrice->getControllerID();
        $key = "$attributeID-$optionID";
        if ($controllerID) {
            $key .= "-$controllerID";
        }

        if (isset($this->priceTypesCluster[$key])) {
            return $this->priceTypesCluster[$key];
        } else {
            $priceTypes = $this->PrintShopConfigPrice->getUsingPriceTypes();
            if ($priceTypes) {
                $this->priceTypesCluster[$key] = $priceTypes;
                return $priceTypes;
            } else {
                return false;
            }
        }
    }

    public function getPrintTypeWorkspaces($formatID, $aggregatePrintTypes)
    {
        $key = "$formatID-" . md5(json_encode($aggregatePrintTypes));

        if (isset($this->printTypeWorkspaceCluster[$key])) {
            return $this->printTypeWorkspaceCluster[$key];
        } else {
            $printTypeWorkspaces = $this->PrintShopPrintTypeWorkspace->getByAggregateData($aggregatePrintTypes, [$formatID]);
            if ($printTypeWorkspaces) {
                $this->printTypeWorkspaceCluster[$key] = $printTypeWorkspaces;
                return $printTypeWorkspaces;
            } else {
                return false;
            }
        }
    }

    public function getWeightPerMeter($priceTypes, $perimeter, $amountOfKilograms, $netPerimeter, $netWidth, $netHeight, $longSide, $shortSide, $volume)
    {
        $weightPerMeter = 0;
        foreach ($priceTypes as $priceType) {
            $amountOfMeters = 0;
            switch ($priceType['function']) {
                case 'perimeter':
                case 'perimeter_cm':
                    $amountOfMeters = $perimeter;
                    break;
                case 'net_perimeter':
                case 'net_perimeter_cm':
                    $amountOfMeters = $netPerimeter;
                    break;
                case 'lengthForWidth':
                case 'lengthForWidth_cm':
                    $amountOfMeters = $netWidth / 1000;
                    $weightPerMeter += $amountOfKilograms * $amountOfMeters * $volume;
                    break;
                case 'lengthForHeight':
                case 'lengthForHeight_cm':
                    $amountOfMeters = $netHeight / 1000;
                    $weightPerMeter += $amountOfKilograms * $amountOfMeters * $volume;
                    break;
                case 'longSide':
                case 'longSide_cm':
                    $amountOfMeters = $longSide / 1000;
                    $weightPerMeter += $amountOfKilograms * $amountOfMeters * $volume;
                    break;
                case 'shortSide':
                case 'shortSide_cm':
                    $amountOfMeters = $shortSide / 1000;
                    $weightPerMeter += $amountOfKilograms * $amountOfMeters * $volume;
                    break;
                default:
                    break;
            }
            if ($amountOfMeters) {
                $weightPerMeter += $amountOfKilograms * $amountOfMeters;
            }
        }
        return $weightPerMeter;
    }
}
