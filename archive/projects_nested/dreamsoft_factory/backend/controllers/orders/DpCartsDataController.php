<?php

use DreamSoft\Controllers\Components\CalcDelivery;
use DreamSoft\Controllers\Components\Calculation;
use DreamSoft\Controllers\Components\Filter;
use DreamSoft\Controllers\Components\InvoiceComponent;
use DreamSoft\Controllers\Components\LangComponent;
use DreamSoft\Controllers\Components\Mail;
use DreamSoft\Controllers\Components\Payu;
use DreamSoft\Controllers\Components\Price;
use DreamSoft\Controllers\Components\RealizationTimeComponent;
use DreamSoft\Models\Address\Address;
use DreamSoft\Models\Address\AddressUser;
use DreamSoft\Models\Coupon\Coupon;
use DreamSoft\Models\Coupon\CouponOrder;
use DreamSoft\Models\Currency\CurrencyRoot;
use DreamSoft\Models\CustomProduct\CustomProduct;
use DreamSoft\Models\Delivery\Delivery;
use DreamSoft\Models\Delivery\DeliveryName;
use DreamSoft\Models\Domain\Domain;
use DreamSoft\Models\Lang\LangSetting;
use DreamSoft\Models\Module\Module;
use DreamSoft\Models\Order\DpOrderAddress;
use DreamSoft\Models\Order\DpOrderAddressProduct;
use DreamSoft\Models\Order\DpPaymentRemind;
use DreamSoft\Models\Order\DpProductFile;
use DreamSoft\Models\Order\OrderMessage;
use DreamSoft\Models\Order\OrderStatus;
use DreamSoft\Models\Order\OrderStatusLang;
use DreamSoft\Models\PrintShop\PrintShopRealizationTime;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopUser\UserDeliveryPrice;
use DreamSoft\Models\Reclamation\Reclamation;
use DreamSoft\Models\Order\FileReminder;
use DreamSoft\Libs\TwigExtensions\TranslateExtension;
use DreamSoft\Libs\Tinkoff\TinkoffMerchantAPI;
use DreamSoft\Controllers\Components\PaymentAssistant;
use DreamSoft\Controllers\Components\Acl;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeLanguage;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Models\Payment\Payment;
use DreamSoft\Controllers\Components\ProductionPath;
use DreamSoft\Controllers\Components\RouteAssistant;
use DreamSoft\Models\Currency\Currency;
use DreamSoft\Models\Template\TemplateSetting;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;
use Voronkovich\SberbankAcquiring\Client as SberbankClient;
use Voronkovich\SberbankAcquiring\Currency as SberbankCurrency;
use Voronkovich\SberbankAcquiring\OrderStatus as SberbankOrderStatus;
use PayPalCheckoutSdk\Core\PayPalHttpClient;
use PayPalCheckoutSdk\Core\SandboxEnvironment;
use PayPalCheckoutSdk\Core\ProductionEnvironment;
use PayPalCheckoutSdk\Orders\OrdersCreateRequest;
use PayPalCheckoutSdk\Orders\OrdersGetRequest;
use DreamSoft\Models\Mongo\MgSession;
use DreamSoft\Models\Mongo\MgCart;
use MongoDB\BSON\ObjectId as ObjectId;
use DreamSoft\Models\Order\DpOrder;
use DreamSoft\Models\Order\DpCartsData;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Models\Order\DpInvoice;
use DreamSoft\Models\Product\ProductCategory;
use DreamSoft\Models\Tax\Tax;
use DreamSoft\Models\PrintShop\PrintShopComplex;
use DreamSoft\Models\Price\BasePrice;
use Twig\Loader\FilesystemLoader;
use Twig\Environment as Twig_Environment;
use DreamSoft\Controllers\Components\DeliveryAssistant;
use DreamSoft\Models\Payment\PaymentContent;
use DreamSoft\Models\Setting\Setting;
use DreamSoft\Core\Controller;
use DreamSoft\Models\User\User;
use DreamSoft\Models\User\UserOption;

