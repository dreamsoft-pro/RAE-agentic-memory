<?php

namespace DreamSoft\Controllers\Components;

use DreamSoft\Core\Component;
use DreamSoft\Models\PrintShopProduct\PrintShopVolume;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\Tax\Tax;
use DreamSoft\Models\Currency\Currency;
use DreamSoft\Libs\Auth;
use DreamSoft\Models\PrintShopProduct\PrintShopGroup;
use DreamSoft\Models\Setting\Setting;

/**
 * Class CalculateAssistant
 * @package DreamSoft\Controllers\Components
 */
class CalculateAssistant extends Component
{
    public $useModels = array();

    private $PrintShopVolume;
    private $PrintShopType;
    private $CalculatorCore;
    private $Tax;
    private $Currency;
    private $DiscountCalculation;
    private $Auth;
    private $PromotionCalculation;
    private $PrintShopGroup;
    private $Price;
    private $Setting;

    public function __construct()
    {
        parent::__construct();
        $this->PrintShopVolume = PrintShopVolume::getInstance();
        $this->PrintShopGroup = PrintShopGroup::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->CalculatorCore = Calculator::getInstance();
        $this->DiscountCalculation = new DiscountCalculation();
        $this->Currency = Currency::getInstance();
        $this->PromotionCalculation = new PromotionCalculation();
        $this->Auth = new Auth();
        $this->Price = Price::getInstance();
        $this->Setting = Setting::getInstance();
        $this->Tax = Tax::getInstance();
    }

    public function setDomainID($domainID)
    {
        $this->CalculatorCore->setDomainID($domainID);
        $this->Tax->setDomainID($domainID);
        $this->DiscountCalculation->setDomainID($domainID);
        $this->Currency->setDomainID($domainID);
        $this->PromotionCalculation->setDomainID($domainID);
        $this->Setting->setDomainID($domainID);
    }

