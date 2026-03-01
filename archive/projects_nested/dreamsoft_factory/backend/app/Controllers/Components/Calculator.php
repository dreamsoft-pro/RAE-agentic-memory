<?php

namespace DreamSoft\Controllers\Components;

use DreamSoft\Controllers\Components\CalculatorDevices;
use DreamSoft\Libs\Debugger;
use DreamSoft\Models\Discount\DiscountGroup;
use DreamSoft\Models\Discount\DiscountGroupLang;
use DreamSoft\Models\Discount\UserDiscountGroup;
use DreamSoft\Models\PrintShop\PrintShopRealizationTime;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttribute;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttributeNature;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttributeRange;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigConnectOption;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigConnectPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigDetailPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigDiscountPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigIncrease;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOption;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionDescription;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPaperPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPriceList;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigRealizationTime;
use DreamSoft\Models\PrintShopProduct\PrintShopFormat;
use DreamSoft\Models\PrintShopProduct\PrintShopIncrease;
use DreamSoft\Models\PrintShopProduct\PrintShopPage;
use DreamSoft\Models\PrintShopProduct\PrintShopStaticPrice;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeTax;
use DreamSoft\Models\PrintShopProduct\PrintShopVolume;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigWorkspace;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrintTypeWorkspace;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrintType;
use DreamSoft\Models\ProductionPath\Device;
use DreamSoft\Models\ProductionPath\DevicePrice;
use DreamSoft\Models\ProductionPath\DeviceSpeed;
use DreamSoft\Models\ProductionPath\OperationDevice;
use DreamSoft\Models\ProductionPath\OperationOption;
use DreamSoft\Models\Upload\UploadFile;
use DreamSoft\Libs\Auth;
use DreamSoft\Core\Component;
use DreamSoft\Models\User\UserOption;
use DreamSoft\Models\PrintShop\PrintShopFormatPrintType;
use DreamSoft\Models\Margin\Margin;
use DreamSoft\Models\Margin\MarginSupplier;
use Exception;

class Calculator extends Component
{
    public $useModels = array();
    protected $PrintShopFormatPrintType;
    protected $PrintShopConfigPrintTypeWorkspace;
    protected $PrintShopConfigWorkspace;
    protected $PrintShopFormat;
    protected $PrintShopConfigDetailPrice;
    protected $PrintShopConfigOption;
    protected $PrintShopPage;
    protected $PrintShopIncrease;
    protected $PrintShopConfigAttribute;
    protected $PrintShopConfigIncrease;
    protected $PrintShopConfigPrice;
    protected $PrintShopConfigPaperPrice;
    protected $PrintShopConfigRealizationTime;
    protected $PrintShopStaticPrice;
    protected $RealizationTimeComponent;
    protected $PrintShopVolume;
    protected $PrintShopType;
    protected $PrintShopRealizationTime;
    protected $PrintShopTypeTax;
    protected $PrintShopConfigConnectOption;
    protected $UserDiscountGroup;
    protected $DiscountGroupLang;
    protected $PrintShopConfigConnectPrice;
    protected $PrintShopConfigPrintType;

    protected $DiscountCalculation;
    private $PromotionCalculation;
    protected $Auth;
    protected $Price;
    protected $PrintShopConfigDiscountPrice;
    protected $DiscountGroup;
    protected $UserOption;
    protected $PrintShopConfigAttributeRange;
    protected $UploadFile;
    protected $PrintShopConfigPriceList;
    protected $CalculateStorage;
    protected $LangComponent;
    private $CalculateAdapter;
    private $Standard;
    private $OperationOption;
    private $OperationDevice;
    private $Device;
    private $DeviceSpeed;
    private $DevicePrice;
    private $Margin;
    private $MarginSupplier;
    private $formatSlope;
    private $maxFolds;

    public $adminInfo = array();
    public $attributesInfo = array();
    public $productsInfo = array();
    public $realisationTimes = array();
    public $volumes = array();

    protected $customVolumes = array();

    private $selectedDiscount;
    private $selectedPromotions;
    private $optionsRealisationTimes = array();
    private $priceTypes = array();
    private $currencyCourse = DEFAULT_COURSE;
    private $countBasePrice = false;
    private $specialAttributes = array();
    private $orderUserID = null;
    protected $selectedTechnology;
    private $activePrintTypes = array();
    private $userSelectedPrintTypeID = 0;
    private $userSelectedWorkspaceID = 0;
    private $userSelectedUseForSheet = NULL;
    private $lastUsedDiscountGroup;
    private $volumesContainer;
    private $perimeterContainer;
    private $fullProjectsSheets;
    private $ridgeThickness;
    private $CalculatorDevices;
    private $PrintShopConfigOptionDescription;
    private $PrintShopConfigAttributeNature;


    public function __construct()
    {
        parent::__construct();

        $this->Price = Price::getInstance();
        $this->RealizationTimeComponent = RealizationTimeComponent::getInstance();

        $this->PrintShopFormatPrintType = PrintShopFormatPrintType::getInstance();
        $this->PrintShopConfigPrintTypeWorkspace = PrintShopConfigPrintTypeWorkspace::getInstance();
        $this->PrintShopConfigWorkspace = PrintShopConfigWorkspace::getInstance();
        $this->PrintShopFormat = PrintShopFormat::getInstance();
        $this->PrintShopConfigDetailPrice = PrintShopConfigDetailPrice::getInstance();
        $this->PrintShopConfigOption = PrintShopConfigOption::getInstance();
        $this->PrintShopPage = PrintShopPage::getInstance();
        $this->PrintShopIncrease = PrintShopIncrease::getInstance();
        $this->PrintShopConfigAttribute = PrintShopConfigAttribute::getInstance();
        $this->PrintShopConfigIncrease = PrintShopConfigIncrease::getInstance();
        $this->PrintShopConfigPrice = PrintShopConfigPrice::getInstance();
        $this->PrintShopConfigPaperPrice = PrintShopConfigPaperPrice::getInstance();
        $this->PrintShopConfigRealizationTime = PrintShopConfigRealizationTime::getInstance();
        $this->PrintShopStaticPrice = PrintShopStaticPrice::getInstance();
        $this->PrintShopVolume = PrintShopVolume::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->PrintShopRealizationTime = PrintShopRealizationTime::getInstance();
        $this->PrintShopTypeTax = PrintShopTypeTax::getInstance();
        $this->PrintShopConfigConnectOption = PrintShopConfigConnectOption::getInstance();
        $this->PrintShopConfigConnectPrice = PrintShopConfigConnectPrice::getInstance();
        $this->PrintShopConfigPrintType = PrintShopConfigPrintType::getInstance();
        $this->PrintShopConfigDiscountPrice = PrintShopConfigDiscountPrice::getInstance();
        $this->UserOption = UserOption::getInstance();
        $this->PrintShopConfigAttributeRange = PrintShopConfigAttributeRange::getInstance();
        $this->PrintShopConfigPriceList = PrintShopConfigPriceList::getInstance();
        $this->DiscountCalculation = DiscountCalculation::getInstance();
        $this->PromotionCalculation = PromotionCalculation::getInstance();
        $this->DiscountGroup = DiscountGroup::getInstance();
        $this->UserDiscountGroup = UserDiscountGroup::getInstance();
        $this->DiscountGroupLang = DiscountGroupLang::getInstance();
        $this->UploadFile = UploadFile::getInstance();
        $this->CalculateStorage = CalculateStorage::getInstance();
        $this->LangComponent = LangComponent::getInstance();
        $this->CalculateAdapter = CalculateAdapter::getInstance();
        $this->Standard = Standard::getInstance();
        $this->OperationOption = OperationOption::getInstance();
        $this->OperationDevice = OperationDevice::getInstance();
        $this->Device = Device::getInstance();
        $this->DevicePrice = DevicePrice::getInstance();
        $this->DeviceSpeed = DeviceSpeed::getInstance();
        $this->CalculatorDevices = CalculatorDevices::getInstance();
        $this->PrintShopConfigOptionDescription = PrintShopConfigOptionDescription::getInstance();
        $this->Margin = Margin::getInstance();
        $this->MarginSupplier = MarginSupplier::getInstance();
        $this->PrintShopConfigAttributeNature=PrintShopConfigAttributeNature::getInstance();
         $this->Auth = new Auth();
    }

    private static function formatPriceDetail(array $finalPriceText)
    {
        $partKeys=explode(' ', 'basePrice minPrice expense increase price deviceID workUnit calculateDeviceDetails deviceSpeed speedChange speedChangeByRelation stackingTime transportTime operationTime');
        $parts=[];
        foreach($partKeys as $key){
           if(!empty($finalPriceText[$key])) {
               if(is_array($finalPriceText[$key])){
                   foreach($finalPriceText[$key] as $subitem){
                       $parts[]="$key:".$subitem;
                   }
               }else{
                   $parts[]="$key:".(in_array($key,['price']) ? $finalPriceText[$key] : round( $finalPriceText[$key] / 100, 2));
               }
           }
        }
        if(sizeof($parts)===1){
            return '';
        }
        return join('|', $parts);
    }
    public function getVolumesContainer()
    {
        return $this->volumesContainer;
    }

    public function setVolumesContainer($volumesContainer)
    {
        $this->volumesContainer = $volumesContainer;
    }

    public function getUserSelectedPrintTypeID()
    {
        return $this->userSelectedPrintTypeID;
    }

    public function setUserSelectedPrintTypeID($userSelectedPrintTypeID)
    {
        $this->userSelectedPrintTypeID = $userSelectedPrintTypeID;
    }

    public function getUserSelectedWorkspaceID()
    {
        return $this->userSelectedWorkspaceID;
    }

    public function setUserSelectedWorkspaceID($userSelectedWorkspaceID)
    {
        $this->userSelectedWorkspaceID = $userSelectedWorkspaceID;
    }

    public function getUserSelectedUseForSheet()
    {
        return $this->userSelectedUseForSheet;
    }

    public function setUserSelectedUseForSheet($userSelectedUseForSheet)
    {
        $this->userSelectedUseForSheet = $userSelectedUseForSheet;
    }

    public function getActivePrintTypes()
    {
        return $this->activePrintTypes;
    }

    public function setActivePrintTypes($activePrintTypes)
    {
        $this->activePrintTypes = $activePrintTypes;
    }

    public function resetActivePrintTypes()
    {
        $this->activePrintTypes = array();
    }

    public function addActivePrintType($typeID, $activePrintType)
    {
        $this->activePrintTypes[$typeID][] = $activePrintType;
    }

    public function getAdminInfo()
    {
        return $this->adminInfo;
    }

    public function getSelectedTechnology()
    {
        return $this->selectedTechnology;
    }

    public function setSelectedTechnology($selectedTechnology)
    {
        $this->selectedTechnology = $selectedTechnology;
    }

    public function getLastUsedDiscountGroup()
    {
        return $this->lastUsedDiscountGroup;
    }

    public function setLastUsedDiscountGroup($lastUsedDiscountGroup)
    {
        $this->lastUsedDiscountGroup = $lastUsedDiscountGroup;
    }

    public function getSpecialAttributes()
    {
        return $this->specialAttributes;
    }

    public function setSpecialAttributes($productID, $specialAttributes)
    {
        $this->specialAttributes[$productID] = $specialAttributes;
    }

    public function isCountBasePrice()
    {
        return $this->countBasePrice;
    }

    public function setCountBasePrice($countBasePrice)
    {
        $this->countBasePrice = $countBasePrice;
    }

    public function setSelectedDiscount($selectedDiscount)
    {
        $this->selectedDiscount = $selectedDiscount;
    }

    public function getSelectedDiscount()
    {
        return $this->selectedDiscount;
    }

    public function getSelectedPromotions()
    {
        return $this->selectedPromotions;
    }

    public function setSelectedPromotions($selectedPromotions)
    {
        $this->selectedPromotions = $selectedPromotions;
    }

    public function setOptionsRealisationTimes($optionsRealisationTimes)
    {
        $this->optionsRealisationTimes = $optionsRealisationTimes;
    }

    public function getOptionsRealisationTimes()
    {
        return $this->optionsRealisationTimes;
    }

    public function setCustomVolumes($customVolumes)
    {
        $this->customVolumes = $customVolumes;
    }

    public function getCustomVolumes()
    {
        return $this->customVolumes;
    }

    public function getCurrencyCourse()
    {
        return $this->currencyCourse;
    }

    public function setCurrencyCourse($currencyCourse)
    {
        $this->currencyCourse = $currencyCourse;
    }

    public function getFormatSlope(): int
    {
        return $this->formatSlope;
    }

    public function setFormatSlope(int $formatSlope): void
    {
        $this->formatSlope = $formatSlope;
    }

    public function setDomainID($domainID)
    {
        $this->PrintShopRealizationTime->setDomainID($domainID);
        $this->DiscountCalculation->setDomainID($domainID);
        $this->UserDiscountGroup->setDomainID($domainID);
        $this->PrintShopTypeTax->setDomainID($domainID);
        $this->PrintShopConfigOptionDescription->setDomainID($domainID);
    }
    public function getPriceTypes()
    {
        return $this->priceTypes;
    }

    public function setPriceTypes($priceTypes)
    {
        $this->priceTypes = $priceTypes;
    }

    public function getOrderUserID()
    {
        return $this->orderUserID;
    }

    public function setOrderUserID($orderUserID)
    {
        $this->orderUserID = $orderUserID;
    }

    public function getPerimeterContainer()
    {
        return $this->perimeterContainer;
    }

    public function setPerimeterContainer($perimeterContainer)
    {
        $this->perimeterContainer = $perimeterContainer;
    }

    public function getFullProjectsSheets()
    {
        return $this->fullProjectsSheets;
    }

    public function setFullProjectsSheets($fullProjectsSheets)
    {
        $this->fullProjectsSheets = $fullProjectsSheets;
    }

    public function searchOptionsRealisationTimes($products)
    {
        $optionsRealisationTimes = $this->getOptionsRealisationTimes();

        if (empty($optionsRealisationTimes)) {
            $optionsList = array();
            if (!empty($products)) {
                foreach ($products as $product) {
                    if (!empty($product['options'])) {
                        foreach ($product['options'] as $row) {
                            $optionsList[] = $row['optID'];
                        }
                    }
                    $optionsRealisationTimes = $this->PrintShopConfigRealizationTime->getByList($optionsList, 'DESC');
                    $this->setOptionsRealisationTimes($optionsRealisationTimes);
                }
            }
        }

        return $optionsRealisationTimes;
    }

    private function getSelectedPrintTypeID($adminInfo)
    {
        $selectedPrintTypeID = $adminInfo['selectedPrintType']['printTypeID'];
        return $selectedPrintTypeID;
    }

    private function getNotSelectedPrintTypes($adminInfo)
    {
        $notSelectedPrintTypes = false;
        if(array_key_exists('notSelectedPrintTypes', $adminInfo)) {
            $notSelectedPrintTypes = $adminInfo['notSelectedPrintTypes'];
        }

        if (!$notSelectedPrintTypes) {
            return false;
        }

        $aggregatePrintTypes = array();
        foreach ($notSelectedPrintTypes as $notSelectedPrintType) {
            $aggregatePrintTypes[] = $notSelectedPrintType['printTypeID'];
        }

        return $aggregatePrintTypes;
    }

