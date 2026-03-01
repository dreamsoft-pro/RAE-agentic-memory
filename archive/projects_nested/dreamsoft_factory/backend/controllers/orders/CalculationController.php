<?php

use DreamSoft\Controllers\Components\Calculation;
use DreamSoft\Controllers\Components\Price;
use DreamSoft\Models\Delivery\Delivery;
use DreamSoft\Models\Order\DpOrderAddress;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShopUser\UserCalcProductAttribute;
use DreamSoft\Models\Offer\MultiVolumeOffer;
use DreamSoft\Models\Offer\MultiVolumeOfferCalc;

class CalculationController extends Controller
{
    public $useModels = array();

    protected $Calculation;
    protected $Price;
    protected $UserCalc;
    protected $UserCalcProduct;
    protected $UserCalcProductAttribute;
    private $MultiVolumeOffer;
    private $MultiVolumeOfferCalc;
    private $DpOrderAddress;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Calculation = Calculation::getInstance();
        $this->Price = Price::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->UserCalcProductAttribute = UserCalcProductAttribute::getInstance();
        $this->MultiVolumeOfferCalc = MultiVolumeOfferCalc::getInstance();
        $this->MultiVolumeOffer = MultiVolumeOffer::getInstance();
        $this->DpOrderAddress = DpOrderAddress::getInstance();
    }

    public function setDomainID($domainID)
    {
        $this->Price->setDomainID($domainID);
    }

    public function index($calculationID)
    {
        if ($calculationID) {
            $result = $this->UserCalc->customGet($calculationID);
            if ($result) {
                $output = $this->Calculation->getCalcData(array($result));
                $result = $output[0];
            } else {
                return [];
            }
        } else {
            $user = $this->Auth->getLoggedUser();
            $result = $this->UserCalc->getAllforUser($user['ID']);
            if ($result) {
                $result = $this->Calculation->getCalcData($result);
            } else {
                return [];
            }
        }

        return $result ?: [];
    }


    public function history($baseID)
    {
        if (!$baseID) {
            return $this->sendFailResponse('04');
        }
        $results = $this->UserCalc->getHistory($baseID);
        return $this->Calculation->getCalcData($results);
    }

    public function historyMultiOffer($productID)
    {
        if (!$productID) {
            return $this->sendFailResponse('04');
        }

        $response = [];
        $multiVolumeOffer = $this->MultiVolumeOffer->get('productID', $productID);
        $multiVolumeOfferID = $multiVolumeOffer['ID'];

        $currentMultiOfferVolumes = $this->MultiVolumeOfferCalc->get('multiVolumeOfferID', $multiVolumeOfferID, true);
        foreach ($currentMultiOfferVolumes as &$currentMultiOfferVolume) {
            $userCalc = $this->UserCalc->get('ID', $currentMultiOfferVolume['calcID']);
            $results = $this->UserCalc->getHistory($userCalc['baseID']);
            $results = $this->Calculation->getCalcData($results);
            $response = array_merge($response, $results);
        }

        return $response;
    }

    public function deliveriesHistory($orderID)
    {
        return $this->DpOrderAddress->deliveriesHistory($orderID);
    }
}
