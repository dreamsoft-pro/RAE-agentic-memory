<?php

use DreamSoft\Controllers\Components\CalcDelivery;
use DreamSoft\Controllers\Components\DiscountCalculation;
use DreamSoft\Controllers\Components\Price;
use DreamSoft\Controllers\Components\PromotionCalculation;
use DreamSoft\Controllers\Components\RealizationTimeComponent;
use DreamSoft\Libs\Debugger;
use DreamSoft\Models\CustomProduct\CustomProduct;
use DreamSoft\Models\Order\DpProductFile;
use DreamSoft\Models\Order\OrderMessage;
use DreamSoft\Models\PrintShop\PrintShopRealizationTime;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOption;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopUser\UserCalcProductAttribute;
use DreamSoft\Models\PrintShopUser\UserCalcProductSpecialAttribute;
use DreamSoft\Controllers\Components\Acl;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopProduct\PrintShopVolume;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeTax;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Controllers\Components\CalculateStorage;
use DreamSoft\Models\Currency\Currency;
use DreamSoft\Models\Order\DpOrder;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Models\PrintShopProduct\PrintShopGroup;
use DreamSoft\Models\PrintShopUser\UserDeliveryPrice;
use DreamSoft\Models\Tax\Tax;
use DreamSoft\Models\Price\BasePrice;
use DreamSoft\Core\Controller;
use DreamSoft\Models\Setting\Setting;
use DreamSoft\Models\User\User;
use DreamSoft\Models\Route\RouteLang;
use DreamSoft\Controllers\Components\Calculator;
use DreamSoft\Controllers\Components\ProductionPath;
use DreamSoft\Models\Offer\MultiVolumeOffer;
use DreamSoft\Models\Offer\MultiVolumeOfferCalc;
use DreamSoft\Models\Order\DpCalcFileSet;
use DreamSoft\Models\Order\DpCartsData;

/**
 * Description of CalculateController
 */
class CalculateController extends Controller
{
    /**
     * @var DpCartsData
     */
    protected $DpCartsData;

    /**
     * @var PrintShopConfigOption
     */
    protected $PrintShopConfigOption;

    public $useModels = array();

    /**
     * $var Acl
     */
    protected $Acl;
    /**
     * @var Calculator
     */
    protected $Calculator;
    /**
     * @var RealizationTimeComponent
     */
    protected $RealizationTimeComponent;
    /**
     * @var Price
     */
    protected $Price;
    /**
     * @var CalcDelivery
     */
    protected $CalcDelivery;

    /**
     * @var PrintShopVolume
     */
    protected $PrintShopVolume;
    /**
     * @var UserCalc
     */
    protected $UserCalc;
    /**
     * @var UserCalcProduct
     */
    protected $UserCalcProduct;
    /**
     * @var UserCalcProductAttribute
     */
    protected $UserCalcProductAttribute;
    /**
     * @var DpProduct
     */
    protected $DpProduct;
    /**
     * @var DpOrder
     */
    protected $DpOrder;
    /**
     * @var PrintShopType
     */
    protected $PrintShopType;
    /**
     * @var Tax
     */
    protected $Tax;
    /**
     * @var Setting
     */
    protected $Setting;
    /**
     * @var PrintShopRealizationTime
     */
    protected $PrintShopRealizationTime;
    /**
     * @var UserDeliveryPrice
     */
    protected $UserDeliveryPrice;
    /**
     * @var DiscountCalculation
     */
    protected $DiscountCalculation;
    /**
     * @var PromotionCalculation
     */
    private $PromotionCalculation;
    /**
     * @var Currency
     */
    protected $Currency;
    /**
     * @var RouteLang
     */
    protected $RouteLang;
    /**
     * @var User
     */
    protected $User;
    /**
     * @var OrderMessage
     */
    protected $OrderMessage;
    /**
     * @var DpProductFile
     */
    protected $DpProductFile;
    /**
     * @var UserCalcProductSpecialAttribute
     */
    protected $UserCalcProductSpecialAttribute;
    /**
     * @var PrintShopGroup
     */
    protected $PrintShopGroup;
    /**
     * @var CustomProduct
     */
    protected $CustomProduct;
    /**
     * @var PrintShopTypeTax
     */
    private $PrintShopTypeTax;
    /**
     * @var CalculateStorage
     */
    private $CalculateStorage;
    /**
     * @var BasePrice
     */
    private $BasePrice;
    /**
     * @var ProductionPath
     */
    private $ProductionPath;
    /**
     * @var MultiVolumeOffer
     */
    private $MultiVolumeOffer;
    /**
     * @var MultiVolumeOfferCalc
     */
    private $MultiVolumeOfferCalc;
    /**
     * @var DpCalcFileSet
     */
    private $DpCalcFileSet;

    protected $adminInfo = array();
    protected $attributesInfo = array();
    protected $productsInfo = array();

    /**
     * CalculateController constructor.
     * @param array $params
     */
    public function __construct($params)
    {
        parent::__construct($params);

        $this->Calculator = Calculator::getInstance();
        $this->Price = Price::getInstance();
        $this->RealizationTimeComponent = RealizationTimeComponent::getInstance();
        $this->Acl = new Acl();
        $this->CalcDelivery = CalcDelivery::getInstance();
        $this->DiscountCalculation = new DiscountCalculation();
        $this->PromotionCalculation = new PromotionCalculation();

        $this->PrintShopVolume = PrintShopVolume::getInstance();

        $this->UserCalc = UserCalc::getInstance();
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->UserCalcProductAttribute = UserCalcProductAttribute::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->DpOrder = DpOrder::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->PrintShopGroup = PrintShopGroup::getInstance();
        $this->Tax = Tax::getInstance();
        $this->Setting = Setting::getInstance();
        $this->PrintShopRealizationTime = PrintShopRealizationTime::getInstance();
        $this->UserDeliveryPrice = UserDeliveryPrice::getInstance();
        $this->Currency = Currency::getInstance();
        $this->RouteLang = RouteLang::getInstance();
        $this->User = User::getInstance();
        $this->OrderMessage = OrderMessage::getInstance();
        $this->DpProductFile = DpProductFile::getInstance();
        $this->UserCalcProductSpecialAttribute = UserCalcProductSpecialAttribute::getInstance();
        $this->CustomProduct = CustomProduct::getInstance();
        $this->PrintShopTypeTax = PrintShopTypeTax::getInstance();
        $this->CalculateStorage = CalculateStorage::getInstance();
        $this->BasePrice = BasePrice::getInstance();
        $this->ProductionPath = ProductionPath::getInstance();
        $this->MultiVolumeOfferCalc = MultiVolumeOfferCalc::getInstance();
        $this->MultiVolumeOffer = MultiVolumeOffer::getInstance();
        $this->DpCalcFileSet = DpCalcFileSet::getInstance();
        $this->DpCartsData = DpCartsData::getInstance();
        $this->PrintShopConfigOption = PrintShopConfigOption::getInstance();
        $this->Setting->setModule('general');
    }