    private function getSelectedPrintTypeIndex($adminInfo, $ID)
    {
        foreach ($adminInfo['printTypes'] as $index => $printType) {
            if ($printType['printTypeID'] == $ID) {
                return $index;
            }
        }
        return false;
    }

    private function getSelectedWorkspaceID($adminInfo)
    {
        $workspaceID = $adminInfo['selectedPrintType']['workspaceID'];
        return $workspaceID;
    }

    private function getSelectedWorkspaceIndex($adminInfo, $printTypeIndex, $ID)
    {
        foreach ($adminInfo['printTypes'][$printTypeIndex]['workspaces'] as $index => $printType) {
            if ($printType['workspaceID'] == $ID) {
                return $index;
            }
        }
        return false;
    }

    public function calculate($groupID, $typeID, $amount, $volume, $products, $tax)
    {

        $calcInfo = array();
        $calculations = array();
        $this->productsInfo = array();
        $errorsInfo = array();

        $additionalPrice = 0;
        $additionalWeight = 0;
        $this->ridgeThickness = $this->calculateRidgeThickness($products, $groupID, $typeID);
        foreach ($products as $prodIdx => $product) {

            if ( array_key_exists('printTypeID', $product) ) {
                $this->setUserSelectedPrintTypeID($product['printTypeID']);
            }

            if ( array_key_exists('workspaceID', $product) ) {
                $this->setUserSelectedWorkspaceID($product['workspaceID']);
            }

            if( array_key_exists('useForSheet', $product) ) {
                $this->setUserSelectedUseForSheet($product['useForSheet']);
            } else {
                $this->setUserSelectedUseForSheet(NULL);
            }

            $this->adminInfo = array();

            if (!$product['groupID']) {
                $type = $this->CalculateStorage->getType($product['typeID']);
                $product['groupID'] = $type['groupID'];
            }

            $pagesRange = $this->CalculateStorage->getPagesRange($product['groupID'], $product['typeID']);

            if ($pagesRange) {

                if ($pagesRange['minPages'] > 0 && $product['pages'] < $pagesRange['minPages']) {
                    $errorsInfo[] = array(
                        'translate' => $this->LangComponent->translate('minimum_number_of_pages'),
                        'text' => 'Minimal number of pages not achieved. Minimal pages is: ' . $pagesRange['minPages'],
                        'minimumPages' => $pagesRange['minPages'],
                        'maximumPages' => $pagesRange['maxPages']
                    );
                    continue;
                }

                if ($pagesRange['maxPages'] > 0 && $product['pages'] > $pagesRange['maxPages']) {
                    $errorsInfo[] = array(
                        'translate' => $this->LangComponent->translate('maximum_number_of_pages'),
                        'text' => 'Maximum number of pages exceeded. Max number of pages is: ' . $pagesRange['maxPages'],
                        'maximumPages' => $pagesRange['maxPages'],
                        'minimumPages' => $pagesRange['minPages']
                    );
                    continue;
                }

            }

            $errorAttributesPages = $this->checkAttributesPages($product['attrPages']);

            if ($errorAttributesPages) {
                $errorsInfo = array_merge($errorsInfo, $errorAttributesPages);
                continue;
            }

            $doublePage = $this->CalculateStorage->getDoublePage($product['groupID'], $product['typeID']);

            $errorThickness = $this->checkProductThickness($product['options'], $product['pages'], $doublePage);

            if ($errorThickness) {
                $errorsInfo = array_merge($errorsInfo, $errorThickness);
                continue;
            }

            $format = $this->CalculateStorage->getFormat($product['formatID'],$product);
            if (isset($product['wingtipFront'])) {
                $format['wingtipFront'] = $product['wingtipFront'];
            }
            if (isset($product['wingtipBack'])) {
                $format['wingtipBack'] = $product['wingtipBack'];
            }

            $this->attributesInfo=[];

            $calcResult = $this->_calcPrice(
                $product['groupID'],
                $product['typeID'],
                $product['formatID'],
                $format,
                $product['width'],
                $product['height'],
                $product['pages'],
                $volume,
                $product['options'],
                $product['attrPages']
            );

            $productInfoIdx = count($this->productsInfo) - 1;
            if ($pagesRange) {
                $this->productsInfo[$productInfoIdx]['pageRanges'] = array(
                    'minimumPages' => $pagesRange['minPages'],
                    'maximumPages' => $pagesRange['maxPages'],
                    'minimumWarning' => $this->LangComponent->translate('minimum_number_of_pages'),
                    'maximumWarning' => $this->LangComponent->translate('maximum_number_of_pages'),
                );
            }
            $calculations[] = $calcResult;

            $selectedPrintTypeID = $this->getSelectedPrintTypeID($this->adminInfo);
            $selectedPrintTypeIndex = $this->getSelectedPrintTypeIndex($this->adminInfo, $selectedPrintTypeID);

            $selectedWorkspaceID = $this->getSelectedWorkspaceID($this->adminInfo);
            $selectedWorkspaceIndex = $this->getSelectedWorkspaceIndex($this->adminInfo, $selectedPrintTypeIndex, $selectedWorkspaceID);

            $selectedWorkspacePrice = $this->adminInfo['printTypes'][$selectedPrintTypeIndex]['workspaces'][$selectedWorkspaceIndex]['price'];
            $selectedWorkspaceExpense = $this->adminInfo['printTypes'][$selectedPrintTypeIndex]['workspaces'][$selectedWorkspaceIndex]['expense'];

            $specialAttributes = array();
            $totalSelectedPrice = 0;
            $totalSelectedExpense = 0;
            if (!empty($product['specialAttributes'])) {
                foreach ($product['specialAttributes'] as $specialAttribute) {
                    $sumPrice = 0;
                    $sumExpense = 0;
                    $sumWeight = 0;
                    $specialAttribute['price'] = $this->Price->getPriceToDb($specialAttribute['price']);
                    $specialAttribute['expense'] = $this->Price->getPriceToDb($specialAttribute['expense']);

                    if ($specialAttribute['type'] == SPECIAL_ATTRIBUTE_TYPE_AMOUNT) {
                        $sumPrice = $specialAttribute['price'] * $volume;
                        $sumExpense = $specialAttribute['expense'] * $volume;
                        $sumWeight += ($specialAttribute['weight'] / 1000) * $volume;
                    } else if ($specialAttribute['type'] == SPECIAL_ATTRIBUTE_TYPE_METERS) {
                        $sumPrice = $specialAttribute['price'] * $calcResult['area'];
                        $sumExpense = $specialAttribute['expense'] * $calcResult['area'];
                        $sumWeight += ($specialAttribute['weight'] / 1000) * $calcResult['area'];
                    }else if ($specialAttribute['type'] == SPECIAL_ATTRIBUTE_TYPE_ORDER) {
                        $sumPrice = $specialAttribute['price'];
                    }

                    $totalSelectedPrice = intval($selectedWorkspacePrice) + intval($sumPrice);
                    $totalSelectedExpense = intval($selectedWorkspaceExpense) + intval($sumExpense);

                    $additionalPrice += $sumPrice;
                    $additionalWeight += $sumWeight;
                    $specialAttribute['price'] = $this->Price->getPriceToView($specialAttribute['price']);
                    $specialAttribute['expense'] = $this->Price->getPriceToView($specialAttribute['expense']);
                    $specialAttribute['sumPrice'] = $this->Price->getPriceToView($sumPrice);
                    $specialAttribute['sumExpense'] = $this->Price->getPriceToView($sumExpense);
                    $specialAttribute['sumWeight'] = str_replace('.', MATH_DIVIDE_SYMBOL, round($sumWeight, 2));
                    $specialAttributes[] = $specialAttribute;
                }
            }

            if ($totalSelectedPrice > 0) {
                $this->adminInfo['printTypes'][$selectedPrintTypeIndex]['workspaces'][$selectedWorkspaceIndex]['totalPrice'] = $this->Price->getPriceToView(
                    $totalSelectedPrice
                );
            }

            if ($totalSelectedExpense) {
                $this->adminInfo['printTypes'][$selectedPrintTypeIndex]['workspaces'][$selectedWorkspaceIndex]['totalExpense'] = $this->Price->getPriceToView(
                    $totalSelectedExpense
                );
            }

            $this->setSpecialAttributes($product['typeID'], $specialAttributes);

            $productName = NULL;
            if( array_key_exists('name', $product) ) {
                $productName = $product['name'];
            }

            $this->adminInfo['product'] = array(
                'name' => $productName,
                'typeID' => $product['typeID'],
                'taxName' => $tax['name'],
                'taxValue' => $tax['value'],
                'specialAttributes' => $specialAttributes
            );
            $calcInfo[] = $this->adminInfo;
        }

        if (empty($calculations)) {
            return array(
                'correctCalculation' => false,
                'errors' => $errorsInfo
            );
        }

        if (!isset($this->realisationTimes[$typeID])) {
            $this->PrintShopRealizationTime->setGroupID($groupID);
            $this->PrintShopRealizationTime->setTypeID($typeID);

            $realisationTimes = $this->PrintShopRealizationTime->getRealizationTimes(NULL);
            $realisationTimesDetails = $this->PrintShopRealizationTime->getRealizationTimeDetailsAll();

            if ($realisationTimes && $realisationTimesDetails) {

                foreach ($realisationTimes as $rtKey => $rt) {

                    if ( !array_key_exists($rt['ID'], $realisationTimesDetails)) {

                        if ($rt['active'] == 0) {
                            unset($realisationTimes[$rtKey]);
                            continue;
                        }
                    }

                    if (isset($realisationTimesDetails[$rt['ID']])) {

                        foreach ($realisationTimesDetails[$rt['ID']] as $row) {

                            $row = $this->identifyRealizationTimeDetail($row);

                            switch ($row['type']) {
                                case 'volume':

                                    if( $row['active'] == 0 ) {
                                        $this->volumes[$row['realizationID']][$row['volume']] = array(
                                            'active' => false,
                                            'volume' => $row['volume']
                                        );
                                    } else {
                                        $this->volumes[$row['realizationID']][$row['volume']] = array(
                                            'days' => $row['days'],
                                            'pricePercentage' => $row['pricePercentage'],
                                            'active' => true,
                                            'replaced' => true
                                        );
                                    }

                                    break;
                                case 'type':

                                    $realisationTimes[$rtKey]['days'] = $row['days'];
                                    $realisationTimes[$rtKey]['pricePercentage'] = $row['pricePercentage'];
                                    $realisationTimes[$rtKey]['replaced'] = 2;
                                    $realisationTimes[$rtKey]['active'] = $row['active'];

                                    break;
                                case 'group':

                                    $replaced = false;
                                    if( array_key_exists($rtKey, $realisationTimes) &&
                                        array_key_exists('replaced', $realisationTimes[$rtKey])
                                    && $realisationTimes[$rtKey]['replaced'] > 1 ) {
                                        $replaced = true;
                                    }

                                    if(!$replaced) {
                                        $realisationTimes[$rtKey]['days'] = $row['days'];
                                        $realisationTimes[$rtKey]['pricePercentage'] = $row['pricePercentage'];
                                        $realisationTimes[$rtKey]['replaced'] = 1;
                                        $realisationTimes[$rtKey]['active'] = $row['active'];
                                    }
                                    break;
                            }

                        }
                    }

                }
            }

            foreach ($realisationTimes as $key => $row) {
                if( intval($row['active']) == 0 ) {
                    unset($realisationTimes[$key]);
                }
            }

            $realisationTimesResult = array();
            if ($realisationTimes) {
                foreach ($realisationTimes as $key => $row) {
                    $row['date'] = $this->RealizationTimeComponent->calcRealizationDate($row['days']);
                    $realisationTimesResult[$row['ID']] = $row;
                }
            }
            $this->realisationTimes[$typeID] = $realisationTimesResult;
        }

        $result['products'] = $this->productsInfo;

        if (sourceApp === 'manager') {
            $result['info'] = $calcInfo;
            $result['specialAttributes'] = $specialAttributes;
        } else {
            $result['info'] = null;
        }

        $result['response'] = true;

        $course = $this->getCurrencyCourse();
        if (!$course) {
            $course = DEFAULT_COURSE;
        }

        $endCalculation = compact('amount', 'groupID', 'typeID', 'volume');
        $endCalculation['marginParts']=[];
        $allNatures=$this->PrintShopConfigAttributeNature->getAll();
        $naturesMap=[];
        foreach($allNatures as $nature){
            $naturesMap[$nature['ID']]=$nature['function'];
        }
        foreach ($this->attributesInfo as $attrInfo) {
            foreach($attrInfo as $optId=>$info){
                foreach ($info['all']['marginsParts'] as $key => $value) {
                    $type = !empty($naturesMap[$key]) ? 'nature' : 'supplier';
                    $key = !empty($naturesMap[$key]) ? $naturesMap[$key] : $key;
                    if (!isset($endCalculation['marginParts'][$key])) {
                        $endCalculation['marginParts'][$key] = ['value' => 0];
                    }
                    $endCalculation['marginParts'][$key]['type'] = $type;
                    $endCalculation['marginParts'][$key]['value'] += $value['value'];
                }
            }

        }
        foreach($endCalculation['marginParts'] as &$mp){
            $mp['value']=$this->Price->getPriceToView($mp['value']);
        }
        $endCalculation['price'] = 0;
        $endCalculation['basePrice'] = 0;
        $endCalculation['weight'] = 0;
        $endCalculation['expense'] = null;

        $increaseRealizationTime = 0;

        $allProcessDiscount = 0;
        foreach ($calculations as $calculation) {

            $allProcessDiscount += $calculation['attrDiscount'];

            $endCalculation['basePrice'] += $calculation['basePrice'];
            $endCalculation['price'] += $calculation['price'];

            $endCalculation['attrDiscount'] = $calculation['attrDiscount'];
            if ($calculation['expense']) $endCalculation['expense'] += $calculation['expense'];
            $endCalculation['weight'] += $calculation['weight'];

            if ($calculation['increaseRealizationTime'] > $increaseRealizationTime) {
                $increaseRealizationTime = $calculation['increaseRealizationTime'];
            }
        }

        $loggedUser = $this->Auth->getLoggedUser();

        $areaInMeters = NULL;
        $percentageDiscount = 0;

        if (count($calculations) == 1) {
            $areaInMeters = $calculations[0]['area'];
        }

        if ((sourceApp === 'manager' && $this->getOrderUserID() > 0) || $loggedUser) {

            $this->DiscountCalculation->setSelectedDiscount($this->getSelectedDiscount());

            $percentageDiscount = $this->DiscountCalculation->calculate($volume, $areaInMeters);

        }

        $this->PromotionCalculation->setSelectedPromotions($this->getSelectedPromotions());

        $percentagePromotion = $this->PromotionCalculation->calculate($volume, $areaInMeters);

        if (($percentagePromotion || $percentageDiscount) && $percentagePromotion > $percentageDiscount) {
            $endCalculation['percentageDiscount'] = $percentagePromotion;
        } else {
            $endCalculation['percentageDiscount'] = $percentageDiscount;
        }

        if ($amount < 1) {
            $amount = 1;
        }

        $endCalculation['price'] *= $amount;
        $additionalPrice *= $amount;
        $additionalWeight *= $amount;
        $endCalculation['expense'] *= $amount;
        $endCalculation['weight'] *= $amount;

        if ($course > 0) {
            $endCalculation['price'] = $endCalculation['price'] / ($course / 100);
            $endCalculation['basePrice'] = $endCalculation['basePrice'] / ($course / 100);
            $allProcessDiscount = $allProcessDiscount / ($course / 100);
            $endCalculation['expense'] /=  ($course / 100);
        }

        if ($additionalPrice > 0) {
            $endCalculation['price'] += $additionalPrice;
        }

        if ($additionalWeight > 0) {
            $endCalculation['weight'] += $additionalWeight;
        }

        if ($tax) {
            $endCalculation['priceBrutto'] = $endCalculation['price'] * (1 + ($tax['value'] / 100));
        } else {
            $endCalculation['priceBrutto'] = $endCalculation['price'];
        }

        if ($tax) {
            $endCalculation['baseGrossPrice'] = $endCalculation['basePrice'] * (1 + ($tax['value'] / 100));
        } else {
            $endCalculation['baseGrossPrice'] = $endCalculation['basePrice'];
        }

        $realisationTimeDiscounts = array();

        if (!empty($this->realisationTimes[$typeID])) {
            foreach ($this->realisationTimes[$typeID] as $key => $row) {

                $oldPrice = false;
                $oldPriceGross = false;

                $tmpPrice = $endCalculation['basePrice'];

                $preparedPrice = $this->preparePrice($tmpPrice, $row['pricePercentage'], $tax['value']);
                $tmpPrice = $preparedPrice['price'];

                $discount = false;
                if ($percentageDiscount > 0) {
                    $discount = ($tmpPrice * $percentageDiscount) / 100;
                }

                $promotionDiscount = false;
                if ($percentagePromotion > 0) {
                    $promotionDiscount = ($tmpPrice * $percentagePromotion) / 100;
                }

                $discountAggregation = array(
                    'processDiscount' => $allProcessDiscount,
                    'discount' => $discount,
                    'promotionDiscount' => $promotionDiscount
                );

                $bestDiscountKey = array_search(max($discountAggregation), $discountAggregation);

                if ($discountAggregation[$bestDiscountKey] > 0) {
                    $oldPrice = $tmpPrice;
                    $oldPriceGross = $tmpPrice * (1 + ($tax['value'] / 100));


                    switch ($bestDiscountKey) {
                        case 'processDiscount':

                            $realisationTimeDiscounts[$row['ID']] = $allProcessDiscount;
                            $tmpPrice -= $allProcessDiscount;

                            break;
                        case 'discount':

                            $realisationTimeDiscounts[$row['ID']] = $discount;
                            $tmpPrice = $tmpPrice - $discount;

                            break;
                        case 'promotionDiscount':

                            $realisationTimeDiscounts[$row['ID']] = $promotionDiscount;
                            $tmpPrice = $tmpPrice - $promotionDiscount;

                            break;
                        default:


                            break;
                    }

                } else {
                    $bestDiscountKey = null;
                }

                if ($additionalPrice > 0) {
                    $tmpPrice += $additionalPrice;
                }

                if( $amount > 1 ) {
                    $tmpPrice *= $amount;
                }

                $tmpPriceGross = $tmpPrice * (1 + ($tax['value'] / 100));

                $newDate = NULL;
                $active = true;
                $actDays = false;

                if( array_key_exists($row['ID'], $this->volumes) ) {

                    if( array_key_exists($volume, $this->volumes[$row['ID']]) ) {
                        if ($this->volumes[$row['ID']][$volume]) {
                            if(array_key_exists('active', $this->volumes[$row['ID']][$volume])) {
                                $active = $this->volumes[$row['ID']][$volume]['active'];
                            }
                            if(array_key_exists('days', $this->volumes[$row['ID']][$volume])) {
                                $actDays = $this->volumes[$row['ID']][$volume]['days'];
                            }
                        }
                    }

                    if (!empty($this->volumes[$row['ID']])) {
                        foreach ($this->volumes[$row['ID']] as $keyVolume => $rowVolume) {
                            if(!array_key_exists('days', $rowVolume)) {
                                $rowVolume['days'] = 0;
                            }
                            if ($keyVolume <= $volume && ($actDays > $rowVolume['days'] || !$actDays)) {
                                $actDays = $rowVolume['days'];
                            }
                        }
                    }

                }

                $moreDayForVolume = $this->getMoreDaysForVolume($products, $volume);

                if ($moreDayForVolume > 0) {
                    $actDays += $moreDayForVolume;
                } else if ($moreDayForVolume < 0) {
                    $actDays -= abs($moreDayForVolume);
                }

                if ($active && $actDays) {
                    $actDays = intval($row['days']) + $actDays;
                    if( $actDays < 0 ) {
                        $actDays = 0;
                    }
                    $newDate = $this->RealizationTimeComponent->calcRealizationDate($actDays);
                }

                $addItem = array(
                    'price' => $this->Price->getPriceToView($tmpPrice),
                    'priceBrutto' => $this->Price->getPriceToView($tmpPriceGross),
                    'basePrice' => $this->Price->getPriceToView($endCalculation['basePrice']),
                    'baseGrossPrice' => $this->Price->getPriceToView($endCalculation['baseGrossPrice']),
                    'volume' => $volume,
                    'date' => $newDate,
                    'active' => $active,
                    'weight' => $endCalculation['weight']
                );

                if (in_array($volume, $this->getCustomVolumes())) {
                    $addItem['custom'] = true;
                } else {
                    $addItem['custom'] = false;
                }

                if ($oldPrice) {
                    $addItem['oldPrice'] = $this->Price->getPriceToView($oldPrice);
                    $addItem['oldPriceBrutto'] = $this->Price->getPriceToView($oldPriceGross);
                    $addItem['price'] = $this->Price->getPriceToView($tmpPrice);
                    $addItem['priceBrutto'] = $this->Price->getPriceToView($tmpPriceGross);
                    if ($percentageDiscount) {
                        $addItem['percentageDiscount'] = $percentageDiscount;
                    }

                    if ($percentagePromotion && $percentagePromotion > $percentageDiscount) {
                        $addItem['percentageDiscount'] = $percentagePromotion;
                    }
                    $addItem['promotionType'] = $bestDiscountKey;
                }

                $this->realisationTimes[$typeID][$key]['volumes'][] = $addItem;
                unset($addItem);
            }
        }

        $endCalculation['oldPrice'] = $endCalculation['basePrice'];
        $endCalculation['basePrice'] = $this->Price->getPriceToView($endCalculation['basePrice']);
        $endCalculation['baseGrossPrice'] = $this->Price->getPriceToView($endCalculation['baseGrossPrice']);
        $endCalculation['tax'] = $tax;

        $result['calculation'] = $endCalculation;

        $result['realisationTimes'] = $this->realisationTimes;
        $result['calculation']['realisationTimeDiscounts'] = $realisationTimeDiscounts;
        $result['correctCalculation'] = true;
        $result['errors'] = $errorsInfo;


        $selectedPrintTypeID = $this->getSelectedPrintTypeID($this->adminInfo);
        $selectedIndex = $this->getSelectedPrintTypeIndex($this->adminInfo, $selectedPrintTypeID);
        $result['calculation']['priceListIcon'] = $this->adminInfo['printTypes'][$selectedIndex]['priceListIcon'];

        $result['calculation']['priceListIcons'] = [];
        foreach ($result['products'] as $product) {
            foreach ($this->adminInfo['printTypes'] as $printType) {
                if ($printType['printTypeID'] == $product['printTypeID']) {
                    $result['calculation']['priceListIcons'][$product['typeID']] = $this->adminInfo['printTypeIcons'][$printType['priceLists']['iconID']];
                }
            }
        }

        $result['calculation']['priceLists'] = $this->adminInfo['printTypes'][$selectedIndex]['priceLists'];

        $notSelectedPrintTypes = $this->getNotSelectedPrintTypes($this->adminInfo);
        if ($notSelectedPrintTypes) {
            foreach ($notSelectedPrintTypes as $notSelectedPrintTypeID) {
                $selectedIndex = $this->getSelectedPrintTypeIndex($this->adminInfo, $notSelectedPrintTypeID);
                $result['calculation']['notSelectedPrintTypes'][] = $this->adminInfo['printTypes'][$selectedIndex]['priceLists'];
            }
        }


        return $result;

    }