class DpCartsDataController extends Controller
{

    public $useModels = array();
    /**
     * @var Domain
     */
    private $Domain;
    /**
     * @var DpOrder
     */
    protected $DpOrder;
    /**
     * @var DpCartsData
     */
    protected $DpCartsData;

    /**
     * @var DpProduct
     */
    protected $DpProduct;

    /**
     * @var DpOrderAddress
     */
    protected $DpOrderAddress;

    /**
     * @var DpOrderAddressProduct
     */
    protected $DpOrderAddressProduct;

    /**
     * @var DpPaymentRemind
     */
    protected $DpPaymentRemind;

    /**
     * @var BasePrice
     */
    protected $BasePrice;

    /**
     * @var User
     */
    protected $User;

    /**
     * @var Address
     */
    protected $Address;

    /**
     * @var UserCalc
     */
    protected $UserCalc;
    /**
     * @var UserCalcProduct
     */
    protected $UserCalcProduct;
    /**
     * @var PrintShopType
     */
    protected $PrintShopType;

    /**
     * @var PrintShopTypeLanguage
     */
    protected $PrintShopTypeLanguage;

    /**
     * @var MgSession
     */
    protected $MgSession;

    /**
     * @var MgCart
     */
    protected $MgCart;

    /**
     * @var ProductCategory
     */
    protected $ProductCategory;

    /**
     * @var PrintShopRealizationTime
     */
    protected $PrintShopRealizationTime;

    /**
     * @var DeliveryName
     */
    protected $DeliveryName;

    /**
     * @var Payment
     */
    protected $Payment;

    /**
     * @var Module
     */
    protected $Module;

    /**
     * @var OrderStatus
     */
    protected $OrderStatus;

    /**
     * @var OrderStatusLang
     */
    protected $OrderStatusLang;

    /**
     * @var UserDeliveryPrice
     */
    protected $UserDeliveryPrice;

    /**
     * @var Currency
     */
    protected $Currency;

    /**
     * @var CurrencyRoot
     */
    protected $CurrencyRoot;

    /**
     * @var Setting
     */
    protected $Setting;

    /**
     * @var Calculation
     */
    protected $Calculation;

    /**
     * @var Acl
     */
    protected $Acl;

    /**
     * @var Price
     */
    protected $Price;

    /**
     * @var Mail
     */
    protected $Mail;

    /**
     * @var Filter
     */
    protected $Filter;

    /**
     * @var CalcDelivery
     */
    protected $CalcDelivery;

    /**
     * @var ProductionPath
     */
    protected $ProductionPath;
    /**
     * @var RealizationTimeComponent
     */
    protected $RealizationTimeComponent;

    /**
     * @var PayU
     */
    protected $PayU;

    /**
     * @var CouponOrder
     */
    protected $CouponOrder;

    /**
     * @var Coupon
     */
    protected $Coupon;

    /**
     * @var Tax
     */
    protected $Tax;

    /**
     * @var DpInvoice
     */
    protected $DpInvoice;

    /**
     * @var AddressUser
     */
    protected $AddressUser;

    /**
     * @var InvoiceComponent
     */
    protected $InvoiceComponent;

    /**
     * @var UserOption
     */
    protected $UserOption;

    /**
     * @var Reclamation
     */
    protected $Reclamation;

    /**
     * @var OrderMessage
     */
    protected $OrderMessage;

    /**
     * @var Delivery
     */
    protected $Delivery;
    /**
     * @var TemplateSetting
     */
    protected $TemplateSetting;
    /**
     * @var FileReminder
     */
    protected $FileReminder;
    /**
     * @var DpProductFile
     */
    protected $DpProductFile;
    /**
     * @var CustomProduct
     */
    protected $CustomProduct;
    /**
     * @var PaymentAssistant
     */
    protected $PaymentAssistant;
    /**
     * @var LangComponent
     */
    protected $LangComponent;
    /**
     * @var PrintShopComplex
     */
    protected $PrintShopComplex;
    /**
     * @var RouteAssistant
     */
    private $RouteAssistant;
    /**
     * @var LangSetting
     */
    private $LangSetting;
    /**
     * @var DeliveryAssistant
     */
    private $DeliveryAssistant;
    /**
     * @var PaymentContent
     */
    private $PaymentContent;