    public function prepareRealizationTimes($post)
    {
        $amount = $post['amount'];
        $groupID = $post['groupID'];
        $typeID = $post['typeID'];
        $products = $post['products'];
        $customVolumes = $post['customVolumes'] ?? [];
        $taxID = $post['taxID'] ?? false;
        $currencyCode = $post['currency'];
        $orderUserID = $post['userID'] ?? false;
        $selectedTechnology = $post['selectedTechnology'] ?? false;
        $limitedVolumes = $post['limitedVolumes'] ?? 0;

        $tax = $this->selectActualTax($taxID);

        $this->PrintShopVolume->setGroupID($groupID);
        $this->PrintShopVolume->setTypeID($typeID);

        $volumes = $this->PrintShopVolume->getAll(true);
        $minVolume = current($volumes);

        $customVolumesArr = array_filter($customVolumes, fn($row) => $row['volume'] >= $minVolume['volume']);

        $volumesArr = array_column($volumes, 'ID');
        $customVolumesArr = array_diff($customVolumesArr, array_column($volumes, 'volume'));

        foreach ($customVolumesArr as $value) {
            $volumes[] = ['volume' => $value, 'active' => true, 'custom' => true];
        }

        $volumesToFormats = !empty($volumesArr) ? $this->PrintShopVolume->volumesHasFormats($volumesArr) : [];

        $formats = array_column($products, 'formatID');
        $volumes = $this->filterVolumesByFormats($volumes, $formats, $volumesToFormats);

        if ($limitedVolumes) {
            $volumesManipulator = $this->limitNumberOfVolumes($volumes, $post['activeVolume']);
            $volumes = $volumesManipulator['volumes'];
        }

        $result = [
            'volumes' => [],
            'realisationTimes' => [],
            'response' => false
        ];

        $type = $this->PrintShopType->get('ID', $typeID);
        $customVolume = $this->PrintShopVolume->getCustom();
        $result['customVolume'] = ['custom' => false];
        if ($customVolume) {
            $result['volumeInfo'] = ['custom' => true, 'maxVolume' => $type['maxVolume']];
        }

        $this->CalculatorCore->setCustomVolumes($customVolumesArr);

        $currency = $this->selectActualCurrency($currencyCode);
        $this->CalculatorCore->setCurrencyCourse($currency['course']);

        $loggedUser = $this->Auth->getLoggedUser();

        $firstProductFormatID = count($products) == 1 ? $products[0]['formatID'] : null;

        if ($orderUserID && sourceApp === 'manager') {
            $this->DiscountCalculation->searchBestDiscounts($orderUserID, $groupID, $typeID, $firstProductFormatID);
            $this->CalculatorCore->setOrderUserID($orderUserID);
        } elseif ($loggedUser) {
            $this->DiscountCalculation->searchBestDiscounts($loggedUser['ID'], $groupID, $typeID, $firstProductFormatID);
        }

        $this->PromotionCalculation->searchBestPromotions($groupID, $typeID, $firstProductFormatID);
        $selectedPromotions = $this->PromotionCalculation->getSelectedPromotions();

        $selectedDiscount = $this->DiscountCalculation->getSelectedDiscount();
        $this->CalculatorCore->setSelectedDiscount($selectedDiscount);
        $this->CalculatorCore->setSelectedPromotions($selectedPromotions);

        $group = $this->PrintShopGroup->customGet($groupID);
        $result['technologies'] = [];

        $this->CalculatorCore->setSelectedTechnology($selectedTechnology);

        $preparedVolumes = $this->filterVolumes($volumes, $formats, $volumesToFormats);
        $this->CalculatorCore->setVolumesContainer($preparedVolumes);

        $calculations = [];
        $additionalVolumes = [];

        foreach ($volumes as $each) {
            $calculation = $this->CalculatorCore->calculate($groupID, $typeID, $amount, $each['volume'], $products, $tax);
            $calculation['volume'] = $each['volume'];

            $inactive = [];
            foreach ($calculation['realisationTimes'][$typeID] as $realisationTime) {
                foreach ($realisationTime['volumes'] as $realisationTimeVolume) {
                    if (!$realisationTimeVolume['active']) {
                        $inactive[$realisationTimeVolume['volume']] = ($inactive[$realisationTimeVolume['volume']] ?? 0) + 1;
                    }
                }
            }

            $excludeCalculation = isset($inactive[$each['volume']]) && $inactive[$each['volume']] == count($calculation['realisationTimes'][$typeID]);
            if ($excludeCalculation && isset($volumesManipulator['oldVolumes'][$volumesManipulator['lastIndex'] + 1])) {
                $additionalVolumes[] = $volumesManipulator['oldVolumes'][$volumesManipulator['lastIndex'] + 1];
            }

            if (!$excludeCalculation) {
                $calculations[] = $calculation;
            }
        }

        foreach ($additionalVolumes as $each) {
            $calculation = $this->CalculatorCore->calculate($groupID, $typeID, $amount, $each['volume'], $products, $tax);
            $calculation['volume'] = $each['volume'];
            $calculations[] = $calculation;
        }

        foreach ($calculations as $calculation) {
            if ($calculation['correctCalculation'] === true) {
                $calculation['calculation'] = $this->discountChangePrice($calculation['calculation'], $tax);
                $calculation['calculation']['price'] = $this->Price->getPriceToView($calculation['calculation']['price']);
                $calculation['calculation']['priceBrutto'] = $this->Price->getPriceToView($calculation['calculation']['priceBrutto']);
                $calculation['calculation']['custom'] = in_array($calculation['volume'], $this->CalculatorCore->getCustomVolumes());

                $calculation = $this->roundRealisationTimePrices($calculation, $typeID, $group['round'], $tax);
                $calculation = $this->checkAmountForBasePrices($calculation, $typeID, $amount);
                sort($calculation['realisationTimes'][$typeID]);

                $result['realisationTimes'] = $calculation['realisationTimes'][$typeID];
                $result['volumes'][] = [
                    'calculation' => $calculation['calculation'],
                    'volume' => $calculation['volume'],
                    'custom' => $calculation['calculation']['custom']
                ];

                $result['technologies'] = $this->searchUsedTechnologies(
                    $selectedTechnology,
                    $calculation['calculation'],
                    $result['technologies']
                );
            }
        }

        $result['technologies'] = array_values($result['technologies']);
        $result['volumes'] = $this->roundRealisationVolumes($result['volumes'], $tax, $group['round'] ?? 0);

        $result['tax'] = $tax;
        $result['currency'] = $currency['code'];
        $result['response'] = !empty($result['volumes']);

        return $result;
    }

    private function filterVolumesByFormats($volumes, $formats, $volumesToFormats)
    {
        return array_filter($volumes, function($each) use ($formats, $volumesToFormats) {
            foreach ($formats as $formatID) {
                if (isset($volumesToFormats[$each['ID']]) && !in_array($formatID, $volumesToFormats[$each['ID']])) {
                    return false;
                }
            }
            return true;
        });
    }

    private function limitNumberOfVolumes($volumes, $activeVolume)
    {
        $this->Setting->setModule('general');
        $numberOfVolumes = $this->Setting->getValue('numberOfVolumesInOffer');

        $actualVolumeIndex = array_search($activeVolume, array_column($volumes, 'volume'));

        if ($numberOfVolumes >= (count($volumes) - 1)) {
            $firstIndex = 0;
            $lastIndex = count($volumes) - 1;
        } else {
            $halfOfVolumes = intval($numberOfVolumes) / 2;
            $firstIndex = max(0, $actualVolumeIndex - $halfOfVolumes);
            $lastIndex = min(count($volumes) - 1, $firstIndex + $numberOfVolumes - 1);

            if ($lastIndex - $firstIndex < $numberOfVolumes - 1) {
                $firstIndex = max(0, $lastIndex - $numberOfVolumes + 1);
            }
        }

        return [
            'volumes' => array_slice($volumes, $firstIndex, $lastIndex - $firstIndex + 1),
            'oldVolumes' => $volumes,
            'firstIndex' => $firstIndex,
            'lastIndex' => $lastIndex
        ];
    }