    private function identifyRealizationTimeDetail($realizationTimeDetailEntity)
    {
        if( intval($realizationTimeDetailEntity['volume']) > 0 && intval($realizationTimeDetailEntity['typeID']) > 0 &&
        intval($realizationTimeDetailEntity['groupID']) > 0)  {
            $realizationTimeDetailEntity['type'] = 'volume';
            return $realizationTimeDetailEntity;
        }

        if( intval($realizationTimeDetailEntity['volume']) == 0 && intval($realizationTimeDetailEntity['typeID']) > 0 &&
            intval($realizationTimeDetailEntity['groupID']) > 0 ) {
            $realizationTimeDetailEntity['type'] = 'type';
            return $realizationTimeDetailEntity;
        }

        if( intval($realizationTimeDetailEntity['volume']) == 0 && intval($realizationTimeDetailEntity['typeID']) == 0 &&
            intval($realizationTimeDetailEntity['groupID']) > 0 ) {
            $realizationTimeDetailEntity['type'] = 'group';
            return $realizationTimeDetailEntity;
        }

        return $realizationTimeDetailEntity;
    }

    private function preparePrice($price, $pricePercentage, $taxValue)
    {
        $result = array();
        $price = $price * (1 + ($pricePercentage / 100));
        $priceGross = $price * (1 + ($taxValue / 100));
        $result['price'] = $price;
        $result['priceGross'] = $priceGross;
        return $result;
    }

    private function getMoreDaysForVolume($products, $volume)
    {
        $optionsRealizationTimes = $this->searchOptionsRealisationTimes($products);

        $sumDaysToAdded = 0;
        $excludedOptions = array();

        $foundToAdded = $this->searchByVolume($optionsRealizationTimes, $volume);

        if( $foundToAdded['daysToAdd'] > 0 ) {
            $sumDaysToAdded += $foundToAdded['daysToAdd'];
        } else if ( $foundToAdded['daysToAdd'] < 0 ) {
            $sumDaysToAdded -= abs($foundToAdded['daysToAdd']);
        }

        if( is_array( $foundToAdded['optionToExclude'] ) ) {
            $excludedOptions = array_merge($excludedOptions, $foundToAdded['optionToExclude']);
        }

        $previousVolume = $this->getPreviousVolume($volume);

        while($previousVolume) {

            $foundToAdded = $this->searchByVolume($optionsRealizationTimes, $previousVolume, $excludedOptions, true);

            if( $foundToAdded['daysToAdd'] > 0 ) {
                $sumDaysToAdded += $foundToAdded['daysToAdd'];
            } else if ( $foundToAdded['daysToAdd'] < 0 ) {
                $sumDaysToAdded -= abs($foundToAdded['daysToAdd']);
            }
            if ( is_array($foundToAdded['optionToExclude']) ) {
                $excludedOptions = array_merge($excludedOptions, $foundToAdded['optionToExclude']);
            } else {
                $excludedOptions = array();
            }

            $previousVolume = $this->getPreviousVolume($previousVolume);

        }

        return $sumDaysToAdded;

    }

    private function getPreviousVolume($currentVolume)
    {
        $volumesList = $this->getVolumesContainer();

        $currentKey = $this->getVolumeKey($volumesList, $currentVolume);

        if( isset($volumesList[$currentKey-1]) ) {
            return $volumesList[$currentKey-1]['volume'];
        }

        return false;
    }

    private function getVolumeKey($volumesList, $volume)
    {

        if (!$volumesList) {
            return false;
        }

        foreach ($volumesList as $key => $row) {

            if ($row['volume'] == $volume) {
                return $key;
            }

        }

        return false;

    }

    private function searchByVolume($optionsRealizationTimes, $volume, $excludedOptions = array(), $checkSmallerVolume = false)
    {
        if (!$optionsRealizationTimes) {
            return false;
        }

        $daysToAdd = 0;
        $optionToExclude = array();

        foreach ($optionsRealizationTimes as $optID => $optionVolumes) {

            if( in_array($optID, $excludedOptions) ) {
                continue;
            }

            foreach ($optionVolumes as $ovValue) {

                if( in_array($optID, $optionToExclude) ) {
                    continue;
                }

                if( $checkSmallerVolume ) {

                    if ($ovValue['volume'] <= $volume) {
                        $optionToExclude[] = $optID;
                        if ($ovValue['days'] > 0) {
                            $daysToAdd += intval($ovValue['days']);
                        } else {
                            $daysToAdd -= abs($ovValue['days']);
                        }
                    }

                } else {

                    if ($ovValue['volume'] == $volume) {
                        $optionToExclude[] = $optID;
                        if ($ovValue['days'] > 0) {
                            $daysToAdd += intval($ovValue['days']);
                        } else {
                            $daysToAdd -= abs($ovValue['days']);
                        }
                    } else if ($ovValue['volume'] <= $volume) {
                        $optionToExclude[] = $optID;
                        if ($ovValue['days'] > 0) {
                            $daysToAdd += intval($ovValue['days']);
                        } else {
                            $daysToAdd -= abs($ovValue['days']);
                        }
                    }

                }

            }
        }

        return compact(
            'daysToAdd',
            'optionToExclude'
        );
    }

    private function setMaxFolds($maxFolds)
    {
        $this->maxFolds = $maxFolds;
    }

    private function getMaxFolds()
    {
        return $this->maxFolds;
    }