    protected $calculations;
    protected $basePrices;
    protected $orderCurrency;
    protected $deliveryPrices;
    protected $langNames;
    protected $formatNames;
    protected $configs = array();

    /**
     * DpOrdersController constructor.
     * @param array $params
     */
    public function __construct($params)
    {
        parent::__construct($params);
        $this->DpOrder = DpOrder::getInstance();
        $this->DpCartsData = DpCartsData::getInstance();
        $this->User = User::getInstance();
        $this->DpProduct = DpProduct::getInstance();
    }

    /**
     *
     */
    public function setConfigs()
    {
        $this->configs = array(
            'ID' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'ID', 'sign' => $this->Filter->signs['li']),
            'ready' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'ready', 'sign' => $this->Filter->signs['e']),
            'isOffer' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'isOffer', 'sign' => $this->Filter->signs['e']),
            'isOrder' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'isOrder', 'sign' => $this->Filter->signs['e']),
            'sellerID' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'sellerID', 'sign' => $this->Filter->signs['e']),
            'dateFrom' => array('type' => 'timestamp', 'table' => 'dp_orders', 'field' => 'created', 'sign' => $this->Filter->signs['gt']),
            'dateTo' => array('type' => 'timestamp', 'table' => 'dp_orders', 'field' => 'created', 'sign' => $this->Filter->signs['lt']),
            'production' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'production', 'sign' => $this->Filter->signs['e']),
            'userID' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'userID', 'sign' => $this->Filter->signs['e']),
            'user' => array('type' => 'string', 'table' => 'user', 'field' => 'user', 'sign' => $this->Filter->signs['li']),
            'paid' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'paid', 'sign' => $this->Filter->signs['e']),
            'status' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'status', 'sign' => $this->Filter->signs['e']),
            'notStatus' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'status', 'sign' => $this->Filter->signs['not']),
            'statusType' => array('type' => 'string', 'table' => 'orderStatuses', 'field' => 'type', 'sign' => $this->Filter->signs['e']),
            'invoiceType' => array('type' => 'string', 'table' => 'invoices', 'field' => 'type', 'sign' => $this->Filter->signs['e']),
            'domainID' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'domainID', 'sign' => $this->Filter->signs['e']),
            'name' => array('type' => 'string', 'table' => 'user', 'join' => 'lastname', 'field' => 'name', 'sign' => $this->Filter->signs['li']),
            'lastname' => array('type' => 'string', 'table' => 'user', 'join' => 'name', 'field' => 'lastname', 'sign' => $this->Filter->signs['li']),
            'telephone' => array('type' => 'string', 'table' => 'address', 'join' => 'nip', 'field' => 'telephone', 'sign' => $this->Filter->signs['li']),
            'nip' => array('type' => 'string', 'table' => 'invoiceAddress', 'join' => 'telephone', 'field' => 'nip', 'sign' => $this->Filter->signs['li']),
            'companyName' => array('type' => 'string', 'table' => 'invoiceAddress', 'field' => 'companyName', 'sign' => $this->Filter->signs['li']),
            'statusTypeList' => array('type' => 'string', 'table' => 'orderStatuses', 'field' => 'type', 'sign' => $this->Filter->signs['in']),
            'customProductExist' => array('type' => 'string', 'table' => 'customProducts', 'field' => 'ID', 'sign' => $this->Filter->signs['gt']),
            'orderFromOffer' => array('type' => 'string', 'table' => 'dp_orders', 'field' => 'offerStatus', 'sign' => $this->Filter->signs['e']),
            'expireDateFrom' => array('type' => 'timestamp', 'table' => 'dp_orders', 'field' => 'expires', 'sign' => $this->Filter->signs['gt']),
            'expireDateTo' => array('type' => 'timestamp', 'table' => 'dp_orders', 'field' => 'expires', 'sign' => $this->Filter->signs['lt']),
            'sellerMail' => array('type' => 'string', 'table' => 'seller', 'field' => 'user', 'sign' => $this->Filter->signs['li']),
        );
    }

    /**
     * @param $domainID
     */
    public function setDomainID($domainID)
    {
        // parent::setDomainID($domainID);
        // $this->User->setDomainID($domainID);
        // $this->Mail->setDomainID($domainID);
        // $this->Payment->setDomainID($domainID);
        // $this->PayU->setDomainID($domainID);
        // $this->Setting->setDomainID($domainID);
        // $this->Currency->setDomainID($domainID);
        // $this->InvoiceComponent->setDomainID($domainID);
        // $this->TemplateSetting->setDomainID($domainID);
        // $this->OrderStatus->setDomainID($domainID);
        // $this->PaymentAssistant->setDomainID($domainID);
        // $this->RouteAssistant->setDomainID($domainID);
        // $this->LangSetting->setDomainID($domainID);
        // $this->DeliveryAssistant->setDomainID($domainID);
        // $this->PaymentContent->setDomainID($domainID);
    }

    /**
     * @return array
     */
    public function getConfigs()
    {
        return $this->configs;
    }

    public function index($userID){
        $orderCart = $this->DpOrder->getLastNullUserOrder($userID);
        if($orderCart){
            $products = $this->DpCartsData->get('orderID', $orderCart['ID'], true);
            return $products;
        }
        return array();
    }

    public function post_index(){

        $singleCart = $this->Data->getAllPost();

            $this->debug("singleCart", $singleCart);
            $calcID = $singleCart['calcID'];
            $orderID = $singleCart['orderID'];
            $productID = $singleCart['productID'];
            $productAddresses = json_encode($singleCart['productAddresses']);
            $userID = $singleCart['userID'];
            $token = '';
            $cartsDataID = $this->DpCartsData->create(
                compact(
                    'calcID',
                    'orderID',
                    'productID',
                    'productAddresses',
                    'userID',
                    'token'
                )
            );     
        
        

        return array('response' => $cartsDataID===false ? false : true);
    }

    public function post_updateAddresses(){

        $singleCart = $this->Data->getAllPost();
        $orderID = $singleCart['orderID'];
        $productID = $singleCart['productID'];
        $productAddresses = json_encode($singleCart['productAddresses']);

        $data['response'] = false;

        if($this->DpCartsData->updateProductAddresses($productID, $orderID, $productAddresses)){
            $data['response'] = true;
        }

        return $data;
    }

    public function patch_updateAddresses(){

        $data = $this->Data->getAllPost();
        $userID = $data['userID'];
        $calcID = $data['calcID'];
        $data['response'] = false;

        if($this->DpCartsData->updateUserCart($calcID, $userID)){
            $data['response'] = true;
        }

        return $data;
    }

    function post_getUserCart(){
        $data = $this->Data->getAllPost();
        $userEmail = $data['email'];
        $domainID = $data['domainID'];

        $User = new User();
        $User->setDomainID($domainID);
        $userInstance = $User->get('user', $userEmail);

        if(!$userInstance){
            return array('response' => true, 'responseType' => 0, 'info' => 'Wrong query!');
        }

        $products = $this->DpCartsData->get('userID', $userInstance['ID'], true);
        if(!$products){
            return array('response' => true, 'responseType' => 1, 'info' => 'No products in cart!');
        }

        $productsArray = array();
        foreach($products as $singleCartData){
            $productsInfo = $this->DpProduct->getProductInfoByCalcID($singleCartData['calcID']);
            $productsArray[] = $productsInfo;
        }

        return array('response' => true, 'responseType' => 3, 'productsInCart' => $productsArray, 'countProductsInCart' => sizeof($productsArray));
    }

}