    private function selectActualTax($taxID)
    {
        $this->Setting->setModule('general');
        $defaultTaxID = $this->Setting->getValue('defaultTax');

        return $this->Tax->customGet($taxID ?: $defaultTaxID, 1) ?? ['name' => 'empty', 'value' => 0];
    }

    private function selectActualCurrency($currencyCode)
    {
        $this->Setting->setModule('general');
        $defaultCurrencyID = $this->Setting->getValue('defaultCurrency');

        return $currencyCode
            ? $this->Currency->getByCode($currencyCode)
            : $this->Currency->get('ID', $defaultCurrencyID) ?? ['code' => DEFAULT_CURRENCY, 'course' => 100];
    }

    private function filterVolumes($volumes, $formats, $volumesToFormats)
    {
        return array_filter($volumes, function($each) use ($formats, $volumesToFormats) {
            foreach ($formats as $formatID) {
                if (isset($volumesToFormats[$each['ID']]) && !in_array($formatID, $volumesToFormats[$each['ID']])) {
                    return false;
                }
            }
            return true;
        });
    }

    private function discountChangePrice($calculation, $tax)
    {
        if ($calculation['percentageDiscount'] > 0) {
            $discount = ($calculation['price'] * $calculation['percentageDiscount']) / 100;
            if ($discount > $calculation['attrDiscount']) {
                $calculation['price'] -= $discount;
                $calculation['priceBrutto'] = $calculation['price'] * (1 + ($tax['value'] / 100));
            }
        }

        return $calculation;
    }

    private function roundRealisationTimePrices($calculation, $typeID, $roundType, $tax)
    {
        if ($roundType == 0 || !$tax) {
            return $calculation;
        }

        foreach ($calculation['realisationTimes'][$typeID] as $key => $realisationTime) {
            foreach ($realisationTime['volumes'] as $volumeKey => $volume) {
                $price = $this->Price->getPriceToDb($volume['price']);
                $priceBrutto = $this->Price->getPriceToDb($volume['priceBrutto']);

                if ($roundType == 1) {
                    $price = $this->Price->priceRound($price, 0);
                    $grossPrice = $price * (1 + ($tax['value'] / 100));
                } else {
                    $grossPrice = $this->Price->priceRound($priceBrutto, 0);
                    $price = $grossPrice / (1 + ($tax['value'] / 100));
                }

                $calculation['realisationTimes'][$typeID][$key]['volumes'][$volumeKey]['price'] = $this->Price->getPriceToView($price);
                $calculation['realisationTimes'][$typeID][$key]['volumes'][$volumeKey]['priceBrutto'] = $this->Price->getPriceToView($grossPrice);
            }
        }

        return $calculation;
    }

    private function checkAmountForBasePrices($calculation, $typeID, $amount)
    {
        foreach ($calculation['realisationTimes'][$typeID] as $key => $realisationTime) {
            foreach ($realisationTime['volumes'] as $volumeKey => $volume) {
                $oldPrice = $this->Price->getPriceToDb($volume['oldPrice'] ?? $volume['price']);
                $oldPriceBrutto = $this->Price->getPriceToDb($volume['oldPriceBrutto'] ?? $volume['priceBrutto']);

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

    private function searchUsedTechnologies($selectedTechnology, $calculation, $technologies)
    {
        $techID = $calculation['priceLists']['ID'];

        if (!isset($technologies[$techID])) {
            $technologies[$techID] = $calculation['priceLists'];
            $technologies[$techID]['selected'] = (bool) $selectedTechnology;
        }

        if (!empty($calculation['notSelectedPrintTypes'])) {
            foreach ($calculation['notSelectedPrintTypes'] as $notSelected) {
                if (!isset($technologies[$notSelected['ID']])) {
                    $technologies[$notSelected['ID']] = $notSelected;
                    $technologies[$notSelected['ID']]['selected'] = false;
                }
            }
        }

        return $technologies;
    }

    private function roundRealisationVolumes($volumes, $tax, $roundType = 0)
    {
        if ($roundType == 0) {
            return $volumes;
        }

        foreach ($volumes as $key => $volume) {
            $price = $this->Price->getPriceToDb($volume['calculation']['price']);
            $priceBrutto = $this->Price->getPriceToDb($volume['calculation']['priceBrutto']);

            if ($roundType == 1) {
                $price = $this->Price->priceRound($price, 0);
                $grossPrice = $price * (1 + ($tax['value'] / 100));
            } else {
                $grossPrice = $this->Price->priceRound($priceBrutto, 0);
                $price = $grossPrice / (1 + ($tax['value'] / 100));
            }

            $volumes[$key]['calculation']['price'] = $this->Price->getPriceToView($price);
            $volumes[$key]['calculation']['priceBrutto'] = $this->Price->getPriceToView($grossPrice);
        }

        return $volumes;
    }
}