    /**
     * @param $domainID
     */
    public function setDomainID($domainID)
    {
        $this->Price->setDomainID($domainID);
        $this->Calculator->setDomainID($domainID);
        $this->Tax->setDomainID($domainID);
        $this->Setting->setDomainID($domainID);
        $this->PrintShopRealizationTime->setDomainID($domainID);
        $this->Currency->setDomainID($domainID);
        $this->RouteLang->setDomainID($domainID);
        $this->User->setDomainID($domainID);
        $this->DiscountCalculation->setDomainID($domainID);
        $this->PromotionCalculation->setDomainID($domainID);
        $this->PrintShopTypeTax->setDomainID($domainID);
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return mixed
     * @throws Exception
     */
    private function _post_calculate($groupID, $typeID)
    {
        $post = $this->Data->getAllPost();

        $amount = $post['amount'];
        $groupID = $post['groupID'];
        $typeID = $post['typeID'];
        $volume = $post['volume'];
        $products = $post['products'];

        $taxID = $post['taxID'] ?? false;
        $orderUserID = $post['userID'] ?? false;
        $currencyCode = $post['currency'];

        if (!$groupID) {
            $type = $this->PrintShopType->get('ID', $typeID);
            if (!$type) {
                return $this->sendFailResponse('06');
            }
            $groupID = $type['groupID'];
        }

        $actTax = $this->selectActualTax($taxID);

        $loggedUser = $this->Auth->getLoggedUser();

        $formatID = count($products) == 1 ? $products[0]['formatID'] : NULL;

        if ((sourceApp === 'manager' || $orderUserID > 0) || $loggedUser) {
            if (sourceApp === 'manager' || $orderUserID > 0) {
                $this->Calculator->setOrderUserID($orderUserID);
                $this->DiscountCalculation->searchBestDiscounts($orderUserID, $groupID, $typeID, $formatID);
            } else {
                $this->DiscountCalculation->searchBestDiscounts($loggedUser['ID'], $groupID, $typeID, $formatID);
            }
        }

        $this->PromotionCalculation->searchBestPromotions($groupID, $typeID, $formatID);
        $selectedPromotions = $this->PromotionCalculation->getSelectedPromotions();

        $selectedDiscount = $this->DiscountCalculation->getSelectedDiscount();

        $this->Calculator->setSelectedDiscount($selectedDiscount);
        $this->Calculator->setSelectedPromotions($selectedPromotions);

        $currency = $this->Currency->getByCode($currencyCode);

        $this->Calculator->setCurrencyCourse($currency['course']);

        $result = $this->Calculator->calculate($groupID, $typeID, $amount, $volume, $products, $actTax);

        if ($this->Acl->canChangeAttrPrice($loggedUser)) {
            $result = $this->Calculator->addFlagToChangeAttributePrice($result);
        }

        if ($result['correctCalculation'] === true) {
            $result['calculation'] = $this->discountChangePrice($result['calculation'], $actTax);
        }

        $price = $this->Price->getPriceToView($result['calculation']['price']);
        $result['calculation']['price'] = $price;
        $result['calculation']['currency'] = $currency;

        $priceBrutto = $this->Price->getPriceToView($result['calculation']['priceBrutto']);
        $result['calculation']['priceBrutto'] = $priceBrutto;

        $group = $this->PrintShopGroup->customGet($groupID);
        $round = $group['round'] ?? 0;

        $result['calculation'] = $this->roundCalculation($result['calculation'], $actTax, $round);

        return $result;
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return mixed
     * @throws Exception
     */
    public function post_calculate($groupID, $typeID)
    {
        return $this->_post_calculate($groupID, $typeID);
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return mixed
     * @throws Exception
     */
    public function post_calculatePublic($groupID, $typeID)
    {
        return $this->_post_calculate($groupID, $typeID);
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return array
     * @throws Exception
     */
    private function _patch_calculate($groupID, $typeID)
    {
        $post = $this->Data->getAllPost();

        $amount = $post['amount'];
        $groupID = $post['groupID'] ?? NULL;
        $typeID = $post['typeID'] ?? NULL;
        $products = $post['products'];
        $customVolumes = $post['customVolumes'] ?? array();
        $taxID = $post['taxID'] ?? false;
        $currencyCode = $post['currency'];
        $orderUserID = $post['userID'] ?? false;
        $selectedTechnology = $post['selectedTechnology'] ?? false;

        $tax = $this->selectActualTax($taxID);

        $this->PrintShopVolume->setGroupID($groupID);
        $this->PrintShopVolume->setTypeID($typeID);

        $volumes = $this->PrintShopVolume->getAll(true);

        $minVolume = current($volumes);

        $customVolumesArr = array();
        if (!empty($customVolumes)) {
            foreach ($customVolumes as $row) {
                if ($row['volume'] < $minVolume['volume']) {
                    continue;
                }
                $customVolumesArr[] = $row['volume'];
            }
        }

        $volumesArr = array();
        foreach ($volumes as $each) {
            $cKey = array_search($each['volume'], $customVolumesArr);
            if ($cKey) {
                unset($customVolumesArr[$cKey]);
            }
            $volumesArr[] = $each['ID'];
        }

        if (!empty($customVolumesArr)) {
            foreach ($customVolumesArr as $value) {
                $volumes[] = array('volume' => $value, 'active' => true, 'custom' => true);
            }
        }

        $volumesToFormats = $this->PrintShopVolume->volumesHasFormats($volumesArr);

        $formats = array();
        if (!empty($products)) {
            if (count($products) == 1) {
                $product = current($products);
                if (array_key_exists('formatID', $product)) {
                    $formats[] = $product['formatID'];
                }
            } elseif (count($products) > 1) {
                foreach ($products as $p) {
                    $formats[] = $p['formatID'];
                }
            }
        }

        $result = array(
            'volumes' => array(),
            'realisationTimes' => array(),
            'response' => false
        );

        $type = $this->PrintShopType->get('ID', $typeID);
        $customVolume = $this->PrintShopVolume->getCustom();
        $result['customVolume'] = array('custom' => false);
        if ($customVolume != false) {
            $result['volumeInfo'] = array('custom' => true, 'maxVolume' => $type['maxVolume']);
        }

        $this->Calculator->setCustomVolumes($customVolumesArr);

        $currency = $this->Currency->getByCode($currencyCode);

        $this->Calculator->setCurrencyCourse($currency['course']);

        $loggedUser = $this->Auth->getLoggedUser();

        $firstProductFormatID = NULL;
        if (count($products) == 1) {
            if (array_key_exists(0, $products) && array_key_exists('formatID', $products[0])) {
                $firstProductFormatID = $products[0]['formatID'];
            }
        }

        if ($orderUserID && sourceApp === 'manager') {
            $this->DiscountCalculation->searchBestDiscounts($orderUserID, $groupID, $typeID, $firstProductFormatID);
            $this->Calculator->setOrderUserID($orderUserID);
        } else if ($loggedUser) {
            $this->DiscountCalculation->searchBestDiscounts($loggedUser['ID'], $groupID, $typeID, $firstProductFormatID);
        }

        $this->PromotionCalculation->searchBestPromotions($groupID, $typeID, $firstProductFormatID);
        $selectedPromotions = $this->PromotionCalculation->getSelectedPromotions();

        $selectedDiscount = $this->DiscountCalculation->getSelectedDiscount();
        $this->Calculator->setSelectedDiscount($selectedDiscount);
        $this->Calculator->setSelectedPromotions($selectedPromotions);

        $group = $this->PrintShopGroup->customGet($groupID);

        $result['technologies'] = array();

        $this->Calculator->setSelectedTechnology($selectedTechnology);

        $preparedVolumes = $this->filterVolumes($volumes, $formats, $volumesToFormats);
        $this->Calculator->setVolumesContainer($preparedVolumes);

        foreach ($volumes as $each) {
            foreach ($formats as $formatID) {
                if (array_key_exists('ID', $each)
                    && is_array($volumesToFormats)
                    && array_key_exists($each['ID'], $volumesToFormats)
                    && is_array($volumesToFormats[$each['ID']])
                    && !in_array($formatID, $volumesToFormats[$each['ID']])) {
                    continue 2;
                }
            }

            $calculation = $this->Calculator->calculate($groupID, $typeID, $amount, $each['volume'], $products, $tax);

            if (array_key_exists('correctCalculation', $calculation) && $calculation['correctCalculation'] === true) {

                $calculation['calculation'] = $this->discountChangePrice($calculation['calculation'], $tax);

                $price = $this->Price->getPriceToView($calculation['calculation']['price']);
                $calculation['calculation']['price'] = $price;

                $priceBrutto = $this->Price->getPriceToView($calculation['calculation']['priceBrutto']);
                $calculation['calculation']['priceBrutto'] = $priceBrutto;

                if (in_array($each['volume'], $this->Calculator->getCustomVolumes())) {
                    $custom = true;
                } else {
                    $custom = false;
                }

                $calculation = $this->roundRealisationTimePrices($calculation, $typeID, $group['round'], $tax);
                $calculation = $this->checkAmountForBasePrices($calculation, $typeID, $amount);
                sort($calculation['realisationTimes'][$typeID]);

                $result['realisationTimes'] = $calculation['realisationTimes'][$typeID];

                $result['volumes'][] = array(
                    'calculation' => $calculation['calculation'],
                    'volume' => $each['volume'],
                    'custom' => $custom
                );

                $result['technologies'] = $this->searchUsedTechnologies(
                    $selectedTechnology,
                    $calculation['calculation'],
                    $result['technologies']
                );

            } else {
                Debugger::getInstance()->addWarning($calculation['errors'][0]['text']);
            }
        }

        $result['technologies'] = array_values($result['technologies']);

        $round = $group['round'] ?? 0;

        $result['volumes'] = $this->roundRealisationVolumes($result['volumes'], $tax, $round);

        $result['response'] = false;
        if (!empty($result['volumes'])) {
            $result['response'] = true;
        } else {
            Debugger::getInstance()->addWarning("Product volumes list is empty");
        }

        return $result;
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return array
     * @throws Exception
     */
    public function patch_calculate($groupID, $typeID)
    {
        return $this->_patch_calculate($groupID, $typeID);
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return array
     * @throws Exception
     */
    public function patch_calculatePublic($groupID, $typeID)
    {
        return $this->_patch_calculate($groupID, $typeID);
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return mixed
     * @throws Exception
     */
    public function _post_saveCalculation($groupID, $typeID)
    {
        $post = $this->Data->getAllPost();

        $isMultiVolumeOffer = $post['isMultiVolumeOffer'] ?? 0;
        $this->Calculator->setSelectedTechnology($post['selectedTechnology']);
        $orderID = $post['orderID'] ?? false;
        $productID = $post['productID'] ?? false;
        $name = $post['name'] ?? NULL;
        $currencyCode = $post['currency'];
        $files = $post['files'] ?? array();
        $updateReason = $post['updateReason'] ?? false;
        $copyFromID = $post['copyFromID'] ?? false;
        $isQuestion = $post['isQuestion'] ?? 0;
        $uID = $this->Data->getPost('uID');
        $baseID = $this->Data->getPost('baseID');

        $loggedUser = $this->Auth->getLoggedUser();

        if (sourceApp == 'manager' && isset($post['userID']) && intval($post['userID']) > 0) {
            $user = $this->User->getOne($post['userID']);
        } else {
            $user = $loggedUser;
        }

        if (!$orderID && sourceApp != 'manager' && $post['isOffer'] != 1) {
            $cartOrder = $this->DpOrder->getLastNullUserOrder($user['ID']);
            if (!$cartOrder) {
                $orderID = null;
            } else {
                $orderID = $cartOrder['ID'];
            }
        }

        $order = $this->DpOrder->get('ID', $orderID);

        if ($order && $order['paid'] == 1) {
            $orderID = null;
        }

        $amount = $post['amount'] ?? 1;
        $groupID = $post['groupID'];
        $typeID = $post['typeID'];
        $volume = $post['volume'];
        $products = $post['products'];
        $taxID = $post['taxID'] ?? false;
        $realizationTimeID = $post['realizationTimeID'];
        $realizationDate = $post['realizationDate'];
        $productAddresses = $post['productAddresses'];
        $weight = $post['weight'];

        if (!$groupID) {
            $type = $this->PrintShopType->get('ID', $typeID);
            $groupID = $type['groupID'];
        }

        $actTax = $this->selectActualTax($taxID);

        if (!$realizationTimeID) {
            $calculation = $this->Calculator->calculate($groupID, $typeID, $amount, $volume, $products, $actTax);
            $realisationTime = current(current($calculation['realisationTimes']));

            $realizationTimeID = $realisationTime['ID'];
            $realizationDate = $realisationTime['date'];
            if (intval($calculation['moreDayForVolumes'][$volume]) > 0) {
                $actualDate = strtotime($realizationDate);
                $actualDate = strtotime('+' . $calculation['moreDayForVolumes'][$volume] . ' day', $actualDate);
                $realizationDate = date('Y-m-d', $actualDate);
            }
        }

        $result['response'] = false;

        $formatID = count($products) == 1 ? $products[0]['formatID'] : NULL;

        if ($user) {
            $this->DiscountCalculation->searchBestDiscounts($user['ID'], $groupID, $typeID, $formatID);
        }

        $this->PromotionCalculation->searchBestPromotions($groupID, $typeID, $formatID);
        $selectedPromotions = $this->PromotionCalculation->getSelectedPromotions();

        $selectedDiscount = $this->DiscountCalculation->getSelectedDiscount();
        $this->Calculator->setSelectedDiscount($selectedDiscount);
        $this->Calculator->setSelectedPromotions($selectedPromotions);

        $this->Calculator->resetActivePrintTypes();

        $calculation = $this->Calculator->calculate($groupID, $typeID, $amount, $volume, $products, $actTax);

        $this->PrintShopRealizationTime->setGroupID($groupID);
        $this->PrintShopRealizationTime->setTypeID($typeID);
        $this->PrintShopRealizationTime->setVolume($volume);

        if ($realizationTimeID > 0) {
            $realizationTime = $this->PrintShopRealizationTime->getWithDetails($realizationTimeID);

            if ($realizationTime) {
                if (isset($calculation['calculation']['attrDiscount']) && $calculation['calculation']['attrDiscount']) {
                    $priceWithoutDiscount = $calculation['calculation']['oldPrice'] * (1 + ($realizationTime['pricePercentage'] / 100));
                    $newPrice = $priceWithoutDiscount - $calculation['calculation']['attrDiscount'];
                    if ($newPrice < $calculation['calculation']['price']) {
                        $calculation['calculation']['price'] = $newPrice;
                    } else {
                        $calculation['calculation']['price'] = $calculation['calculation']['price'] * (1 + ($realizationTime['pricePercentage'] / 100));
                    }
                } else {
                    $calculation['calculation']['price'] = $calculation['calculation']['price'] * (1 + ($realizationTime['pricePercentage'] / 100));
                }

                if (isset($calculation['calculation']['oldPrice']) && $calculation['calculation']['oldPrice'] > 0) {
                    $calculation['calculation']['oldPrice'] = $calculation['calculation']['oldPrice'] * (1 + ($realizationTime['pricePercentage'] / 100));
                }
            }
        }

        if (isset($calculation['calculation']['oldPrice']) && $calculation['calculation']['oldPrice'] > 0) {
            $calculation['calculation']['calcPrice'] = $calculation['calculation']['oldPrice'];
        } else {
            $calculation['calculation']['calcPrice'] = $calculation['calculation']['price'];
        }

        $isSeller = $loggedUser && $this->Acl->isSeller($loggedUser);

        $price = $this->Data->getPost('price');
        if ($price !== null && $this->Acl->canEditPrice($loggedUser)) {
            $price = $this->Price->getPriceToDb($price);
            $calculation['calculation']['price'] = $price;
            $calculation['calculation']['sellerChangePrice'] = true;
        }

        $currencyEntity = $this->Currency->getByCode($currencyCode);

        $calcID = false;

        try {
            $calcID = $this->_saveCalculation(
                $calculation['products'],
                $calculation['calculation'],
                $baseID,
                $realizationDate,
                $currencyEntity,
                $user['ID'],
                $actTax
            );
        } catch (Exception $e) {
            $sqlError = $e->getCode() == '02' ? $this->UserCalc->getDbError() : '';

            return array(
                'response' => false,
                'info' => $e->getMessage(),
                'errorCode' => $e->getCode(),
                'sqlError' => $sqlError
            );
        }

        if (!$calcID) {
            $result['error'] = 'Save calculation failed ';
            return $result;
        }

        $userDeliveryAggregate = array();
        $newVolumesProductAddresses = array();
        $calcWithoutDelivery = $this->Setting->getValue('calcWithoutDelivery', 'additionalSettings');
        try {
            if (!empty($productAddresses) && is_array($productAddresses)) {
                foreach ($productAddresses as $productAddress) {
                    $params = array();

                    $deliveryPrice = $this->CalcDelivery->countDeliveryPrice(
                        $productAddress['deliveryID'],
                        $productAddress['allVolume'],
                        $volume,
                        $weight,
                        $calculation['calculation']['amount'],
                        $calculation
                    );

                    $params['priceID'] = $this->Price->setBasePrice($deliveryPrice['price'], $deliveryPrice['taxID'], $currencyEntity);
                    $params['calcID'] = $calcID;
                    $params['volume'] = $productAddress['allVolume'];
                    $params['deliveryID'] = $productAddress['deliveryID'];
                    if (array_key_exists('parcelShopID', $productAddress)) {
                        $params['parcelShopID'] = $productAddress['parcelShopID'];
                    }
                    $userDeliveryAggregate[] = $this->UserDeliveryPrice->create($params);
                }

                if (intval($copyFromID) > 0) {
                    $originalProduct = $this->DpProduct->get('ID', $copyFromID);
                    $originalCalc = $this->UserCalc->customGet($originalProduct['calcID']);

                    $volumeDiff = 0;
                    if ($originalCalc['volume'] !== $volume) {
                        $volumeDiff = $volume - $originalCalc['volume'];
                    }

                    $originalDeliveryPrices = $this->UserDeliveryPrice->get('calcID', $originalProduct['calcID'], true);

                    if ($originalDeliveryPrices) {
                        $index = 0;
                        foreach ($originalDeliveryPrices as $originalDeliveryPrice) {
                            if ($index == 0 && $volumeDiff > 0) {
                                $newVolume = $originalDeliveryPrice['volume'] + $volumeDiff;
                            } else if ($volumeDiff < 0) {
                                $volumeDiff = $originalDeliveryPrice['volume'] + $volumeDiff;

                                if ($volumeDiff < 0) {
                                    $newVolumesProductAddresses[$index] = 0;
                                    $index++;
                                    continue;
                                } else {
                                    $newVolume = $volumeDiff;
                                }
                            } else {
                                $newVolume = $originalDeliveryPrice['volume'];
                            }

                            $deliveryPrice = $this->CalcDelivery->countDeliveryPrice(
                                $originalDeliveryPrice['deliveryID'],
                                $newVolume,
                                $newVolume,
                                $weight,
                                $amount,
                                $originalCalc
                            );

                            $originalBasePrice = $this->BasePrice->get('ID', $originalDeliveryPrice['priceID']);

                            $currencyEntity = $this->Currency->getByCode($originalBasePrice['currency']);

                            $newDeliveryPriceParams = $originalDeliveryPrice;
                            $newDeliveryPriceParams['priceID'] = $this->Price->setBasePrice(
                                $deliveryPrice['price'],
                                $deliveryPrice['taxID'],
                                $currencyEntity
                            );

                            $newDeliveryPriceParams['calcID'] = $calcID;
                            $newDeliveryPriceParams['volume'] = $newVolume;
                            $newVolumesProductAddresses[$index] = $newVolume;
                            unset($newDeliveryPriceParams['ID']);

                            $userDeliveryAggregate[] = $this->UserDeliveryPrice->create($newDeliveryPriceParams);
                            $index++;
                        }
                    }
                }
            }
        } catch (Exception $e) {
            $this->debug($e->getMessage());
        }

        $result['calcID'] = $calcID;

        if (!$orderID) {
            $isOrder = 1;
            $isOffer = 0;
            $offerStatus = NULL;
            if (array_key_exists('isOffer', $post) && $post['isOffer'] == 1) {
                $isOffer = 1;
                $isOrder = 0;
                $offerStatus = 1;
            }

            $userID = $user['ID'];
            if ($user['ID'] != $loggedUser['ID']) {
                $sellerID = $loggedUser['ID'];
            }

            $modified = $created = date(DATE_FORMAT);

            $orderID = $this->DpOrder->create(
                compact(
                    'isOrder',
                    'isOffer',
                    'sellerID',
                    'userID',
                    'offerStatus',
                    'modified',
                    'created',
                    'isQuestion'
                )
            );
        }

        $inEditor = $post['inEditor'];

        if (array_key_exists('customProductID', $post) && $post['customProductID']) {
            $customProduct = $this->CustomProduct->get('ID', $post['customProductID']);
            if (!$customProduct['orderID']) {
                $this->CustomProduct->update($customProduct['ID'], 'orderID', $orderID);
            }
        }

        $result['orderID'] = $orderID;

        if ($productID) {
            $this->DpProduct->updateAll($productID, compact('calcID', 'name', 'realizationTimeID', 'inEditor'));
        } else {
            $productID = $this->DpProduct->create(compact('calcID', 'name', 'orderID', 'realizationTimeID', 'isMultiVolumeOffer', 'inEditor'));

            if (array_key_exists('projectID', $post) && $post['projectID']) {
                $this->DpProduct->update($productID, 'projectID', $post['projectID']);
            }
        }

        $insertedFiles = 0;
        if ($productID && !empty($files)) {
            foreach ($files as $file) {
                $params = array();
                $params['isLocal'] = 1;
                $params['productID'] = $productID;
                $nextFileID = $this->DpProductFile->getMaxFileID($productID);
                if (!$nextFileID) {
                    $nextFileID = 1;
                } else {
                    $nextFileID++;
                }
                $params['fileID'] = $nextFileID;
                $params['name'] = $file['name'];
                $params['created'] = date('Y-m-d H:i:s');
                $insertedFileID = $this->DpProductFile->create($params);
                if ($insertedFileID) {
                    $insertedFiles++;
                }
            }
        }

        if ($updateReason) {
            $this->UserCalc->update($calcID, 'updateReason', $updateReason);
        }

        $result['insertedFiles'] = $insertedFiles;

        $allDeliveryPrices = $this->UserDeliveryPrice->getByList($userDeliveryAggregate);
        if ($allDeliveryPrices) {
            foreach ($allDeliveryPrices as $oneDeliveryPrice) {
                $this->UserDeliveryPrice->update($oneDeliveryPrice['ID'], 'productID', $productID);
            }
        }

        $result['productID'] = $productID;

        $homeUrl = $this->RouteLang->getByRoute('home', lang);
        $cartUrl = $this->RouteLang->getByRoute('cart', lang);
        if ($homeUrl && $cartUrl) {
            $result['cartUrl'] = $homeUrl['url'] . $cartUrl['url'];
        }

        if (array_key_exists('orderMessage', $post) && $post['orderMessage']) {
            $messageParams['senderID'] = $loggedUser['ID'];
            $messageParams['orderID'] = $orderID;
            $messageParams['isFirst'] = 1;
            $messageParams['created'] = date('Y-m-d H:i:s');
            $messageParams['content'] = $post['orderMessage'];
            $messageParams['isAdmin'] = 0;

            $messageID = $this->OrderMessage->create($messageParams);
            $result['messageInfoID'] = $messageID;
        }

        $result['response'] = true;
        $result['newVolumesProductAddresses'] = $newVolumesProductAddresses;

        if ($calcID && $baseID && $orderID) {
            $this->ProductionPath->doPath(array(
                'itemID' => $orderID,
                'appVersion' => 1,
                'update' => 1,
                'baseID' => $baseID
            ));
        }

        if ($isMultiVolumeOffer == 1) {
            $multiVolumeOfferID = !$post['multiOfferProductID'] ? $this->MultiVolumeOffer->create(compact('productID')) : $this->MultiVolumeOffer->get('productID', $post['multiOfferProductID'])['ID'];

            $this->MultiVolumeOfferCalc->create(compact('multiVolumeOfferID', 'calcID'));

            $currentMultiOfferVolumes = $this->MultiVolumeOfferCalc->get('multiVolumeOfferID', $multiVolumeOfferID, true);
            foreach ($currentMultiOfferVolumes as &$currentMultiOfferVolume) {
                $userCalc = $this->UserCalc->get('ID', $currentMultiOfferVolume['calcID']);
                $basePrice = $this->BasePrice->get('ID', $userCalc['priceID']);
                $currentMultiOfferVolume['volume'] = $userCalc['volume'];
                $currentMultiOfferVolume['baseCalcID'] = $userCalc['baseID'];
                $currentMultiOfferVolume['calcVer'] = $userCalc['ver'];
                $currentMultiOfferVolume['net_price'] = number_format(str_replace(',', '.', $this->Price->getNumberToView($basePrice['price'])), 2, ',', ' ');
                $currentMultiOfferVolume['gross_price'] = number_format(str_replace(',', '.', $this->Price->getNumberToView($basePrice['grossPrice'])), 2, ',', ' ');
            }
            $result['currentMultiOfferVolumes'] = $currentMultiOfferVolumes;
        }

        if ($post['updateMultiOfferCalc']) {
            $updateMultiOfferCalc = $post['updateMultiOfferCalc'];
            $currentUserCalc = $this->UserCalc->get('ID', $calcID);
            $currentUserCalcBaseID = $currentUserCalc['baseID'];
            $currentMultiOfferVolume = $this->MultiVolumeOfferCalc->get('calcID', $updateMultiOfferCalc);
            $this->MultiVolumeOfferCalc->update($currentMultiOfferVolume['ID'], 'calcID', $calcID);
        }

        if ($post['hasCalcFiles'] && $post['hasCalcFiles'] == true) {
            $calcFileSet = !$user ? $this->DpCalcFileSet->get('ID', $post['notLoggedCalcFilesSetID']) : $this->DpCalcFileSet->getByParams($user['ID'], $typeID, 0);
            if ($calcFileSet !== false) {
                $this->DpCalcFileSet->update($calcFileSet['ID'], 'calcID', $calcID);
            }
        }

        return $result;
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return mixed
     * @throws Exception
     */
    public function post_saveCalculation($groupID, $typeID)
    {
        return $this->_post_saveCalculation($groupID, $typeID);
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return mixed
     * @throws Exception
     */
    public function post_saveCalculationPublic($groupID, $typeID)
    {
        return $this->_post_saveCalculation($groupID, $typeID);
    }

    /**
     * @param $products
     * @param $calculation
     * @param null $baseID
     * @param null $realisationDate
     * @param null $currencyEntity
     * @param null $realizationTimeID
     * @param null $userID
     * @param null $tax
     * @return bool|array
     * @throws Exception
     */
    private function _saveCalculation($products, $calculation, $baseID = null, $realisationDate = NULL,
                                      $currencyEntity = NULL, $userID = NULL, $tax = NULL)
    {
        if (!isset($calculation['amount'])
            || !isset($calculation['groupID'])
            || !isset($calculation['typeID'])
            || !isset($calculation['volume'])) {
            throw new Exception('Bad calculation data', '01');
        }

        $group = $this->PrintShopGroup->customGet($calculation['groupID']);

        $loggedUser = $this->Auth->getLoggedUser();

        if (!$userID) {
            $user = $loggedUser;
            $userID = $user['ID'];
        }

        $sellerChangePrice = $calculation['sellerChangePrice'] ?? false;

        if ($calculation['percentageDiscount'] > 0 && !$sellerChangePrice) {
            $discount = ($calculation['price'] * $calculation['percentageDiscount']) / 100;

            if ($discount > $calculation['attrDiscount']) {
                $calculation['price'] = $calculation['price'] - $discount;
            }
        }

        if (!$tax) {
            $tax = $this->Tax->customGet($this->Setting->getValue('defaultTax', 'general'), 1);
        }

        $calculation['calcPriceID'] = $this->Price->setBasePrice(
            $calculation['calcPrice'],
            $tax['ID'],
            $currencyEntity,
            $group['round'],
            $sellerChangePrice
        );

        $calculation['priceID'] = $this->Price->setBasePrice(
            $calculation['price'],
            $tax['ID'],
            $currencyEntity,
            $group['round'],
            $sellerChangePrice
        );

        if (!$calculation['priceID']) {
            throw new Exception('Save BasePrice error', '03');
        }

        extract($calculation);
        $params = compact('amount', 'groupID', 'typeID', 'volume', 'expense', 'weight', 'priceID', 'calcPriceID', 'realisationDate');

        $calcID = $this->UserCalc->create($params);

        if (!$calcID) {
            throw new Exception('Save UserCalc error', '02');
        }
        $params = array();
        if (!$baseID) {
            $baseID = $calcID;
        } else {
            $version = $this->UserCalc->getMaxVersion($baseID);
            $version++;
            $params['ver'] = $version;
        }

        $params['baseID'] = $baseID;

        $this->UserCalc->updateAll($calcID, $params);

        $specialAttributes = $this->Calculator->getSpecialAttributes();

        $savedSpecialAttributes = 0;

        foreach ($products as $product) {

            $projectSheets = NULL;
            $sheets = NULL;
            $numberOfSquareMeters = NULL;

            $workspace = $this->Calculator->getSelectedWorkspaceById(
                $product['typeID'],
                $product['printTypeID'],
                $product['workspaceID']
            );

            if ($workspace) {
                $projectSheets = $workspace['noRoundedProjectSheets'];
                $sheets = $workspace['sheets'];
                $numberOfSquareMeters = $workspace['area'];
            }

            $params = null;
            extract($product);

            $params = compact(
                'calcID',
                'typeID',
                'groupID',
                'formatID',
                'formatWidth',
                'formatHeight',
                'pages',
                'printTypeID',
                'workspaceID',
                'projectSheets',
                'sheets',
                'numberOfSquareMeters',
                'usePerSheet'
            );

            $format = $this->CalculateStorage->getFormat($params['formatID'], $product);
            if ($format['unit'] == 2) {
                $params['formatWidth'] *= 10;
                $params['formatHeight'] *= 10;
            }
            $params['slope'] = $format['slope'];
            $calcProductID = $this->UserCalcProduct->create($params);
            if (!$calcProductID) {
                return false;
            }
            foreach ($product['attributes'] as $attrID => $options) {
                foreach ($options as $option) {
                    $params = null;
                    $optID = $option['optID'];
                    $optRow = $this->PrintShopConfigOption->get('ID', $optID);
                    $attrID = $option['attrID'];
                    $attrPages = $option['attrPages'];
                    $controllerID = $option['controllerID'];
                    $fileUploadAvailable = $optRow['fileUploadAvailable'];
                    $productAttributeID = $this->UserCalcProductAttribute->create(compact('calcProductID', 'attrID', 'optID', 'attrPages', 'controllerID', 'fileUploadAvailable'));
                    if (!$productAttributeID) {
                        return false;
                    }
                }
            }
            if ($specialAttributes[$product['typeID']]) {
                foreach ($specialAttributes[$product['typeID']] as $specialAttribute) {
                    $params = array();
                    $params['calcProductID'] = $calcProductID;
                    $params['price'] = $this->Price->getPriceToDb($specialAttribute['price']);
                    $params['name'] = $specialAttribute['name'];
                    $params['type'] = $specialAttribute['type'];
                    $params['expense'] = $this->Price->getPriceToDb($specialAttribute['expense']);
                    $params['operatorID'] = $loggedUser['ID'];
                    $params['weight'] = $specialAttribute['weight'];
                    $params['created'] = $params['modified'] = date('Y-m-d H:i:s');
                    $savedCalcSpecialAttributeID = $this->UserCalcProductSpecialAttribute->create($params);
                    if ($savedCalcSpecialAttributeID > 0) {
                        $savedSpecialAttributes++;
                    }
                }
            }
        }

        return $calcID;
    }

    /**
     * @return array
     */
    public function isSeller()
    {
        $user = $this->Auth->getLoggedUser();
        return array('response' => $this->Acl->isSeller($user));
    }

    /**
     * @param $groupID
     * @param $typeID
     * @param $productID
     * @return array
     */
    public function patch_updateName($groupID, $typeID, $productID)
    {
        $name = $this->Data->getPost('name');

        $result = $this->DpProduct->updateAll($productID, compact('name'));

        return array('response' => $result);
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return array
     */
    public function post_possibleTechnologies($groupID, $typeID)
    {
        $post = $this->Data->getAllPost();

        $products = $post['products'];

        $printTypes = array();
        foreach ($products as $product) {
            $printTypes[$product['typeID']] = $this->Calculator->getPrintTypes($product['formatID']);

            foreach ($printTypes[$product['typeID']] as $key => $printType) {
                if ($printType['workspaceID']) {
                    $workspaces = array();
                    $tmp = $this->CalculateStorage->getWorkspace($printType['workspaceID']);
                    $tmp['workspaceID'] = $tmp['ID'];
                    $workspaces[] = $tmp;
                } else {
                    $workspaces = $this->CalculateStorage->getWorkspacesCluster($printType['printTypeID']);
                }

                $printTypes[$product['typeID']][$key]['workspaces'] = $workspaces;
            }
        }

        return $printTypes;
    }

    public function canChangeAttrPrice()
    {
        $user = $this->Auth->getLoggedUser();
        return array('response' => $this->Acl->canChangeAttrPrice($user));
    }

    public function post_getCurrentMultiOfferVolumes()
    {
        $post = $this->Data->getAllPost();

        $productID = $post['productID'];
        $multiVolumeOffer = $this->MultiVolumeOffer->get('productID', $productID);
        $multiVolumeOfferID = $multiVolumeOffer['ID'];

        $currentMultiOfferVolumes = $this->MultiVolumeOfferCalc->get('multiVolumeOfferID', $multiVolumeOfferID, true);
        foreach ($currentMultiOfferVolumes as &$currentMultiOfferVolume) {
            $userCalc = $this->UserCalc->get('ID', $currentMultiOfferVolume['calcID']);
            $basePrice = $this->BasePrice->get('ID', $userCalc['priceID']);
            $currentMultiOfferVolume['volume'] = $userCalc['volume'];
            $currentMultiOfferVolume['baseCalcID'] = $userCalc['baseID'];
            $currentMultiOfferVolume['calcVer'] = $userCalc['ver'];
            $currentMultiOfferVolume['net_price'] = number_format(str_replace(',', '.', $this->Price->getNumberToView($basePrice['price'])), 2, ',', ' ');
            $currentMultiOfferVolume['gross_price'] = number_format(str_replace(',', '.', $this->Price->getNumberToView($basePrice['grossPrice'])), 2, ',', ' ');
        }
        $result['currentMultiOfferVolumes'] = $currentMultiOfferVolumes;
        $result['response'] = true;

        return $result;
    }

    public function post_deleteMultiOffer()
    {
        $post = $this->Data->getAllPost();

        $offerID = $post['ID'];
        $productID = $post['productID'];

        $this->MultiVolumeOfferCalc->delete('ID', $offerID);

        $multiVolumeOffer = $this->MultiVolumeOffer->get('productID', $productID);
        $multiVolumeOfferID = $multiVolumeOffer['ID'];

        $currentMultiOfferVolumes = $this->MultiVolumeOfferCalc->get('multiVolumeOfferID', $multiVolumeOfferID, true);
        foreach ($currentMultiOfferVolumes as &$currentMultiOfferVolume) {
            $userCalc = $this->UserCalc->get('ID', $currentMultiOfferVolume['calcID']);
            $basePrice = $this->BasePrice->get('ID', $userCalc['priceID']);
            $currentMultiOfferVolume['baseCalcID'] = $userCalc['baseID'];
            $currentMultiOfferVolume['volume'] = $userCalc['volume'];
            $currentMultiOfferVolume['calcVer'] = $userCalc['ver'];
            $currentMultiOfferVolume['net_price'] = number_format(str_replace(',', '.', $this->Price->getNumberToView($basePrice['price'])), 2, ',', ' ');
            $currentMultiOfferVolume['gross_price'] = number_format(str_replace(',', '.', $this->Price->getNumberToView($basePrice['grossPrice'])), 2, ',', ' ');
        }
        $result['currentMultiOfferVolumes'] = $currentMultiOfferVolumes;
        $result['response'] = true;

        return $result;
    }

    /**
     * @param $volumes
     * @param $formats
     * @param $volumesToFormats
     * @return array
     */
    private function filterVolumes($volumes, $formats, $volumesToFormats)
    {
        $filteredVolumes = array();
        foreach ($volumes as $each) {
            foreach ($formats as $formatID) {
                if (array_key_exists('ID', $each) &&
                    is_array($volumesToFormats) &&
                    array_key_exists($each['ID'], $volumesToFormats)
                    && is_array($volumesToFormats[$each['ID']])
                    && !in_array($formatID, $volumesToFormats[$each['ID']])) {
                    continue 2;
                }
                $filteredVolumes[] = $each;
            }
        }

        return $filteredVolumes;
    }

    private function selectActualTax($taxID)
    {
        $tax = NULL;
        if (!$taxID) {
            if ($this->Setting->getValue('defaultTax', 'general') > 0) {
                $tax = $this->Tax->customGet($this->Setting->getValue('defaultTax', 'general'), 1);
            } else {
                $tax = array('name' => 'empty', 'value' => 0);
            }
        } else {
            $tax = $this->Tax->customGet($taxID, 1);
        }

        return $tax;
    }

    /**
     * @param $calculation
     * @param $tax
     * @return array
     */
    private function discountChangePrice($calculation, $tax)
    {
        if ($calculation['percentageDiscount'] > 0) {
            $discount = ($calculation['price'] * $calculation['percentageDiscount']) / 100;
            if ($discount > $calculation['attrDiscount']) {
                $calculation['price'] = $calculation['price'] - $discount;
                $calculation['priceBrutto'] = $calculation['price'] * (1 + ($tax['value'] / 100));
            }
        }

        return $calculation;
    }

    /**
     * @param $selectedTechnology
     * @param $calculation
     * @param $technologies
     * @return array
     */
    private function searchUsedTechnologies($selectedTechnology, $calculation, $technologies)
    {
        if (!array_key_exists($calculation['priceLists']['ID'], $technologies)) {
            $technologies[$calculation['priceLists']['ID']] = $calculation['priceLists'];
            if ($selectedTechnology) {
                $technologies[$calculation['priceLists']['ID']]['selected'] = true;
            }
        }

        if (array_key_exists('notSelectedPrintTypes', $calculation) && $calculation['notSelectedPrintTypes']) {
            foreach ($calculation['notSelectedPrintTypes'] as $notSelected) {
                if (!array_key_exists($notSelected['ID'], $technologies)) {
                    $technologies[$notSelected['ID']] = $notSelected;
                    if ($selectedTechnology) {
                        $technologies[$notSelected['ID']]['selected'] = false;
                    }
                }
            }
        }

        return $technologies;
    }

    /**
     * @param $volumes
     * @param $roundType
     * @param $tax
     * @return mixed
     */
    private function roundRealisationVolumes($volumes, $tax, $roundType = 0)
    {
        if ($roundType == 0) {
            return $volumes;
        }

        foreach ($volumes as $key => $volume) {
            if (intval($roundType) == 1) {
                $price = $this->Price->getPriceToDb($volume['calculation']['price']);
                $price = $this->Price->priceRound($price, 0);
                $grossPrice = $price * (1 + ($tax['value'] / 100));
                $volumes[$key]['calculation']['price'] = $this->Price->getPriceToView($price);
                $volumes[$key]['calculation']['priceBrutto'] = $this->Price->getPriceToView($grossPrice);
            } else if (intval($roundType) == 2) {
                $grossPrice = $this->Price->getPriceToDb($volume['calculation']['priceBrutto']);
                $grossPrice = $this->Price->priceRound($grossPrice, 0);
                $price = $grossPrice / (1 + ($tax['value'] / 100));
                $volumes[$key]['calculation']['price'] = $this->Price->getPriceToView($price);
                $volumes[$key]['calculation']['priceBrutto'] = $this->Price->getPriceToView($grossPrice);
            }
        }

        return $volumes;
    }

    private function roundCalculation($calculation, $tax, $roundType = 0)
    {
        if ($roundType == 0) {
            return $calculation;
        }

        if (intval($roundType) == 1) {
            $price = $this->Price->getPriceToDb($calculation['price']);
            $price = $this->Price->priceRound($price, 0);
            $grossPrice = $price * (1 + ($tax['value'] / 100));
            $calculation['price'] = $this->Price->getPriceToView($price);
            $calculation['priceBrutto'] = $this->Price->getPriceToView($grossPrice);
        } else if (intval($roundType) == 2) {
            $grossPrice = $this->Price->getPriceToDb($calculation['priceBrutto']);
            $grossPrice = $this->Price->priceRound($grossPrice, 0);
            $price = $grossPrice / (1 + ($tax['value'] / 100));
            $calculation['price'] = $this->Price->getPriceToView($price);
            $calculation['priceBrutto'] = $this->Price->getPriceToView($grossPrice);
        }

        return $calculation;
    }

    /**
     * @param $calculation
     * @param $typeID
     * @param $roundType
     * @param $tax
     * @return mixed
     */
    private function roundRealisationTimePrices($calculation, $typeID, $roundType, $tax)
    {
        if ($roundType == 0) {
            return $calculation;
        }

        if (!$tax) {
            return $calculation;
        }

        foreach ($calculation['realisationTimes'][$typeID] as $key => $realisationTime) {
            if (empty($realisationTime['volumes'])) {
                continue;
            }
            foreach ($realisationTime['volumes'] as $volumeKey => $volume) {
                if ($roundType == 1) {
                    $price = $this->Price->getPriceToDb($volume['price']);
                    $price = $this->Price->priceRound($price, 0);
                    $grossPrice = $price * (1 + ($tax['value'] / 100));
                    $calculation['realisationTimes'][$typeID][$key]['volumes'][$volumeKey]['price'] = $this->Price->getPriceToView($price);
                    $calculation['realisationTimes'][$typeID][$key]['volumes'][$volumeKey]['priceBrutto'] = $this->Price->getPriceToView($grossPrice);
                } else if ($roundType == 2) {
                    $grossPrice = $this->Price->getPriceToDb($volume['priceBrutto']);
                    $grossPrice = $this->Price->priceRound($grossPrice, 0);
                    $price = $grossPrice / (1 + ($tax['value'] / 100));
                    $calculation['realisationTimes'][$typeID][$key]['volumes'][$volumeKey]['priceBrutto'] = $this->Price->getPriceToView($grossPrice);
                    $calculation['realisationTimes'][$typeID][$key]['volumes'][$volumeKey]['price'] = $this->Price->getPriceToView($price);
                }
            }
        }

        return $calculation;
    }

    /**
     * @param $calculation
     * @param $typeID
     * @param $amount
     * @return mixed
     */
    private function checkAmountForBasePrices($calculation, $typeID, $amount)
    {
        foreach ($calculation['realisationTimes'][$typeID] as $key => $realisationTime) {
            if (empty($realisationTime['volumes'])) {
                continue;
            }

            foreach ($realisationTime['volumes'] as $volumeKey => $volume) {
                $oldPrice = 0;
                if (array_key_exists('oldPrice', $volume)) {
                    $oldPrice = $this->Price->getPriceToDb($volume['oldPrice']);
                }
                $oldPriceBrutto = 0;
                if (array_key_exists('oldPrice', $volume)) {
                    $oldPriceBrutto = $this->Price->getPriceToDb($volume['oldPriceBrutto']);
                }

                if ($amount > 1) {
                    $oldPrice *= $amount;
                    $oldPriceBrutto *= $amount;
                }
                $calculation['realisationTimes'][$typeID][$key]['volumes'][$volumeKey]['oldPrice'] = $this->Price->getPriceToView($oldPrice);
                $calculation['realisationTimes'][$typeID][$key]['volumes'][$volumeKey]['oldPriceBrutto'] = $this->Price->getPriceToView($oldPriceBrutto);
            }
        }

        return $calculation;
    }
}