    private function _calcPrice($groupID, $typeID, $formatID, $format, $formatWidth, $formatHeight, $pages, $volume, $attributes, $attributeAmount)
    {
        $adminInfo = array();
        $calcPrices = array();
        $weight = null;

        $this->productsInfo[] = array(
            'groupID' => $groupID,
            'typeID' => $typeID,
            'formatID' => $formatID,
            'formatWidth' => $formatWidth,
            'formatHeight' => $formatHeight,
            'pages' => $pages,
            'attributes' => array()
        );

        if (Calculator::isDoubledPages($format)) {
            $pages /= 2;
        }

        $this->PrintShopIncrease->setGroupID($groupID);
        $this->PrintShopIncrease->setTypeID($typeID);

        $printTypes = $this->_printTypes($formatID, $volume);
        if (empty($printTypes)) {
            return array('error' => 'No print types');
        }

        $paperInfo=[];
        $optionsArray = array();

        $doublePage = $this->CalculateStorage->getDoublePage($groupID, $typeID);

        list($oneSide,$paperInfo,   $size, $rollLength, $maxFolds) = $this->getDimensions($attributes, $optionsArray, $paperInfo, $pages, $doublePage);

        $similarPages = $this->CalculateStorage->getSimilarPages($groupID, $typeID);

        $setIncrease = $this->CalculateStorage->getIncrease('set', $volume, $formatID);

        $aggregateOptions = $this->agregateOptions($attributes);

        $this->CalculateStorage->setOptionsByList($aggregateOptions);


        $adminInfo['printTypes'] = array();

        $aggregatePriceLists = array();
        $aggregateWorkspaces = array();
        $aggregatePrintTypes = array();

        list( $aggregatePriceLists, $aggregateWorkspaces, $aggregatePrintTypes) = $this->agregateFromPrintType($printTypes, $aggregatePriceLists, $aggregateWorkspaces, $aggregatePrintTypes);

        $printTypeWorkspaces = $this->CalculateStorage->getPrintTypeWorkspaces($formatID, $aggregatePrintTypes);

        $this->CalculateStorage->setWorkSpaceByList($aggregateWorkspaces);

        $priceLists = $this->CalculateStorage->getPriceListCluster($aggregatePriceLists);

        $adminInfo['printTypeIcons'] = $printTypeIcons = $this->getPrintTypeIcons($priceLists);

        foreach ($printTypes as $printType) {

            $noCounting = $this->getSelectedTechnology() && $this->getSelectedTechnology()['ID']!=$printType['pricelistID'];

            $workspaces = $this->getWorkspaces($printType);

            $increaseRealizationTime = 0;

            $printTypeInfo = $this->initPrintTypeInfo($printType, $priceLists[$printType['pricelistID']], $printTypeIcons, $size, $volume);

            $volumeStart = $volume;

            list($rows, $volume) = $this->modifyRowsToFormat($format['rows'], $volume);

            $printTypeInfo['rows'] = $rows;

            $rollWidth = intval($format['width']);

            $printRotated = $printTypeInfo['printRotated'] = $this->CalculateStorage->getPrintRotated($printType['printTypeID'], $optionsArray)!==false ? 1 : 0;

            $printTypeInfo['workspaces'] = array();

            foreach ($workspaces as $workspace) {//attrPrice loop

                $workspace['printTypeWorkspaceSettings'] = $this->CalculateAdapter->getPrintTypeWorkspaceSettings(
                    $formatID,
                    $printType['printTypeID'],
                    $workspace['ID'],
                    $printTypeWorkspaces
                );

                $workspaceID = $workspace['workspaceID'];
                $workspace['ID'] = $workspace['workspaceID'];

                $sheetCuts = 0;
                $excludedPrintType = false;
                $workspaceInfo = array(
                    'name' => $workspace['name'],
                    'workspaceID' => $workspaceID
                );

                list($workspaceInfo, $selectedUseForSheet) = $this->selectUseForSheet($printRotated, $workspaceInfo, $workspace['printTypeWorkspaceSettings']['usePerSheet']);

                $calcAllSheets = $this->getAllSheets(
                    $workspace,
                    $pages,
                    $volume,
                    $oneSide,
                    $printRotated,
                    $doublePage,
                    $selectedUseForSheet,
                    $format
                );
                $workspaceInfo['areaPerSheetForStandardResult'] = $calcAllSheets['areaPerSheetForStandardResult'];
                $workspaceInfo['width'] = $workspace['width'];
                $workspaceInfo['height'] = $workspace['height'];
                $sheets = $calcAllSheets['sheets'];

                $uzytkipersheet = $calcAllSheets['perSheet'];

                if($selectedUseForSheet &&
                    $selectedUseForSheet < $calcAllSheets['originalPerSheet'] ) {
                    $uzytkipersheet = $selectedUseForSheet;
                }

                $workspaceInfo['sheets'] = $sheets;

                if ($sheets === null) {
                    continue;
                }

                if ($calcAllSheets['areaPerSheetForStandardResult']) {
                    $workspace['longSideSheets'] = $calcAllSheets['areaPerSheetForStandardResult']['longSide'];
                    $workspace['shortSideSheets'] = $calcAllSheets['areaPerSheetForStandardResult']['shortSide'];
                }

                $projectSheetsInfo = $this->getProjectSheets(
                    $workspace,
                    $pages,
                    $oneSide,
                    $printRotated,
                    $doublePage,
                    $selectedUseForSheet,
                    $format
                );

                $projectSheets = $projectSheetsInfo['sheets'];

                if ($similarPages) {
                    $workspaceInfo['projectSheetsSimilar'] = true;
                    $projectSheets = 1;
                }

                $area = $this->getArea($volume, $rows, $rollLength, $setIncrease, $format);

                $totalArea = $this->getTotalArea($workspace, $volume, $rollLength, $setIncrease, $format);

                $perimeter = $this->_perimeter($volume, $format);
                $netPerimeter = $this->netPerimeter($volume, $format);
                $this->setPerimeterContainer(compact('perimeter', 'netPerimeter'));

                $uzytki = $this->_uzytki($pages, $volume, $oneSide, $doublePage);

                $sheetsForFolds=$uzytkipersheet;

                if(self::isDoubledPages($format)){
                    $sheetsForFolds +=1;
                }

                $folds = ceil(log($sheetsForFolds, 2));

                if ($maxFolds !== null && $maxFolds > 0) {
                    while ($folds > $maxFolds) {
                        $folds--;
                        $sheetCuts++;
                    }
                }
                $totalSheetFolds = $folds;
                if ($sheetCuts > 0) {
                    $totalSheetFolds *= $sheetCuts * 2;
                }

                $workspaceInfo['projectSheets'] = $projectSheets;

                $workspaceInfo['partProjectSheetsAmount'] = $this->CalculateAdapter->getInfoForPartProjectSheetsAmount(
                    $projectSheets,
                    $projectSheetsInfo['noRoundSheets']
                );

                $this->partProjectSheets=$workspaceInfo['partProjectSheets'] = $this->CalculateAdapter->getPartProjectSheets(
                    $projectSheetsInfo['noRoundSheets'],
                    $calcAllSheets['sheets']
                );

                $workspaceInfo['fullProjectSheets'] = $this->CalculateAdapter->getFullProjectSheets(
                    $projectSheetsInfo['noRoundSheets'],
                    $calcAllSheets['sheets']
                );
                $this->setFullProjectsSheets($workspaceInfo['fullProjectSheets']);

                $workspaceInfo['noRoundedProjectSheets'] = $this->CalculateAdapter->getInfoNoRoundedProjectSheets(
                    $projectSheetsInfo['noRoundSheets'],
                    $projectSheets
                );

                $workspaceInfo['valueOfPartInProjectSheets'] = $this->CalculateAdapter->getInfoForValueOfPartInProjectSheets(
                    $projectSheetsInfo['noRoundSheets']
                );

                $useSheets = $sheets;
                if( $pages > 4 ) {
                    $useSheets = $calcAllSheets['sheets'];
                }
                $workspaceInfo['sheets'] = $sheets = $useSheets;

                $workspaceInfo['area'] = $area['size'];
                $workspaceInfo['totalArea'] = $totalArea;
                $workspaceInfo['cylinderPerimeter'] = '';
                $workspaceInfo['rollWidth'] = $rollWidth;
                $workspaceInfo['generalLenght'] = '';
                $workspaceInfo['perimeter'] = $perimeter;
                $workspaceInfo['uzytki'] = $uzytki;
                $workspaceInfo['uzytkipersheet'] = $uzytkipersheet;
                $workspaceInfo['folds'] = $folds;
                $workspaceInfo['sheetCuts'] = $sheetCuts;
                $workspaceInfo['totalSheetFolds'] = $totalSheetFolds;

                $sheetIncrease = $this->CalculateStorage->getIncrease('sheet', $sheets, $formatID);

                $sheetsWithIncrease = $sheets;
                $volumeWithIncrease = $volume;

                if ($sheetIncrease != false) {
                    $sheetsWithIncrease += intval($sheetIncrease);
                }
                if ($setIncrease != false) {
                    $volumeWithIncrease += intval($setIncrease);
                    $sheetsWithIncrease += intval($setIncrease) * $projectSheets;
                }

                $workspaceInfo['increase']['sheets'] = $sheetsWithIncrease;

                $workspaceInfo['increase']['volume'] = $volumeWithIncrease;

                if ($workspace['type'] != 3) {
                    $sheetsArea = ($workspace['width'] / 1000 * $workspace['height'] / 1000) * $sheets;
                } else {
                    extract($this->getSizeExternal( $format));
                    $sheetsArea = $formatWidth / 1000 * $formatHeight / 1000;
                    $sheetsArea *= $volume;
                }

                $price = 0;
                $basePrice = 0;
                $expense = 0;
                $options = array();
                $options['pages'] = intval($pages);
                $optionsControllers = array();
                $attrsWeight = null;
                $sortAttr = array();
                $itemWeight = null;
                $weightPerMeter = null;

                $totalWeight=$this->CalculateStorage->getTotalWeight($attributes, $sheetsArea, $volume, $perimeter, $netPerimeter, $format, $workspaceID);

                $workspaceInfo['attrs'] = array();

                $discountGroups = false;

                foreach ($attributes as $attr) {

                    $finalPriceText=[];
                    $attrID = $attr['attrID'];
                    $optID = $attr['optID'];

                    if (isset($attributeAmount[$attrID])) {
                        $selectedAmount = $attributeAmount[$attrID];
                    } else {
                        $selectedAmount = null;
                    }

                    $loggedUser = $this->Auth->getLoggedUser();

                    if (sourceApp === 'manager' && $this->getOrderUserID() > 0) {
                        $discountGroups = $this->UserDiscountGroup->getByUser($this->getOrderUserID());
                    } else if ($loggedUser) {
                        $discountGroups = $this->UserDiscountGroup->getByUser($loggedUser['ID']);
                    }

                    $attrPriceBase = false;

                    $attrPrice = $this->_attrPrice(
                        $attrID, $optID, $printType['printTypeID'], $workspace, $printType['pricelistID'], $sheets,
                        $projectSheets, $area, $perimeter, $volume, $selectedAmount, $pages, $size, $uzytki,
                        $totalArea, $totalSheetFolds, $sheetIncrease, $setIncrease, false, $groupID,
                        $typeID, $format, $sheetCuts, $totalWeight, $finalPriceText, $paperInfo
                    );
                    $tmpTexts=[];
                    if ($discountGroups) {

                        $this->setCountBasePrice(true);
                        $attrPriceBase = $this->_attrPrice(
                            $attrID, $optID, $printType['printTypeID'], $workspace, $printType['pricelistID'], $sheets, $projectSheets, $area, $perimeter, $volume, $selectedAmount, $pages, $size, $uzytki, $totalArea, $totalSheetFolds, $sheetIncrease, $setIncrease, false, $groupID, $typeID, $format, $sheetCuts, $totalWeight, $tmpTexts, $paperInfo
                        );
                        $this->setCountBasePrice(false);

                        $basePrice += $attrPriceBase;

                    } else {
                        $basePrice += $attrPrice;
                    }

                    $optionsControllers[$optID] = $this->attributesInfo[$attrID][$optID]['controllerID'];

                    $price += $attrPrice;
                    $attrExpense = $this->_attrPrice(
                        $attrID, $optID, $printType['printTypeID'], $workspace, $printType['pricelistID'], $sheets, $projectSheets, $area, $perimeter, $volume, $selectedAmount, $pages, $size, $uzytki, $totalArea, $totalSheetFolds, $sheetIncrease, $setIncrease, true, $groupID, $typeID, $format, $sheetCuts, $totalWeight, $tmpTexts, $paperInfo
                    );
                    $expense += $attrExpense;

                    if (sourceApp === 'manager') {
                        $optionInfo = $this->CalculateStorage->getOption($optID);

                        $attrInfo = $this->CalculateStorage->getAttribute($attrID);
                        $priceDetail = Calculator::formatPriceDetail($finalPriceText);
                        $this->attributesInfo[$attrID][$optID]['all']['priceDetail']=$priceDetail;
                        $info = array(
                            'optionName' => $optionInfo['name'],
                            'attrName' => $attrInfo['name'],
                            'info' => ' attr[' . $attrID . '][' . $optID . ']',
                            'attrPrice' => $attrPrice,
                            'attrExpense' => $attrExpense,
                            'attrID' => $attrID,
                            'optID' => $optID,
                            'optionController' => $optionsControllers[$optID],
                            'calcInfo' => $this->attributesInfo[$attrID][$optID]
                        );
                        if ($attrPriceBase) {

                            if ($attrPrice < $attrPriceBase) {
                                $info['oldAttrPrice'] = $attrPriceBase;
                            }

                            $lastDiscountGroup = $this->getLastUsedDiscountGroup();
                            if ($lastDiscountGroup) {
                                $discountGroupName = $this->DiscountGroupLang->getNamesForOne($lastDiscountGroup);
                                $info['discountGroup'] = $discountGroupName;
                                $this->setLastUsedDiscountGroup(NULL);
                            }

                        }

                        if ($excludedPrintType) {
                            $info['excluded'] = true;
                        }
                        $workspaceInfo['attrs'][] = $info;
                    } else {
                        $info = null;
                    }

                    if ($attrPrice === null) {
                        $excludedPrintType = true;
                        break;
                    }

                    $options[$attrID] = intval($optID);

                    $attr = $this->CalculateStorage->getAttribute($attrID);
                    $sortAttr[$attrID] = $attr['sort'];
                    $activeAttr[$attrID] = $attr;
                    $activeOption[$optID] = $this->CalculateStorage->getOption($optID);
                    if ($attr['type'] == 3) {
                        $option = $activeOption[$optID];
                        if ($option['weight'] !== null) {
                            $attrsWeight += $option['weight'];
                        }
                    }

                    if ($activeOption[$optID]['itemWeight'] !== null) {
                        $itemWeight += $activeOption[$optID]['itemWeight'];
                    }

                    if ($activeOption[$optID]['weightPerMeter'] !== null) {
                        $priceTypes = $this->getPriceTypes();
                        $amountOfKilograms = $activeOption[$optID]['weightPerMeter'] / 1000;

                        $netWidth = $format['width'] - ($format['slope'] * 2);
                        $netHeight = $format['height'] - ($format['slope'] * 2);

                        if ($netHeight > $netWidth) {
                            $longSide = $netHeight;
                            $shortSide = $netWidth;
                        } else {
                            $longSide = $netWidth;
                            $shortSide = $netHeight;
                        }
                        $weightPerMeter = $this->CalculateStorage->getWeightPerMeter($priceTypes, $perimeter, $amountOfKilograms, $netPerimeter, $netWidth, $netHeight, $longSide, $shortSide, $volume);
                    }

                    $optionRealizationTime = $this->PrintShopConfigRealizationTime->getSpecify($optID, $volume);
                    if ($optionRealizationTime) {
                        $increaseRealizationTime += $optionRealizationTime;
                    }
                }

                $volume = $volumeStart;

                if ($excludedPrintType) {
                    $workspaceInfo['excluded'] = true;
                    $printTypeInfo['workspaces'][] = $workspaceInfo;
                    continue;
                }

                if ($attrsWeight !== null) {
                    $weight = round($sheetsArea * $attrsWeight / 1000, 2);
                }

                if ($itemWeight !== null) {
                    $weight += round($volume * $itemWeight / 1000, 2);
                }

                if ($weightPerMeter !== null) {
                    $weight += $weightPerMeter;
                }

                $options['volumes'] = intval($volume);

                $staticOptions = $options;
                uksort($staticOptions, array($this->Standard, 'sortLikeJs'));
                $staticOptions = json_encode($staticOptions);
                $workspaceInfo['staticPriceOptions'] = $staticOptions;

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

                $workspaceInfo['price'] = $price;
                $workspaceInfo['expense'] = $expense;

                unset($options['volumes']);
                unset($options['pages']);

                $calcPrices[] = array(
                    'price' => $price,
                    'basePrice' => $basePrice,
                    'expense' => $expense,
                    'options' => $options,
                    'optionsControllers' => $optionsControllers,
                    'printTypeID' => $printType['printTypeID'],
                    'printTypeTrueID' => $printType['ID'],
                    'workspaceID' => $workspace['ID'],
                    'iconDir' => $iconDir,
                    'attributesInfo' => $this->attributesInfo,
                    'noCounting' => $noCounting
                );

                $printTypeInfo['workspaces'][] = $workspaceInfo;

            }

            $adminInfo['printTypes'][] = $printTypeInfo;

            $this->addActivePrintType($typeID, $printTypeInfo);

        }

        $price = null;
        $basePrice = null;
        $printTypeID = null;
        $expense = null;
        $options = array();
        $optionsControllers = array();
        $iconDir = null;

        foreach ($calcPrices as $eachPrice) {

            $userSelectedWorkspaceID = $this->getUserSelectedWorkspaceID();
            $userSelectedPrintTypeID = $this->getUserSelectedPrintTypeID();

            if ($userSelectedPrintTypeID && $userSelectedPrintTypeID != $eachPrice['printTypeTrueID']) {
                $eachPrice['noCounting'] = true;
            }

            if ($userSelectedWorkspaceID && $userSelectedWorkspaceID != $eachPrice['workspaceID']) {
                $eachPrice['noCounting'] = true;
            }

            if ($eachPrice['noCounting']) {

                $adminInfo['notSelectedPrintTypes'][] = array(
                    'price' => $price,
                    'printTypeID' => $eachPrice['printTypeID'],
                    'workspaceID' => $eachPrice['workspaceID'],
                    'expense' => $expense
                );

                continue;
            }

            if ($eachPrice['price'] < $price || $price === null) {
                $price = $eachPrice['price'];
                $basePrice = $eachPrice['basePrice'];
                $adminInfo['selectedPrintType'] = array(
                    'price' => $price,
                    'printTypeID' => $eachPrice['printTypeID'],
                    'workspaceID' => $eachPrice['workspaceID'],
                    'expense' => $expense
                );
                $printTypeID = $eachPrice['printTypeID'];
                $workspaceID = $eachPrice['workspaceID'];
                $expense = $eachPrice['expense'];
                $options = $eachPrice['options'];
                $iconDir = $eachPrice['iconDir'];
                $optionsControllers = $eachPrice['optionsControllers'];
                $attributesInfo = $eachPrice['attributesInfo'];
            } else {
                $adminInfo['notSelectedPrintTypes'][] = array(
                    'price' => $price,
                    'printTypeID' => $eachPrice['printTypeID'],
                    'workspaceID' => $eachPrice['workspaceID'],
                    'expense' => $expense
                );
            }
        }

        $idx = count($this->productsInfo) - 1;
        $this->productsInfo[$idx]['attributes'] = $attributesInfo;
        $this->productsInfo[$idx]['printTypeID'] = $printTypeID;
        $this->productsInfo[$idx]['workspaceID'] = $workspaceID;
        $this->productsInfo[$idx]['thickness'] = $size;

        $activeWorkspaceInfo = $this->getSelectedWorkspaceById($typeID, $printTypeID, $workspaceID);
        $this->productsInfo[$idx]['usePerSheet'] = $activeWorkspaceInfo['uzytkipersheet'];

        $this->adminInfo = $adminInfo;

        $attrDiscount = $basePrice - $price;

        return array(
            'price' => $price,
            'basePrice' => $basePrice,
            'attrDiscount' => $attrDiscount,
            'expense' => $expense,
            'printTypeID' => $printTypeID,
            'workspaceID' => $workspaceID,
            'weight' => $weight,
            'options' => $options,
            'attrPages' => $attributeAmount,
            'volume' => $volume,
            'iconDir' => $iconDir,
            'increaseRealizationTime' => $increaseRealizationTime,
            'oneSide' => $oneSide,
            'optionsControllers' => $optionsControllers,
            'area' => $area['size'],
            'areaNet' => $area['sizeNet']
        );

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

    private function _printTypes($formatID, $volume)
    {
        $printTypes = $this->CalculateStorage->getPrintTypes($formatID);

        foreach ($printTypes as $key => $printType) {
            if ($printType['minVolume'] !== null && $volume < $printType['minVolume']) {
                unset($printTypes[$key]);
            } elseif ($printType['maxVolume'] !== null && $volume > $printType['maxVolume']) {
                unset($printTypes[$key]);
            }

        }

        return $printTypes;
    }

    public function getPrintTypes($formatID)
    {
        return $this->CalculateStorage->getPrintTypes($formatID);
    }

    public function getAllSheets($workspace, $pages, $volume, $oneSide, $printRotated, $doublePage,
                                  $userSelectedUseForSheet, $format)
    {
        $amountPages = $this->CalculateAdapter->getAmountPages($pages, $oneSide, $doublePage);
        if ($amountPages != $pages) {
            $pages = $amountPages;
        }
        $perSheet = null;
        $noRoundSheets = false;
        $formatWidth=0; $formatHeight=0;
        extract($this->getSizeExternal($format));
        switch ($workspace['type']) {
            case 3:
                $sheets = 1;
                break;
            case 2:

                $area = $this->CalculateAdapter->getAreaForRolled($pages, $volume);
                $usedHeight = $this->CalculateAdapter->getUsedHeight(
                    $area,
                    $workspace['width'],
                    $formatWidth,
                    $formatHeight
                );

                $sheets = $this->CalculateAdapter->getSheetsForRolled($usedHeight, $workspace['height']);

                break;
            default:
                $areaPerSheetForStandardResult = $this->CalculateAdapter->getAreaPerSheetForStandard(
                    $workspace['width'],
                    $workspace['height'],
                    $formatWidth,
                    $formatHeight,
                    $format
                );
                $perSheet = $originalPerSheet = $areaPerSheetForStandardResult['max'];
                if( $userSelectedUseForSheet &&
                    $userSelectedUseForSheet < $perSheet ) {
                    $perSheet = $userSelectedUseForSheet;
                }

                if ($perSheet == 0) {
                    return null;
                }

                if (!$printRotated) {

                    $originalSheets = $this->CalculateAdapter->getSheetsForStandard($pages, $originalPerSheet, $volume);
                    $sheets = $this->CalculateAdapter->getSheetsForStandard($pages, $perSheet, $volume);

                    $noRoundSheets = $sheets;
                    $sheets = ceil($sheets);
                    $originalSheets = ceil($originalSheets);

                } else {//print rotated

                    $originalSheets = $this->CalculateAdapter->getSheetsForStandardPrintRotated($pages, $originalPerSheet, $volume);
                    $sheets = $this->CalculateAdapter->getSheetsForStandardPrintRotated($pages, $perSheet, $volume);

                    $noRoundSheets = ($sheets * 2) / 2;
                    $sheets = ceil($sheets * 2) / 2;
                    $originalSheets = ceil($originalSheets * 2) / 2;
                }

                break;
        }

        if( $volume > 1 && $sheets < 1 ) {
            $sheets = 1;
        }

        return compact(
            'sheets',
            'perSheet',
            'noRoundSheets',
            'originalPerSheet',
            'originalSheets',
            'areaPerSheetForStandardResult'
        );

    }

    public function getProjectSheets($workspace, $pages, $oneSide, $printRotated, $doublePage,
                                      $userSelectedUseForSheet, $format)
    {
        $result = $this->getAllSheets(
            $workspace,
            $pages,
            1,
            $oneSide,
            $printRotated,
            $doublePage,
            $userSelectedUseForSheet,
            $format
        );
        return $result;
    }

    private function getArea($volume, $rows, $maxRollLength, $setIncrease, $format)
    {
        $slope = $format['slope'];
        $volume = $this->CalculateAdapter->addSetIncreaseToVolume($volume, $setIncrease, $rows);
        $formatWidth=0; $formatHeight=0;
        extract($this->getSizeExternal($format));
        $size = $this->CalculateAdapter->calculateSize($formatWidth, $formatHeight);
        $sizeNet = $this->CalculateAdapter->calculateSizeNet($formatWidth, $formatHeight, $slope);

        $size *= $volume;
        $sizeNet *= $volume;

        if ($maxRollLength) {
            $length = $this->CalculateAdapter->getLengthForRoll($size, $formatWidth);

            $numberOfRolls = $this->CalculateAdapter->getNumberOfRolls($length, $maxRollLength);

            $rollSlipIncrease = $this->CalculateStorage->getIncrease('rollSlip', $numberOfRolls);

            $size = $this->CalculateAdapter->calculateSizeForRollPrint(
                $size,
                $maxRollLength,
                $formatWidth,
                $rollSlipIncrease
            );

        }
        return array('size' => $size, 'sizeNet' => $sizeNet);
    }

    private function _totalSheetsArea($workspace, $sheets)
    {
        return ($workspace['paperWidth'] / 1000) * ($workspace['paperHeight'] / 1000) * $sheets;

    }

    public function getTotalArea($workspace, $volume, $maxRollLength, $setIncrease, $format)
    {
        $volume = $this->CalculateAdapter->addSetIncreaseToVolumeTotal($volume, $setIncrease);
        $formatWidth=0; $formatHeight=0;
        extract($this->getSizeExternal($format));
        $length = $this->CalculateAdapter->getLengthForTotalArea(
            $formatWidth,
            $formatHeight,
            $workspace['width'],
            $volume
        );

        $length = $this->CalculateAdapter->addPaperHeightForTotalArea($length, $workspace);

        if ($maxRollLength) {
            $numberOfRolls = $this->CalculateAdapter->getNumberOfRollsForTotalArea($length, $maxRollLength);

            $rollSlipIncrease = $this->CalculateStorage->getIncrease('rollSlip', $numberOfRolls);
            $length = $this->CalculateAdapter->addRollSlipIncrease($length, $rollSlipIncrease, $numberOfRolls);

        }

        $totalArea = $this->CalculateAdapter->calculateTotalArea($length, $workspace);

        return $totalArea;

    }

    public function _perimeter($volume, $format)
    {
        $formatWidth=0; $formatHeight=0;
        extract($this->getSizeExternal( $format));

        $formatWidth /= 1000;
        $formatHeight /= 1000;

        $perimeter = $formatWidth * 2 + $formatHeight * 2;
        $perimeter *= $volume;

        return $perimeter;

    }

    private function netPerimeter($volume, $format)
    {
        $formatSlope=$format['slope'];
        $formatWidth=0; $formatHeight=0;
        extract($this->getSizeExternal( $format));
        $width = $formatWidth - ($formatSlope * 2);
        $height = $formatHeight - ($formatSlope * 2);

        $width /= 1000;
        $height /= 1000;

        $perimeter = $width * 2 + $height * 2;
        $perimeter *= $volume;

        return $perimeter;
    }

    private function _uzytki($pages, $volume, $oneSide, $doublePage)
    {
        if ($oneSide && $pages > 2) {
            $uzytki = $pages;
        } else {
            $uzytki = $pages / 2;
        }

        if ($doublePage) {
            $uzytki /= 2;
        }

        return $uzytki * $volume;
    }

    private function _attrPrice($attrID, $optID, $printTypeID, $workspace, $pricelistID, $sheets, $projectSheets,
                                $area, $perimeter, $volume, $attributeAmount, $pages, $size, $uzytki, $totalArea,
                                $totalSheetFolds, $sheetIncrease, $setIncrease, $expense, $groupID, $typeID, $format,
                                $sheetCuts, $totalWeight, &$finalPriceText = [], $paperInfo=[])
    {

        $workspaceID = $workspace['ID'];
        if ($sheetIncrease != false) {
            $sheets += intval($sheetIncrease);
        }

        if ($setIncrease != false) {
            $volume += intval($setIncrease);
            $sheets += intval($setIncrease) * $projectSheets;
        }
        $formatWidth=0; $formatHeight=0;
        extract($this->getSizeExternal( $format));
        if ($formatWidth > $formatHeight) {
            $longSide = $formatWidth;
            $shortSide = $formatHeight;
        } else {
            $longSide = $formatHeight;
            $shortSide = $formatWidth;
        }

        $attr = $this->CalculateStorage->getAttribute($attrID);

        if ($attr['function'] == 'standard') {
            $controllerID = $pricelistID;
        } elseif ($attr['function'] == 'print') {
            $controllerID = $printTypeID;
        } elseif ($attr['function'] == 'paper') {
            $controllerID = $workspaceID;
        } else {
            return array('error' => 'Undefined attrType function');
        }

        $this->PrintShopConfigIncrease->setAttrID($attrID);
        $this->PrintShopConfigIncrease->setOptID($optID);
        $this->PrintShopConfigIncrease->setControllerID($controllerID);


        $increases = $this->_attrIncreases( $sheets, $projectSheets, $groupID, $typeID, $attr,
            $printTypeID, $workspace, $pricelistID,$finalPriceText);

        $sheets = $increases['sheets'];

        $sheetsAfterCut = $sheets * Calculator::getStraightCutsPieces($sheetCuts) + $this->getFoldingSheets($this->partProjectSheets);

        $this->PrintShopConfigPrice->setAttrID($attrID);
        $this->PrintShopConfigPrice->setOptID($optID);
        $this->PrintShopConfigPrice->setControllerID($controllerID);

        $priceTypes = $this->CalculateStorage->getPriceTypes();

        $totalFolds = $sheets * $totalSheetFolds;

        $totalSheetsArea = $this->_totalSheetsArea($workspace, $sheets);

        if (!isset($this->attributesInfo[$attr['ID']]) || !isset($this->attributesInfo[$attr['ID']][$optID])) {
            $this->attributesInfo[$attr['ID']][$optID] = array();
        }

        $attrPages = $attributeAmount;

        $this->attributesInfo[$attr['ID']][$optID]['controllerID'] = $controllerID;
        $this->attributesInfo[$attr['ID']][$optID]['attrPages'] = $attributeAmount;
        $this->attributesInfo[$attr['ID']][$optID]['attrID'] = $attr['ID'];
        $this->attributesInfo[$attr['ID']][$optID]['optID'] = $optID;

        $finalPrice = 0;

        $this->PrintShopConfigDetailPrice->setAttrID($attrID);
        $this->PrintShopConfigDetailPrice->setOptID($optID);
        $this->PrintShopConfigDetailPrice->setControllerID($controllerID);

        if ($attr['function'] == 'standard') {
            $this->PrintShopConfigDetailPrice->setControllerID($pricelistID);
        }

        $detailPrice = $this->CalculateStorage->getDetailPrice();
        $finalPriceText['minPrice'] = $detailPrice['minPrice'];
        if ($detailPrice['excluded']) {
            $this->attributesInfo[$attr['ID']][$optID]['excluded'] = true;
            return null;
        }

        $paperPrice = $this->_paperPrice($attr, $optID, $workspace, $sheets, $expense, $finalPriceText);

        if ($paperPrice) {
            $finalPrice += $paperPrice;
        }

        $loggedUser = $this->Auth->getLoggedUser();
        $discountGroups = false;

        if (sourceApp === 'manager' && $this->getOrderUserID() > 0) {
            $discountGroups = $this->CalculateStorage->getUserDiscountGroups($this->getOrderUserID());
        } else if ($loggedUser) {
            $discountGroups = $this->CalculateStorage->getUserDiscountGroups($loggedUser['ID']);
        }

        $discountPriceTypes = null;

        if ($discountGroups) {
            $this->PrintShopConfigDiscountPrice->setAttrID($attrID);
            $this->PrintShopConfigDiscountPrice->setOptID($optID);
            $this->PrintShopConfigDiscountPrice->setControllerID($controllerID);
            $this->PrintShopConfigDiscountPrice->setDiscountGroups($discountGroups);

            $discountPriceTypes = $this->CalculateStorage->getDiscountPriceTypes();

            if( $discountPriceTypes ) {
                foreach ($discountPriceTypes as $key => $discountPriceType) {
                    $discountPriceTypes[$key]['discounted'] = true;
                }
            }
        }

        if ($discountPriceTypes && !$this->isCountBasePrice()) {
            $priceTypes = $discountPriceTypes;
        }

        $this->setPriceTypes($priceTypes);

        $percentagePrice = array();

        $percentageType = null;

        $option = $this->CalculateStorage->getOption($optID);

        $repeatedOperationsNumberRead = $this->CalculateAdapter->getRepeatedOperationsNumber($workspace, $option);
        $repeatedOperationsNumber=0;
        $formatWidth=0; $formatHeight=0;
        extract($this->getSizeExternal( $format));
        $priceFunctions= [];
        $workUnits = [];
        $devices = [];
        if ($detailPrice['manHours']) {
            $deviceDetails = $this->CalculatorDevices->calculateDeviceDetails($attrID, $optID, $controllerID, $sheets, $totalArea, $perimeter, $volume, $projectSheets, $this->getFullProjectsSheets(), $sheetCuts, $sheetsAfterCut, $totalSheetFolds, $size, $paperInfo['stiffness'], $paperInfo['weight'], $formatWidth, $formatHeight, $pages, $totalWeight, $workspace, $finalPriceText);
            $deviceTime = $deviceDetails['deviceTime'];
            $workUnits = $deviceDetails['workUnits'];
            $devices = $deviceDetails['devices'];
            if ($expense) {
                $finalPrice = $deviceDetails['deviceExpense'];
                $finalPriceText['expense'] = $finalPrice;
            } else {
                $finalPrice = $deviceDetails['devicePrice'];
                if ($detailPrice['minPrice'] !== null && $detailPrice['minPrice'] > $finalPrice) {
                    $finalPrice = $detailPrice['minPrice'];
                }
                $finalPriceText['price'] = "devicePrice " . round($finalPrice / 100, 2);
            }
        }
        else {
            if( $priceTypes ) {

                foreach ($priceTypes as $priceType) {

                    if (in_array($priceType['function'], array('sheet', 'projectSheets')) && $repeatedOperationsNumberRead) {
                        $repeatedOperationsNumber = $repeatedOperationsNumberRead;
                    }
                    $priceFunctions[] = $priceType['function'];
                    $percentage = false;
                    switch ($priceType['function']) {
                        case 'sheet':
                            $resultCalculateSheet = $this->calculateSheet(
                                $sheets,
                                $volume,
                                $attributeAmount,
                                $repeatedOperationsNumberRead
                            );
                            $range = $resultCalculateSheet['range'];
                            $amount = $resultCalculateSheet['amount'];
                            break;
                        case 'set':
                            $resultSet = $this->calculateSet($volume, $attributeAmount);
                            $range = $resultSet['range'];
                            $amount = $resultSet['amount'];
                            break;
                        case 'projectSheets':
                            $range = $amount = $projectSheets;
                            break;
                        case 'squareMeter':
                            $range = $amount = $area['size'];
                            break;
                        case 'squareMeter_cm':
                            $range = $amount = $area['size'] * 10000;
                            break;
                        case 'perimeter':
                            if ($attributeAmount > 1) {
                                $range = $amount = $perimeter * $attributeAmount;
                            } else {
                                $range = $amount = $perimeter;
                            }
                            break;
                        case 'perimeter_cm':
                            if ($attributeAmount > 1) {
                                $range = $amount = $perimeter * $attributeAmount * 100;
                            } else {
                                $range = $amount = $perimeter * 100;
                            }
                            break;
                        case 'allSheetsRangeVolume':
                            $range = $volume;
                            $amount = $sheets;
                            break;
                        case 'allPages':
                            $allPagesResult = $this->calculateAllPages($pages, $volume, $attributeAmount);
                            $range = $allPagesResult['range'];
                            $amount = $allPagesResult['amount'];
                            break;
                        case 'allPagesRangeVolume':
                            $allPagesRangeVolumeResult = $this->calculateAllPagesRangeVolume($pages, $volume, $attributeAmount);
                            $range = $allPagesRangeVolumeResult['range'];
                            $amount = $allPagesRangeVolumeResult['amount'];
                            break;
                        case 'setRangeSheet':
                            $range = $sheets;
                            $amount = $volume;
                            break;
                        case 'setRangeSize':
                            $range = $size;
                            $amount = $volume;
                            break;
                        case 'setMultiplication':
                            $range = $volume;
                            $amount = null;
                            $percentage = true;
                            $percentageType = 1;
                            break;
                        case 'longSide':
                            if ($attributeAmount > 1) {
                                $range = ($longSide * $attributeAmount) / 1000;
                                $amount = ($longSide * $attributeAmount) / 1000 * $volume;
                            } else {
                                $range = $longSide / 1000;
                                $amount = $longSide / 1000 * $volume;
                            }
                            break;
                        case 'longSide_cm':
                            if ($attributeAmount > 1) {
                                $range = ($longSide * $attributeAmount) / 1000*100;
                                $amount = ($longSide * $attributeAmount) / 1000 * $volume*100;
                            } else {
                                $range = $longSide / 1000*100;
                                $amount = $longSide / 1000 * $volume*100;
                            }
                            break;
                        case 'shortSide':
                            if ($attributeAmount > 1) {
                                $range = ($shortSide * $attributeAmount) / 1000;
                                $amount = ($shortSide * $attributeAmount) / 1000 * $volume;
                            } else {
                                $range = $shortSide / 1000;
                                $amount = $shortSide / 1000 * $volume;
                            }
                            break;
                        case 'shortSide_cm':
                            if ($attributeAmount > 1) {
                                $range = ($shortSide * $attributeAmount) / 1000*100;
                                $amount = ($shortSide * $attributeAmount) / 1000 * $volume*100;
                            } else {
                                $range = $shortSide / 1000*100;
                                $amount = $shortSide / 1000 * $volume*100;
                            }
                            break;
                        case 'allAreasLength':

                            $length = (($formatWidth * 2) + ($formatHeight * 2)) / 1000 * ceil($uzytki);

                            if ($attributeAmount > 1) {
                                $length *= $attributeAmount;
                            }
                            $amount = $range = $length;
                            break;
                        case 'allAreasLength_cm':

                            $length = (($formatWidth * 2) + ($formatHeight * 2)) / 1000 * ceil($uzytki);

                            if ($attributeAmount > 1) {
                                $length *= $attributeAmount;
                            }
                            $amount = $range = $length * 100;
                            break;
                        case 'alluzytki':
                            $allUzytkiResult = $this->callculateAllUzytki($uzytki, $attributeAmount);
                            $range = $allUzytkiResult['range'];
                            $amount = $allUzytkiResult['amount'];
                            break;
                        case 'paintRangeVolume':
                            $inkVolumePl = 0;

                            // @TODO check file ink volume

                            $range = $volume;
                            $amount = $inkVolumePl;
                            break;
                        case 'setRangePages':
                            $range = $pages;
                            $amount = $volume;
                            break;
                        case 'totalArea':
                            $range = $amount = $totalArea;
                            break;
                        case 'totalArea_cm':
                            $range = $amount = $totalArea * 10000;
                            break;
                        case 'totalSheetsArea':
                            $range = $amount = $totalSheetsArea;
                            break;
                        case 'totalSheetsArea_cm':
                            $range = $amount = $totalSheetsArea * 10000;
                            break;
                        case 'totalSheetsAreaRangeSheets':
                            $range = $sheets;
                            $amount = $totalSheetsArea;
                            break;
                        case 'totalSheetsAreaRangeSheets_cm':
                            $range = $sheets;
                            $amount = $totalSheetsArea * 10000;
                            break;
                        case 'folds':
                            $range = $amount = $totalFolds + $this->getFoldingSheets($this->partProjectSheets);
                            break;
                        case 'collectingFolds':
                            $maxFolds = $this->getMaxFolds();
                            if ($maxFolds == 3) {
                                $range = $sheetsAfterCut;
                            } elseif ($maxFolds == 2) {
                                $range = $sheetsAfterCut * 2;
                            } elseif ($maxFolds == 1) {
                                $range = $sheetsAfterCut * 4;
                            }
                            $range+=$this->getFoldingSheets($this->partProjectSheets);
                            $amount = $range;
                            break;
                        case 'lengthForWidth':
                            if ($attributeAmount > 1) {
                                $range = ($formatWidth * $attributeAmount) / 1000;
                                $amount = ($formatWidth * $attributeAmount) / 1000 * $volume;
                            } else {
                                $range = $formatWidth / 1000;
                                $amount = $formatWidth / 1000 * $volume;
                            }
                            break;
                        case 'lengthForWidth_cm':
                            if ($attributeAmount > 1) {
                                $range = ($formatWidth * $attributeAmount) / 1000 * 100;
                                $amount = ($formatWidth * $attributeAmount) / 1000 * $volume * 100;
                            } else {
                                $range = $formatWidth / 1000 * 100;
                                $amount = $formatWidth / 1000 * $volume * 100;
                            }
                            break;
                        case 'lengthForHeight':
                            if ($attributeAmount > 1) {
                                $range = ($formatHeight * $attributeAmount) / 1000;
                                $amount = ($formatHeight * $attributeAmount) / 1000 * $volume;
                            } else {
                                $range = $formatHeight / 1000;
                                $amount = $formatHeight / 1000 * $volume;
                            }
                            break;
                        case 'lengthForHeight_cm':
                            if ($attributeAmount > 1) {
                                $range = ($formatHeight * $attributeAmount) / 1000 * 100;
                                $amount = ($formatHeight * $attributeAmount) / 1000 * $volume * 100;
                            } else {
                                $range = $formatHeight / 1000 * 100;
                                $amount = $formatHeight / 1000 * $volume * 100;
                            }
                            break;
                        case 'squareMeterNet':
                            $range = $amount = $area['sizeNet'];
                            break;
                        case 'squareMeterNet_cm':
                            $range = $amount = $area['sizeNet']*10000;
                            break;
                        case 'squareMetersForPages':
                            $range = $amount = $this->calculateSquareForPages($area, $pages);
                            break;
                        case 'squareMetersForPages_cm':
                            $range = $amount = $this->calculateSquareForPages($area, $pages) * 10000;
                            break;
                        case 'setPercentage':
                            $range = $volume;
                            $amount = null;
                            $percentage = true;
                            $percentageType = 2;
                            break;
                        case 'bundle':
                            $resultCalculateBundle = $this->calculateBundle($volume, $attributeAmount);
                            $range = $resultCalculateBundle['range'];
                            $amount = $resultCalculateBundle['amount'];
                            break;
                        case 'package':
                            $resultCalculatePackage = $this->calculatePackage($attributeAmount);
                            $range = $resultCalculatePackage['range'];
                            $amount = $resultCalculatePackage['amount'];
                            break;
                        case 'setVolumes':
                            $resultCalculateSetVolumes = $this->calculateSetVolumes($volume);
                            $range = $resultCalculateSetVolumes['range'];
                            $amount = $resultCalculateSetVolumes['amount'];
                            break;
                        case 'allSheetsVolumes':
                            $range = $volume;
                            $amount = 1;
                            break;
                        case 'net_perimeter':

                            $perimeterContainer = $this->getPerimeterContainer();
                            $netPerimeter = $perimeterContainer['netPerimeter'];

                            if ($attributeAmount > 1) {
                                $range = $amount = $netPerimeter * $attributeAmount;
                            } else {
                                $range = $amount = $netPerimeter;
                            }
                            break;
                        case 'net_perimeter_cm':

                            $perimeterContainer = $this->getPerimeterContainer();
                            $netPerimeter = $perimeterContainer['netPerimeter'];

                            if ($attributeAmount > 1) {
                                $range = $amount = $netPerimeter * $attributeAmount * 100;
                            } else {
                                $range = $amount = $netPerimeter * 100;
                            }
                            break;
                        case 'amount_patterns_sum':

                            $resultCalculateAmountOfPattern = $this->calculateAmountOfPattern($attributeAmount);
                            $range = $resultCalculateAmountOfPattern['range'];
                            $amount = $resultCalculateAmountOfPattern['amount'];

                            break;
                        case 'every_sheet_separate':
                            $range = $this->getFullProjectsSheets();
                            $amount = $sheets;
                            break;
                        case 'amount_patterns_value':
                            $resultCalculateAmountOfPattern = $this->calculateAmountOfPattern($attributeAmount);
                            $range = $resultCalculateAmountOfPattern['range'];
                            $amount = 1;
                            break;
                        case 'cutSharp':
                            $amount = ($workspace['longSideSheets'] + $workspace['shortSideSheets'] + 2) * $sheets;
                            $range = $sheets;
                            break;
                        case 'cutClipping':
                            $amount = (($workspace['longSideSheets'] + $workspace['shortSideSheets'] + 2) * 2 - 4) * $sheets;
                            $range = $sheets;
                            break;
                        case 'weight':
                            $range = $amount = $totalWeight;
                            break;
                        case 'packageWeight':
                            $prices = $this->PrintShopConfigPrice->getByPriceType($priceType['priceType']);
                            if (count($prices) != 1) {
                                throw new Exception('Must be one price for price type packageWeight');
                            }
                            $range = 1;
                            $amount = ceil($totalWeight / $prices[0]['amount']);
                            break;
                        default:
                            throw new Exception('Price type function not set 1');
                            break;
                    }
                    if ($expense) {
                        $price = $this->searchMatchingExpense($range, $priceType);

                        if (!$percentage) {
                            if ($priceType['function'] === 'amount_patterns_sum') {
                                $finalPrice += $price['expense'];
                                $finalPriceText['expense'] = $price['expense'];
                            } else {
                                $finalPrice += $price['expense'] * $amount;
                                $finalPriceText['expense'] = $price['expense'] * $amount;
                            }
                            $finalPrice *= $option['repeatedOperationsCount'];

                        } else {
                            $percentagePrice[] = array(
                                'value' => $price['expense'],
                                'type' => $percentageType
                            );
                        }
                    } else {

                        $price = $this->searchMatchingPrice($range, $volume, $priceType);
                        if ($price) {
                            $finalPriceText['price'] = "ID={$price['ID']} " . round($price['value'] / 100, 2);
                        }
                        if (!$percentage) {
                            if ($priceType['function'] === 'amount_patterns_sum') {
                                $finalPrice += $price['value'];
                            } else {
                                $finalPrice += $price['value'] * $amount;
                            }
                            $finalPrice *= $option['repeatedOperationsCount'];
                        } else {
                            $percentagePrice[] = array(
                                'value' => $price['value'],
                                'type' => $percentageType
                            );
                        }
                    }
                    if ($priceType['function'] === 'projectSheets' && $attrPages) {
                        $finalPrice *= $attrPages;
                    }
                }
            }
            $finalPriceText['startUp'] = $detailPrice['startUp'];
            $finalPriceText['basePrice'] = $detailPrice['basePrice'];
            if ($expense) {
                if ($detailPrice['startUp'] !== null) {
                    $finalPrice += $detailPrice['startUp'];
                }

            } else {
                if ($detailPrice['basePrice'] !== null && !$expense) {
                    $finalPrice += $detailPrice['basePrice'];
                }

                if ($detailPrice['minPrice'] !== null && $detailPrice['minPrice'] > $finalPrice) {
                    $finalPrice = $detailPrice['minPrice'];
                }
            }
            if (!empty($percentagePrice)) {
                foreach ($percentagePrice as $each) {
                    if ($each['type'] == 1) {
                        $finalPrice = $finalPrice * (1 + (doubleval($each['value']) / 100));
                        $finalPriceText['percentage'] = $finalPrice;
                    } elseif ($each['type'] == 2) {
                        $finalPrice = $finalPrice * (doubleval($each['value']) / 100);
                        $finalPriceText['percentage'] = $finalPrice;
                    }
                }
            }
        }

        if (!$expense) {
            $marginSummary = $this->getMargin($pricelistID, $attr, $option, $volume, $sheets, $area['size'], $totalWeight, $perimeter, $groupID, $typeID, $finalPrice);
            $finalPrice *= (1 + $marginSummary['value']);
            $marginsParts=$marginSummary['parts'];
            $this->attributesInfo[$attr['ID']][$optID]['all'] = compact(
                'volume',
                'sheets',
                'sheetsAfterCut',
                'projectSheets',
                'area',
                'perimeter',
                'attrPages',
                'pages',
                'size',
                'longSide',
                'shortSide',
                'uzytki',
                'deviceTime',
                'repeatedOperationsNumber',
                'workUnits',
                'priceFunctions',
                'devices',
                'marginsParts'
            );
        }

        return $finalPrice;

    }

    private function searchMatchingPrice($range, $volume, $priceType)
    {

        if($priceType['function'] == 'amount_patterns_sum' ) {

            if ( array_key_exists('discounted', $priceType) ) {
                $price = $this->PrintShopConfigDiscountPrice->getForAmountPatterns($priceType['priceType'], $range);
            } else {
                $price = $this->PrintShopConfigPrice->getForAmountPatterns($priceType['priceType'], $range);
            }

        } else {

            if ( array_key_exists('discounted', $priceType) ) {
                $price = $this->PrintShopConfigDiscountPrice->customGet($priceType['priceType'], $range);
            } else {
                $price = $this->PrintShopConfigPrice->customGet($priceType['priceType'], $range);
            }

        }


        if ($price && isset($price['discountGroupID'])) {
            $this->setLastUsedDiscountGroup($price['discountGroupID']);
        }

        if ($priceType['function'] == 'setVolumes') {
            if (isset($price['lastRangePrice']) && $price['amount'] < $volume) {
                $price['value'] = $volume * $price['lastRangePrice'];
            }
        } else if ($priceType['function'] == 'allSheetsVolumes') {
            if (isset($price['lastRangePrice']) && $price['amount'] < $volume) {
                $price['value'] = $volume * $price['lastRangePrice'];
            }
        }else if ($priceType['function'] == 'packageWight') {
            $price['value'] *= $range / $price['range'];
        }

        return $price;
    }

    private function searchMatchingExpense($range, $priceType)
    {

        if($priceType['function'] == 'amount_patterns_sum' ) {

            if ( array_key_exists('discounted', $priceType) ) {
                $price = $this->PrintShopConfigDiscountPrice->getExpenseForAmountPatterns($priceType['priceType'], $range);
            } else {
                $price = $this->PrintShopConfigPrice->getExpenseForAmountPatterns($priceType['priceType'], $range);
            }

        } else {
            if ( array_key_exists('discounted', $priceType) ) {
                $price = $this->PrintShopConfigDiscountPrice->getExpense($priceType['priceType'], $range);
            } else {
                $price = $this->PrintShopConfigPrice->getExpense($priceType['priceType'], $range);
            }
        }



        return $price;
    }

    private function _attrIncreases( $sheets, $projectSheets, $groupID, $typeID, $attr, $printTypeID,
                                    $workspace, $pricelistID, &$finalPriceText)
    {

        $increases = $this->CalculateStorage->getConfigIncreaseCluster();

        $relatedIncreases=$this->CalculateStorage->getRelatedConfigIncreases($groupID, $typeID, $attr,
            $printTypeID, $workspace, $pricelistID, $this->attributesInfo);

        if($relatedIncreases && count($relatedIncreases)>0){
            if(!$increases){
                $increases=[];
            }
            $relatedIncreases = array_map(function ($item) {
                $item['related'] = true;
                return $item;
            }, $relatedIncreases);
            $increases=array_merge_recursive($increases, $relatedIncreases);
        }

        if (!$increases || !is_array($increases)) {
            return compact('sheets');
        }
        foreach ($increases as $increase) {
            $ranges = [];
            if ($increase['function'] == 'sheet') {
                $ranges = [[$sheets => 1]];
            } elseif ($increase['function'] == 'sheetForProjectSheet') {
                $partRanges = [];
                for ($i = 0; $i < $projectSheets - (count($this->partProjectSheets) > 0 ? 1 : 0); $i++) {
                    $partRanges[] = $sheets/$projectSheets;
                }
                foreach ($this->partProjectSheets as $part => $partSheets) {
                    $partRanges[] = $partSheets;
                }

                foreach ($partRanges as $partRange) {
                    $ranges[] = [$partRange=>1];
                }

            }
            foreach ($ranges as $range1) {
                $range = array_key_first($range1);
                $amount = $range1[$range];

                $configIncrease = isset($increase['isAdditional']) ?
                    $this->PrintShopConfigIncrease->oneForOption($increase['attrID'], $increase['optID'], $increase['controllerID'], $increase['increaseType'], $range) :
                    $this->CalculateStorage->getConfigIncrease($increase['increaseType'], $range);
                $sheets += floatval($configIncrease['value']) * $amount;
                if ($increase['related']) {
                    $finalPriceText['increase'][] = "{$increase['function']}=" . (floatval($configIncrease['value']) * $amount) . " (related: {$increase['attrID']},{$increase['optID']},{$increase['controllerID']}) range=$range";
                } else {
                    $finalPriceText['increase'][] = "{$increase['function']}=" . (floatval($configIncrease['value']) * $amount) . " range=$range";
                }

            }
        }

        return compact(
            'sheets'
        );
    }

    private function _paperPrice($attr, $optID, $workspace, $sheets, $expense, &$finalPriceText)
    {

        if ($attr['function'] !== 'paper') {
            return false;
        }

        $sheetArea = $workspace['paperWidth'] * $workspace['paperHeight'] / 1000000;

        $allSheetsArea = $sheetArea * $sheets;

        $option = $this->CalculateStorage->getOption($optID);

        $weight = ($option['weight'] / 1000) * $allSheetsArea; //kg

        $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['weightKg'] = $weight;

        $this->PrintShopConfigPaperPrice->setOptID($optID);

        $connect = $this->CalculateStorage->getConnectOption($optID);

        if ($expense) {
            if (!$connect) {
                $result = $this->CalculateStorage->getPaperPrice('expense', $weight);
                $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['expenseForKg'] = $result['expense'];
                $price = $result['expense'] * $weight;
                $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['expense'] = $price;
                $finalPriceText['price']=round($result['expense']/100,2)." * weight=$weight";
            } else {
                $result = $this->CalculateStorage->getPaperPrice('connectExpense', $weight, $connect['connectOptionID']);
                $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['expenseForKg'] = $result['expense'];
                $price = $result['expense'] * $weight;
                $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['expense'] = $price;
                $finalPriceText['price']=round($result['expense']/100,2)." * weight=$weight";
            }

        } else {
            if (!$connect) {
                $result = $this->CalculateStorage->getPaperPrice('price', $weight);
                $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['priceForKg'] = $result['price'];
                $price = $result['price'] * $weight;
                $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['price'] = $price;
                $finalPriceText['price']=round($result['price']/100,2)." * weight=$weight";
            } else {
                $result = $this->CalculateStorage->getPaperPrice('connectPrice', $weight, $connect['connectOptionID']);
                $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['priceForKg'] = $result['value'];
                $price = $result['value'] * $weight;
                $this->attributesInfo[$attr['ID']][$optID]['paperPriceKG']['price'] = $price;
                $finalPriceText['price']=round($result['value']/100,2)." * weight=$weight";
            }

        }

        return $price;
    }

    private function calculateAllPages($pages, $volume, $attributeAmount = NULL)
    {
        $result = array();
        if ($attributeAmount !== NULL) {
            $result['range'] = $result['amount'] = $attributeAmount * $volume;
        } else {
            $result['range'] = $result['amount'] = $pages * $volume;
        }

        return $result;
    }

    private function calculateAllPagesRangeVolume($pages, $volume, $attributeAmount = NULL)
    {
        $result = array();
        $result['range'] = $volume;
        if ($attributeAmount !== NULL) {
            $result['amount'] = $attributeAmount * $volume;
        } else {
            $result['amount'] = $pages * $volume;
        }

        return $result;
    }

    private function calculateSheet($sheets, $volume, $attributeAmount = NULL, $repeatedOperationsNumber = NULL)
    {
        $result = array();

        if ($attributeAmount !== NULL) {
            $result['range'] = $attributeAmount;
            $result['amount'] = $volume * $attributeAmount;
        } else {
            $result['range'] = $sheets;
            $result['amount'] = $sheets;
        }

        if($repeatedOperationsNumber !== NULL && $repeatedOperationsNumber > 0) {
            $result['amount'] *= $repeatedOperationsNumber;
        }

        return $result;
    }

    private function calculateSet($volume, $attributeAmount = NULL)
    {
        $result = array();

        if ($attributeAmount !== NULL) {
            $result['range'] = $result['amount'] = $volume * $attributeAmount;
        } else {
            $result['range'] = $result['amount'] = $volume;
        }

        return $result;
    }

    private function calculateSquareForPages($area, $pages)
    {
        return $area['size'] * $pages;
    }

    private function callculateAllUzytki($uzytki, $attributeAmount = NULL)
    {
        $result = array();

        if (!$attributeAmount) {
            $result['range'] = $result['amount'] = $uzytki;
        } else {
            $result['range'] = $result['amount'] = $uzytki * $attributeAmount;
        }

        return $result;
    }

    private function calculateBundle($volume, $attributeAmount)
    {
        $result = array();

        if ($attributeAmount > 0) {
            $bundleValue = ceil($volume / $attributeAmount);
            if ($bundleValue < 1) {
                $bundleValue = 1;
            }
            $result['range'] = $result['amount'] = $bundleValue;
        } else {
            $result['range'] = $result['amount'] = 1;
        }
        return $result;
    }

    private function calculateAmountOfPattern($attributeAmount)
    {
        if ($attributeAmount > 0) {
            $result['range'] = $result['amount'] = $attributeAmount;
        } else {
            $result['range'] = $result['amount'] = 1;
        }
        return $result;
    }

    private function calculatePackage($attributeAmount)
    {
        $result = array();

        if ($attributeAmount > 0) {
            $result['range'] = $result['amount'] = $attributeAmount;
        } else {
            $result['range'] = $result['amount'] = 1;
        }
        return $result;
    }

    private function calculateSetVolumes($volume)
    {
        $result['amount'] = 1;
        $result['range'] = $volume;

        return $result;
    }

    private function checkAttributesPages($attributePages)
    {

        $aggregateAttributes = array();
        foreach ($attributePages as $tmpAttrID => $tmpAttrPage) {
            $aggregateAttributes[] = $tmpAttrID;
        }

        $attributes = $this->CalculateStorage->getAttributesCluster($aggregateAttributes);

        $aggregateRange = array();

        if ($attributes && is_array($attributes)) {
            foreach ($attributes as $attribute) {
                if ($attribute['rangeID'] > 0) {
                    $aggregateRange[] = $attribute['rangeID'];
                }
            }
        }

        $attributeRanges = $this->CalculateStorage->getAttributeRangesCluster($aggregateRange);

        if (!$attributeRanges || !is_array($attributeRanges)) {
            return false;
        }

        $errors = array();
        foreach ($attributePages as $tmpAttrID => $tmpAttrPage) {

            if ($tmpAttrPage === NULL) {
                continue;
            }

            if (!$attributes[$tmpAttrID]['rangeID']) {
                continue;
            }

            $maxPages = $attributeRanges[$attributes[$tmpAttrID]['rangeID']]['maxPages'];
            $minPages = $attributeRanges[$attributes[$tmpAttrID]['rangeID']]['minPages'];

            if ($tmpAttrPage > $maxPages && $maxPages !== NULL) {
                $errors[] = array(
                    'translate' => $this->LangComponent->translate('maximum_number_of_pages'),
                    'text' => 'Maximum number to attribute exceeded. Max number is: ' . $maxPages,
                    'maximumPages' => $maxPages,
                    'minimumPages' => $minPages
                );
            }
            if ($tmpAttrPage < $minPages && $minPages !== NULL) {
                $errors[] = array(
                    'translate' => $this->LangComponent->translate('minimum_number_of_pages'),
                    'text' => 'Minimal number not achieved. Minimal is: ' . $minPages,
                    'maximumPages' => $maxPages,
                    'minimumPages' => $minPages
                );
            }
        }

        if (empty($errors)) {
            return false;
        }
        return $errors;
    }

    private function checkProductThickness($productOptions, $pages, $doublePage)
    {
        $aggregateOptions = array();
        foreach ($productOptions as $productOption) {
            $aggregateOptions[] = $productOption['optID'];
        }

        $productSize = 0;
        $options = $this->CalculateStorage->getOptionsCluster($aggregateOptions);

        if( is_array($options) ) {
            foreach ($options as $option) {
                if (doubleval($option['sizePage']) > 0) {
                    $productSize += $this->calculateProductThickness($pages, $option['sizePage'], $doublePage);
                }
            }
        }

        if ($productSize <= 0) {
            return false;
        }

        $errors = array();

        foreach ($options as $option) {
            if ($option['minThickness'] > 0 && $productSize < $option['minThickness']) {
                $errors[] = array(
                    'key' => 'minimum_thickness',
                    'text' => 'Thickness: ' . $productSize . '. Minimal thickness not achieved for option ' .
                        $option['ID'] . '. Minimal is: ' . $option['minThickness']
                );
            }
            if ($option['maxThickness'] > 0 && $productSize > $option['maxThickness']) {
                $errors[] = array(
                    'key' => 'maximum_thickness',
                    'text' => 'Thickness: ' . $productSize . '. Maximum thickness exceeded for option ' .
                        $option['ID'] . '. Maximal is: ' . $option['maxThickness']
                );
            }
        }

        if (empty($errors)) {
            return false;
        }

        return $errors;

    }

    public function getSelectedWorkspace()
    {
        $selectedPrintTypeID = $this->getSelectedPrintTypeID($this->adminInfo);
        $selectedPrintTypeIndex = $this->getSelectedPrintTypeIndex($this->adminInfo, $selectedPrintTypeID);

        $selectedWorkspaceID = $this->getSelectedWorkspaceID($this->adminInfo);
        $selectedWorkspaceIndex = $this->getSelectedWorkspaceIndex($this->adminInfo, $selectedPrintTypeIndex, $selectedWorkspaceID);

        return $this->adminInfo['printTypes'][$selectedPrintTypeIndex]['workspaces'][$selectedWorkspaceIndex];
    }

    public function getSelectedWorkspaceById($typeID, $printTypeID, $workspaceID)
    {
        $selectedPrintTypeIndex = $this->getActivePrintTypeIndex($typeID, $printTypeID);
        $selectedWorkspaceIndex = $this->getActiveWorkspaceIndex($typeID, $selectedPrintTypeIndex, $workspaceID);

        $activePrintTypes = $this->getActivePrintTypes();

        return $activePrintTypes[$typeID][$selectedPrintTypeIndex]['workspaces'][$selectedWorkspaceIndex];
    }

    public function addFlagToChangeAttributePrice($data)
    {

        if( !$data || !isset($data['info']) ) {
            return $data;
        }

        foreach ($data['info'] as $infoKey => $info) {
            foreach ($info['printTypes'] as $printTypeKey => $printType) {
                foreach ($printType['workspaces'] as $workspaceKey => $workspace) {
                    foreach ($workspace['attrs'] as $attributeKey => $attribute) {

                        $data['info'][$infoKey]['printTypes'][$printTypeKey]['workspaces']
                        [$workspaceKey]['attrs'][$attributeKey]['changePrice'] = true;
                        $attributePrice = $data['info'][$infoKey]['printTypes'][$printTypeKey]['workspaces']
                        [$workspaceKey]['attrs'][$attributeKey]['attrPrice'];
                        $data['info'][$infoKey]['printTypes'][$printTypeKey]['workspaces']
                        [$workspaceKey]['attrs'][$attributeKey]['attrPriceFormatted'] = $this->Price->getPriceToView($attributePrice);

                    }
                }
            }
        }

        return $data;

    }

    private function getActivePrintTypeIndex($typeID, $ID)
    {
        $activePrintTypes = $this->getActivePrintTypes();
        foreach ($activePrintTypes[$typeID] as $index => $printType) {
            if ($printType['printTypeID'] == $ID) {
                return $index;
            }
        }
        return false;
    }

    private function getActiveWorkspaceIndex($typeID, $printTypeIndex, $ID)
    {
        $activePrintTypes = $this->getActivePrintTypes();
        foreach ($activePrintTypes[$typeID][$printTypeIndex]['workspaces'] as $index => $workspace) {
            if ($workspace['workspaceID'] == $ID) {
                return $index;
            }
        }
        return false;
    }

    private function getSizeExternal($format)
    {
        $binding = $format['binding'];

        $formatWidth = $format['width'];
        if (Calculator::isDoubledPages($format)) {
            $formatWidth *= 2;
        }
        $formatWidth += $format['slopeExternalLeft'];
        $formatWidth += $format['slopeExternalRight'];
        if ($binding == 'sewn') {
            $formatWidth -= 2 * $format['slope'];
        } else if ($binding == 'spiral') {
            $formatWidth +=  $format['slopeExternalLeft'];
            $formatWidth +=  $format['slopeExternalRight'];
        } else if ($format['addRidgeThickness']) {
            $formatWidth += $this->ridgeThickness;
        }
        if ($format['wingtipFront']) {
            $formatWidth += $format['wingtipFront'];
        }
        if ($format['wingtipBack']) {
            $formatWidth += $format['wingtipBack'];
        }
        $formatHeight = $format['height'];
        $formatHeight += $format['slopeExternalTop'];
        $formatHeight += $format['slopeExternalBottom'];

        if ($format['unit'] == 2) {
            $formatWidth *= 10;
            $formatHeight *= 10;
        }
        return ['formatWidth' => $formatWidth, 'formatHeight' => $formatHeight];
    }

    public static function getStraightCutsPieces($cuts)
    {
        return pow(2, $cuts);
    }

    private function calculateRidgeThickness($products, $groupID, $typeID)
    {
        $ridgeThickness = 0;
        $doublePage = $this->CalculateStorage->getDoublePage($groupID, $typeID);
        foreach ($products as $product) {
            foreach ($product['options'] as $attr) {
                $option = $this->CalculateStorage->getOption($attr['optID']);
                if (doubleval($option['sizePage']) > 0) {
                    $this->PrintShopConfigOptionDescription->setOptID($option['ID']);
                    $this->PrintShopConfigOptionDescription->setAttrID($option['attrID']);
                    $ridgeThickness += $this->calculateProductThickness($product['pages'], $option['sizePage'], $doublePage);;
                }
            }
        }
        return $ridgeThickness;
    }

    public static function isDoubledPages($format): bool
    {
        $joining = false;
        if ((isset($format['binding']) && in_array($format['binding'], ['sewn', 'glue', 'spiral'])) || $format['addRidgeThickness']) {
            $joining = true;
        }
        return $joining;
    }

    private function getMargin($priceListTypeID, $attr, $option, $pieces, $sheets, $sqmeters, $kilograms, $meters, $groupID, $typeID, $price)
    {

        $margins = $this->Margin->findMargins($priceListTypeID, $attr['natureID'], $pieces, $sheets, $sqmeters, $kilograms, $meters);
        $margins=array_filter($margins, function($margin)use($groupID, $typeID){
            if($margin['typeID']){
                return $margin['typeID']==$typeID;
            }else if($margin['groupID']){
                return $margin['groupID']==$groupID;
            }else{
                return true;
            }
        });
        usort($margins, function ($a, $b) {
            $counts = array_map(function ($relatedItem) {
                $count = $relatedItem['typeID'] ? 100 : 0;
                $count += $relatedItem['groupID'] ? 10 : 0;
                return $count;
            }, [$a, $b]);
            return $counts[0] == $counts[1] ? 0 : ($counts[0] > $counts[1] ? -1 : 1);
        });
        array_splice($margins,1);
        $sum = array_reduce($margins, function ($all, $item) {
            return $all + $item['percentage'];
        }, 0);
        $parts[$attr['natureID']] = ['value'=>$sum / 100 * $price, 'type'=>'nature'];
        $this->PrintShopConfigOptionDescription->setAttrID($attr['ID']);
        $this->PrintShopConfigOptionDescription->setOptID($option['ID']);
        $descriptionsAll = $this->PrintShopConfigOptionDescription->getForOption();
        $descriptionsAll=array_filter($descriptionsAll,function($item){return $item['name']=='manufacturer' || $item['name']=='supplier';});
        $descriptions = array_map(function ($item) {
            return $item['value'];
        }, $descriptionsAll);
        $supplierMargin=$this->MarginSupplier->findMargin($descriptions);
        if($supplierMargin){
            $parts[$descriptions[0]]=['value'=>$supplierMargin/100 * $price];
        }
        $sum += $supplierMargin;
        return ['value'=>$sum / 100, 'parts'=>$parts];
    }

    private function getPrintTypeIcons($priceLists)
    {
        $iconFolder = 'uploadedFiles/' . companyID . '/priceListIcons/';
        $icons = false;
        $aggregateIcons = array();

        if ($priceLists) {
            foreach ($priceLists as $priceList) {
                if (!in_array($priceList['iconID'], $aggregateIcons) && intval($priceList['iconID']) > 0) {
                    $aggregateIcons[] = $priceList['iconID'];
                }
            }
            $icons = $this->CalculateStorage->getIconsCluster($aggregateIcons);
        }

        if ($icons) {
            foreach ($icons as $key => $icon) {
                $icons[$key]['url'] = STATIC_URL . $iconFolder . $icon['path'];
            }
        }
        return $icons;
    }
    private function getFoldingSheets($partSheets){
        $sum=0;
        foreach($partSheets as $part=>$amount){
            switch($part){
                case '0.125':
                    $sum+= $amount * 8;
                    break;
                case '0.25':
                    $sum+= $amount * 4;
                    break;
                case '0.5':
                    $sum+= $amount * 2;
                    break;
                case '0.33':
                    $sum+= $amount * 3;
                    break;
                default:
                    Debugger::getInstance()->addWarning("No case for part $part");
                    break;
            }
        }
        return $sum;
    }

    private function agregateOptions($attributes): array
    {
        $aggregateOptions=[];
        foreach ($attributes as $attribute) {
            $this->attributesInfo[$attribute['attrID']][$attribute['optID']]['optID'] = $attribute['optID'];
            if ($attribute['optID'] && !in_array($attribute['optID'], $aggregateOptions)) {
                $aggregateOptions[] = $attribute['optID'];
            }
        }
        return $aggregateOptions;
    }

    private function getDimensions($attributes, array $optionsArray,  array $paperInfo, mixed $pages, bool|array $doublePage): array
    {
        $oneSide=false;
        $rollLength=0;
        $maxFolds=0;
        $size=0;
        foreach ($attributes as $attr) {
            $optionsArray[] = $attr['optID'];

            $option = $this->CalculateStorage->getOption($attr['optID']);

            if ($option['oneSide'] == 1) {
                $oneSide = true;
            }

            if (doubleval($option['sizePage']) > 0) {//TODO check attr type paper
                $paperInfo['weight'] = $option['weight'];
                $this->PrintShopConfigOptionDescription->setOptID($option['ID']);
                $this->PrintShopConfigOptionDescription->setAttrID($option['attrID']);
                $paperInfo['stiffness'] = $this->PrintShopConfigOptionDescription->getByTypeName('stiffness');
                $size += $this->calculateProductThickness($pages, $option['sizePage'], $doublePage);
            }
            if ($option['rollLength'] > 0) {
                $rollLength = $option['rollLength'];
            }

            if (isset($option['maxFolds']) && $option['maxFolds'] !== null) {
                $maxFolds = $option['maxFolds'];
            }

            $this->setMaxFolds($maxFolds);

        }
        return array( $oneSide, $paperInfo, $size, $rollLength, $maxFolds);
    }

    private function agregateFromPrintType(array $printTypes, array $aggregatePriceLists, array $aggregateWorkspaces, array $aggregatePrintTypes): array
    {
        foreach ($printTypes as $printType) {
            if (!in_array($printType['pricelistID'], $aggregatePriceLists)) {
                $aggregatePriceLists[] = $printType['pricelistID'];
            }
            if ($printType['workspaceID'] && !in_array($printType['workspaceID'], $aggregateWorkspaces)) {
                $aggregateWorkspaces[] = $printType['workspaceID'];
            }
            if ($printType['printTypeID'] && !in_array($printType['printTypeID'], $aggregatePrintTypes)) {
                $aggregatePrintTypes[] = $printType['printTypeID'];
            }
        }
        return array($aggregatePriceLists, $aggregateWorkspaces, $aggregatePrintTypes);
    }

    private function getWorkspaces(mixed $printType): array|bool
    {
        if ($printType['workspaceID']) {
            $workspace4pt = $this->CalculateStorage->getWorkspace($printType['workspaceID']);
            $workspace4pt['workspaceID'] = $workspace4pt['ID'];
            $workspaces = [$workspace4pt];
        } else {
            $workspaces = $this->CalculateStorage->getWorkspacesCluster($printType['printTypeID']);
        }
        return $workspaces;
    }

    private function initPrintTypeInfo(mixed $printType, $priceLists, bool|array $printTypeIcons, mixed $size, mixed $volume): array
    {
        $printTypeInfo=[];
        $printTypeInfo['name'] = $printType['name'];
        $printTypeInfo['printTypeID'] = $printType['printTypeID'];
        $printTypeInfo['priceListIcon'] = null;
        $printTypeInfo['priceLists'] = null;

        if ($priceLists) {
            $selectedPriceList = $priceLists;
            if ($printTypeIcons[$selectedPriceList['iconID']]) {
                $selectedPriceList['icon'] = $printTypeIcons[$selectedPriceList['iconID']];
            }
            $printTypeInfo['priceLists'] = $selectedPriceList;
        }
        if ($printTypeIcons[$printType['priceListIconID']]) {
            $printTypeInfo['priceListIcon'] = $printTypeIcons[$printType['priceListIconID']];
        }

        $printTypeInfo['size'] = $size;

        $printTypeInfo['volume'] = $volume;
        return $printTypeInfo;
    }

    private function modifyRowsToFormat($formatRows, mixed $volume): array
    {
        $rows = 1;
        if ($formatRows > 1) {
            $rows = intval($formatRows);
            $volume = ceil($volume / $rows);
        }
        return array($rows, $volume);
    }

    private function selectUseForSheet(int $printRotated, array $workspaceInfo, $usePerSheet): array
    {
        $selectedUseForSheet=false;
        if ($this->getUserSelectedUseForSheet()
            && $this->getUserSelectedUseForSheet() % 2 != 0
            && $printRotated) {
            $perSheetOdd = $this->getUserSelectedUseForSheet();
            if ($perSheetOdd < 2) {
                $this->setUserSelectedUseForSheet(2);
            } else {
                $this->setUserSelectedUseForSheet($perSheetOdd - 1);
            }
            $workspaceInfo['perSheetOddInRotatedPrinting'] = $perSheetOdd;
        }

        if ($usePerSheet &&
            $usePerSheet > 0) {
            $selectedUseForSheet = $usePerSheet;
        }

        if ($this->getUserSelectedUseForSheet() &&
            $this->getUserSelectedUseForSheet() > 0) {
            $selectedUseForSheet = $this->getUserSelectedUseForSheet();
        }
        return array($workspaceInfo, $selectedUseForSheet);
    }
}
