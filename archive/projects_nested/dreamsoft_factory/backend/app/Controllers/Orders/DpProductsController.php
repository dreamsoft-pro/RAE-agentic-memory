<?php

namespace DreamSoft\Controllers\Orders;

use DreamSoft\Controllers\Components\Filter;
use DreamSoft\Controllers\Components\LangComponent;
use DreamSoft\Controllers\Components\Mail;
use DreamSoft\Controllers\Components\Price;
use DreamSoft\Controllers\Components\Uploader;
use DreamSoft\Models\Address\Address;
use DreamSoft\Models\Lang\LangSetting;
use DreamSoft\Models\Order\DpOrderAddress;
use DreamSoft\Models\Order\DpOrderAddressProduct;
use DreamSoft\Models\Order\DpProductLabelImposition;
use DreamSoft\Models\Order\DpProductReportFile;
use DreamSoft\Models\PrintShop\LabelImposition;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopUser\UserCalcProductAttribute;
use DreamSoft\Models\PrintShopUser\UserCalcProductFile;
use DreamSoft\Models\PrintShopUser\UserCalcProductSpecialAttribute;
use DreamSoft\Libs\TwigExtensions\TranslateExtension;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Controllers\Components\ProductionPath;
use DreamSoft\Models\ProductionPath\Ongoing;
use DreamSoft\Models\Mongo\MgSession;
use DreamSoft\Models\Order\DpOrder;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Core\Controller;
use DreamSoft\Models\Price\BasePrice;
use DreamSoft\Models\Template\TemplateSetting;
use DreamSoft\Models\Upload\UploadFile;
use Exception;
use DreamSoft\Models\Setting\Setting;
use ImagickException;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;
use Twig\Loader\FilesystemLoader;
use Twig\Environment as Twig_Environment;
use DreamSoft\Models\User\User;
use DreamSoft\Models\User\UserOption;
use DreamSoft\Controllers\Components\ExportImport;
use DreamSoft\Models\Payment\Payment;
use DreamSoft\Models\Payment\PaymentName;
use DreamSoft\Models\Delivery\DeliveryName;
use DreamSoft\Models\Order\DpCartsData;

/**
 * Description of DpProductsController
 *
 * @author Rafał
 */
class DpProductsController extends Controller
{
    /**
     * @var UserCalcProductFile
     */
    protected $UserCalcProductFile;

    public $useModels = array();
    /**
     * @var LangComponent
     */
    private $LangComponent;
    /**
     * @var UploadFile
     */
    private $UploadFile;

    /**
     * @var DpOrder
     */
    protected $DpOrder;
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
     * @var BasePrice
     */
    protected $BasePrice;
    /**
     * @var MgSession
     */
    protected $MgSession;
    /**
     * @var PrintShopType
     */
    protected $PrintShopType;
    /**
     * @var UserCalcProduct
     */
    protected $UserCalcProduct;
    /**
     * @var UserCalcProductAttribute
     */
    protected $UserCalcProductAttribute;

    /**
     * @var Price
     */
    protected $Price;
    /**
     * @var Filter
     */
    protected $Filter;
    /**
     * @var Address
     */
    protected $Address;
    /**
     * @var Mail
     */
    protected $Mail;
    /**
     * @var UserCalc
     */
    protected $UserCalc;
    /**
     * @var User
     */
    protected $User;
    /**
     * @var TemplateSetting
     */
    protected $TemplateSetting;
    /**
     * @var UserCalcProductSpecialAttribute
     */
    protected $UserCalcProductSpecialAttribute;
    /**
     * @var UserOption
     */
    protected $UserOption;
    /**
     * @var ProductionPath
     */
    private $ProductionPath;
    /**
     * @var Ongoing
     */
    private $Ongoing;
    /**
     * @var Setting
     */
    private $Setting;
    /**
     * @var LangSetting
     */
    private $LangSetting;
    /**
     * @var DpProductReportFile
     */
    private $DpProductReportFile;
    /**
     * @var array
     */
    private $configs;
    /**
     * @var ExportImport
     */
    protected $ExportImport;
    /**
     * @var Payment
     */
    protected $Payment;
    /**
     * @var PaymentName
     */
    protected $PaymentName;
    /**
     * @var DeliveryName
     */
    protected $DeliveryName;
    /**
     * @var Uploader
     */
    private $Uploader;
    /**
     * @var DpCartsData
     */
    protected $DpCartsData;
    private $fileFolder;
    /**
     * @var LabelImposition
     */
    private $LabelImposition;
    private DpProductLabelImposition $DpProductLabelImposition;

    public function __construct($params = [])
    {

        parent::__construct($params);

        $this->Price = Price::getInstance();
        $this->Filter = Filter::getInstance();

        $this->DpOrder = DpOrder::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->DpOrderAddress = DpOrderAddress::getInstance();
        $this->BasePrice = BasePrice::getInstance();
        $this->MgSession = MgSession::getInstance();
        $this->DpOrderAddressProduct = DpOrderAddressProduct::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->UserCalcProductAttribute = UserCalcProductAttribute::getInstance();
        $this->Address = Address::getInstance();
        $this->Mail = Mail::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->User = User::getInstance();
        $this->TemplateSetting = TemplateSetting::getInstance();
        $this->UserCalcProductSpecialAttribute = UserCalcProductSpecialAttribute::getInstance();
        $this->UserOption = UserOption::getInstance();
        $this->ProductionPath = new ProductionPath();
        $this->Ongoing = Ongoing::getInstance();
        $this->Setting = Setting::getInstance();
        $this->LangSetting = LangSetting::getInstance();
        $this->ExportImport = ExportImport::getInstance();
        $this->Payment = Payment::getInstance();
        $this->PaymentName = PaymentName::getInstance();
        $this->DeliveryName = DeliveryName::getInstance();

        $this->DpProductReportFile = DpProductReportFile::getInstance();
        $this->Uploader = Uploader::getInstance();
        $this->UploadFile = UploadFile::getInstance();
        $this->fileFolder = 'uploadedFiles/';
        $this->LangComponent = LangComponent::getInstance();
        $this->DpCartsData = DpCartsData::getInstance();
        $this->UserCalcProductFile = UserCalcProductFile::getInstance();
        $this->LabelImposition = LabelImposition::getInstance();
        $this->DpProductLabelImposition = DpProductLabelImposition::getInstance();
        $this->setConfigs();
    }

    /**
     * @param $domainID
     */
    public function setDomainID($domainID)
    {
        parent::setDomainID($domainID);
        $this->Mail->setDomainID($domainID);
        $this->TemplateSetting->setDomainID($domainID);
        $this->LangSetting->setDomainID($domainID);
    }

    public function setConfigs()
    {
        $this->configs = array(
            'ID' => array('type' => 'string', 'table' => 'dp_products', 'field' => 'ID', 'sign' => $this->Filter->signs['e']),
            'orderID' => array('type' => 'string', 'table' => 'dp_products', 'field' => 'orderID', 'sign' => $this->Filter->signs['e']),
            'dateFrom' => array('type' => 'timestamp', 'table' => 'dp_products', 'field' => 'created', 'sign' => $this->Filter->signs['gt']),
            'dateTo' => array('type' => 'timestamp', 'table' => 'dp_products', 'field' => 'created', 'sign' => $this->Filter->signs['lt']),
            'production' => array('type' => 'string', 'table' => 'orders', 'alias' => true, 'field' => 'production', 'sign' => $this->Filter->signs['e']),
            'isOrder' => array('type' => 'string', 'table' => 'orders', 'alias' => true, 'field' => 'isOrder', 'sign' => $this->Filter->signs['e']),
            'ready' => array('type' => 'string', 'table' => 'orders', 'alias' => true, 'field' => 'ready', 'sign' => $this->Filter->signs['e']),
            'accept' => array('type' => 'string', 'table' => 'dp_products', 'field' => 'accept', 'sign' => $this->Filter->signs['e'], 'default' => 0),
            'userID' => array('type' => 'string', 'table' => 'orders', 'alias' => true, 'field' => 'userID', 'sign' => $this->Filter->signs['li']),
            'name' => array('type' => 'string', 'table' => 'typeLanguages', 'alias' => true, 'field' => 'name', 'sign' => $this->Filter->signs['li']),
            'volumeFrom' => array('type' => 'string', 'table' => 'calculate', 'alias' => true, 'field' => 'volume', 'sign' => $this->Filter->signs['gt']),
            'volumeTo' => array('type' => 'string', 'table' => 'calculate', 'alias' => true, 'field' => 'volume', 'sign' => $this->Filter->signs['lt']),
            'realizationDateFrom' => array('type' => 'string', 'table' => 'calculate', 'alias' => true, 'field' => 'realisationDate', 'sign' => $this->Filter->signs['gt']),
            'realizationDateTo' => array('type' => 'string', 'table' => 'calculate', 'alias' => true, 'field' => 'realisationDate', 'sign' => $this->Filter->signs['lt']),
        );
    }

    /**
     * @return array
     */
    public function getConfigs()
    {
        return $this->configs;
    }

    /**
     * product list
     * @method index
     *
     * @param array
     * @return array
     */
    public function index($params)
    {
        $limit = 30;
        if (isset($params['limit'])) {
            $limit = $params['limit'];
        }
        $offset = 0;
        if (isset($params['offset'])) {
            $offset = $params['offset'];
        }

        $sortBy[0] = '-ID';
        if (isset($params['sort'])) {
            $sortBy = explode('|', $params['sort']);
        }

        $configs = $this->getConfigs();

        $filters = $this->Filter->prepare($configs, $params);

        $dpProducts = $this->DpProduct->getList($filters, $offset, $limit, $sortBy);

        if (!empty($dpProducts)) {
            $typeArr = array();
            $calcArr = array();
            $aggregateProducts = array();
            $aggregateUsers = array();
            foreach ($dpProducts as $row) {
                $calcArr[] = $row['calcID'];
                $typeArr[] = $row['typeID'];
                $aggregateProducts[] = $row['ID'];
                if ($row['userID']) {
                    $aggregateUsers[] = $row['userID'];
                }

            }
            $types = $this->PrintShopType->getByList2($typeArr);
            $calcProducts = $this->UserCalcProduct->getByCalcIds($calcArr);

            $calcProductsIds = array();
            foreach ($calcProducts as $products) {
                foreach ($products as $each) {
                    $calcProductsIds[] = $each['ID'];
                }
            }

            $ongoings = $this->Ongoing->getByItemList($calcProductsIds);
            $ongoings = $this->prepareOngoings($ongoings);

            $attributes = $this->UserCalcProductAttribute->getByCalcProductIds($calcProductsIds);
            $specialAttributes = $this->UserCalcProductSpecialAttribute->getByCalcProductIds($calcProductsIds);

            foreach ($calcProducts as $calcProductKey => $products) {
                foreach ($products as $productKey => $product) {

                    if ($product['formatUnit'] == 2) {
                        $calcProducts[$calcProductKey][$productKey]['formatWidth'] /= 10;
                        $calcProducts[$calcProductKey][$productKey]['formatHeight'] /= 10;
                    }

                    if (array_key_exists($product['ID'], $attributes)) {
                        $calcProducts[$calcProductKey][$productKey]['attributes'] = $attributes[$product['ID']];
                    }
                    if (array_key_exists($product['ID'], $specialAttributes)) {
                        $calcProducts[$calcProductKey][$productKey]['specialAttributes'] = $specialAttributes[$product['ID']];
                    }
                    if (array_key_exists($product['ID'], $ongoings)) {
                        $calcProducts[$calcProductKey][$productKey]['ongoings'] = $ongoings[$product['ID']];
                    }

                }
            }

            $aggregateUsers = array_unique($aggregateUsers);
            $defaultAddresses = $this->Address->getDefaultByList($aggregateUsers);

            foreach ($dpProducts as $key => $row) {
                $dpProducts[$key]['type'] = $types[$row['typeID']];
                $dpProducts[$key]['products'] = $calcProducts[$row['calcID']];
                $dpProducts[$key]['fileList'] = $this->UserCalcProductFile->getFlatFiles($row['calcID']);
                $labelImposition = $this->LabelImposition->getForType($row['typeID']);
                if ($labelImposition && $labelImposition['enabled']) {
                    $dpProducts[$key]['labelImpositionID'] = $labelImposition['ID'];
                    $dpProducts[$key]['labelImposition'] = [];
                    foreach ($dpProducts[$key]['fileList'] as $file) {
                        $dpProducts[$key]['labelImposition'][] = $this->DpProductLabelImposition->get('fileID', $file['ID']);
                    }
                }

                $dpProducts[$key]['filesCount'] = count($dpProducts[$key]['fileList']);
                if (isset($defaultAddresses[$row['userID']])) {
                    $dpProducts[$key]['defaultAddress'] = $defaultAddresses[$row['userID']];
                }
                $dpProducts[$key]['reportsCount'] = $this->DpProductReportFile->countFilesForProduct($row['ID']);
            }

            foreach ($dpProducts as $key => $row) {
                $orderInstance = $this->DpOrder->get('ID', $dpProducts[$key]['orderID']);
                $allFilesAccepted = true;
                if ($dpProducts[$key]['accept'] != 1)
                    $allFilesAccepted = false;

                $userOptionEntity = $this->UserOption->get('uID', $dpProducts[$key]['userID']);
                $isLimitLeft = false;
                if ($userOptionEntity['creditLimit'] != null) {
                    $aggregateCalculations = $this->DpOrder->getNotPaidCalculations($dpProducts[$key]['userID']);
                    $notPaidCalculations = $this->UserCalc->getByList($aggregateCalculations);
                    if (!$notPaidCalculations) {
                        $notPaidCalculations = array();
                    }
                    $totalUnpaidValue = $this->Price->getTotalBasePrice($notPaidCalculations);
                    $totalUnpaidDeliveryValue = $this->Price->getTotalDeliveryPrice($notPaidCalculations);
                    $unpaidPayments = ($totalUnpaidValue + $totalUnpaidDeliveryValue);
                    $creditLimit = (intval($userOptionEntity['creditLimit']) * 100);

                    $limitLeft = $creditLimit - $unpaidPayments;
                    if ($limitLeft > $dpProducts[$key]['userID']) {
                        $isLimitLeft = true;
                    }
                }

                $temporaryPaid = false;
                if ($isLimitLeft == true || $orderInstance['paid'] == 1) {
                    $temporaryPaid = true;
                }


                $displayRealisationDate = true;
                if (!$allFilesAccepted && !$temporaryPaid) {
                    $displayRealisationDate = 'no_file_and_payment';
                } else if (!$allFilesAccepted) {
                    $displayRealisationDate = 'no_file';
                } else if (!$temporaryPaid) {
                    $displayRealisationDate = 'no_payment';
                }
                $dpProducts[$key]['displayRealisationDate'] = $displayRealisationDate;
            }
        }

        return $dpProducts;
    }

    /**
     * @param $ongoings
     * @return array
     */
    private function prepareOngoings($ongoings)
    {
        $result = array();
        if (!$ongoings) {
            return $result;
        }

        foreach ($ongoings as $calcProductID => $calculationOngoings) {

            $result[$calcProductID]['count'] = 0;
            $result[$calcProductID]['finished'] = 0;
            $result[$calcProductID]['endProduction'] = false;

            foreach ($calculationOngoings as $ongoing) {
                $result[$calcProductID]['count']++;
                if ($ongoing['finished']) {
                    $result[$calcProductID]['finished']++;
                }
                if ($ongoing['inProgress']) {
                    $result[$calcProductID]['currentStage'] = $result[$calcProductID]['finished'] + 1;
                    $result[$calcProductID]['currentOperation'] = $ongoing['operationName'];
                    $result[$calcProductID]['currentDate'] = $ongoing['currentDate'];
                }
                if (count($calculationOngoings) == $ongoing['order']) {
                    $ongoing['widthPercent'] = 0;
                } else {
                    $ongoing['widthPercent'] = round(100 / (count($calculationOngoings) - 1), 0);
                }

                $result[$calcProductID]['list'][] = $ongoing;
            }

            if (!array_key_exists('currentStage', $result[$calcProductID])) {
                $lastOngoing = end($calculationOngoings);
                $result[$calcProductID]['currentStage'] = $lastOngoing['order'];
                $result[$calcProductID]['currentOperation'] = $lastOngoing['operationName'];
                $result[$calcProductID]['currentDate'] = $lastOngoing['currentDate'];
                $result[$calcProductID]['endProduction'] = true;
            }

        }

        return $result;
    }

    /**
     * @param $params
     * @return array
     */
    public function count($params)
    {
        $configs = $this->getConfigs();

        $filters = $this->Filter->prepare($configs, $params);

        $count = $this->DpProduct->count($filters);
        return array('count' => $count);
    }

    /**
     * @param $id
     * @return bool
     */
    public function baseInfo($id)
    {
        if (!$id) {
            return false;
        }
        $result = $this->DpProduct->getBaseInfo($id);
        return $result;
    }

    public function baseCalcInfo($id)
    {

        $calcProduct = $this->UserCalcProduct->getByProductCalcIds(array($id));

        $attributes = $this->UserCalcProductAttribute->getByCalcProductIds(array($id));
        $specialAttributes = $this->UserCalcProductSpecialAttribute->getByCalcProductIds(array($id));

        $calcProduct[$id][0]['attributes'] = $attributes[$id];
        $calcProduct[$id][0]['specialAttributes'] = $specialAttributes[$id];

        return $calcProduct[$id][0];
    }

    /**
     * @param $ID
     * @return array
     */
    private function _delete($ID)
    {
        $one = $this->DpProduct->get('ID', $ID);

        $data['response'] = false;
        if (!$one) {
            return $this->sendFailResponse('06');
        }

        if ($this->DpProduct->delete('ID', $one['ID'])) {

            $data['response'] = true;

            $allProductAddress = $this->DpOrderAddressProduct->getAllByProduct($ID);

            $orderAddressArr = array();
            if ($allProductAddress) {
                foreach ($allProductAddress as $productAddress) {
                    $orderAddressArr[] = $productAddress['orderAddressID'];
                }
            }

            $orderAddresses = $this->DpOrderAddress->getByList($orderAddressArr);

            $removedAddresses = 0;
            $removedOrderAddresses = 0;
            if ($orderAddresses) {
                foreach ($orderAddresses as $orderAddress) {
                    $removedOrderAddresses += intval($this->DpOrderAddress->delete('ID', $orderAddress['ID']));
                    $removedAddresses += intval($this->Address->delete('ID', $orderAddress['addressID']));
                }
            }
            $data['removedOrderAddresses'] = $removedOrderAddresses;
            $data['removedAddresses'] = $removedAddresses;
        }

        return $data;
    }

    /**
     * @param $ID
     * @return mixed
     */
    public function delete_index($ID)
    {
        return $this->_delete($ID);
    }

    /**
     * @param $ID
     * @return array
     * @throws Exception
     */
    public function delete_deletePublic($ID)
    {

        $data['response'] = $this->DpOrderAddressProduct->deleteByProduct($ID);
        $data['response'] = $data['response'] && $this->DpCartsData->delete('productID', $ID);
        $files = $this->UserCalcProductFile->getByProduct($ID);
        foreach ($files as $file) {
            $data['response'] = $data['response'] && $this->Uploader->removeFromCompany(Uploader::getUploadPath($ID, $file['ID']), $file['name']);
            $data['response'] = $data['response'] && $this->UserCalcProductFile->delete('ID', $file['ID']);
        }
        $data['response'] = $data['response'] && $this->DpProduct->delete('ID', $ID);

        return $data;
    }

    /**
     * @param $productID
     * @return array
     * @throws LoaderError
     * @throws RuntimeError
     * @throws SyntaxError
     */
    public function patch_index($productID)
    {
        $accept = $this->Data->getPost('accept');
        if ($accept === NULL) {
            return array('response' => false);
        }
        $rejectInfo = $this->Data->getPost('rejectInfo');
        $acceptFilesIds = $this->Data->getPost('acceptFiles') ?? [];

        if ($accept == 1) {
            $this->UserCalc->updateRealizationTime($productID, $this->DpOrder, $this->DpProduct);
        }

        return $this->changeStatusAndSendMail($productID, $accept, $acceptFilesIds, $rejectInfo);

    }

    /**
     * @param $orderID
     * @return array|bool
     */
    public function getByOrder($orderID)
    {
        $products = $this->DpProduct->getInfoProducts($orderID);

        if (!$products) {
            return array();
        }

        $aggregateTypes = array();
        $aggregateCopyBasePrices = array();
        foreach ($products as $product) {
            $aggregateTypes[] = $product['typeID'];
            $aggregateCopyBasePrices[] = $product['copyPriceID'];
        }

        $copyPrices = $this->BasePrice->getByList($aggregateCopyBasePrices);

        $types = $this->PrintShopType->getByList2($aggregateTypes);
        foreach ($products as $key => $product) {
            $products[$key]['type'] = $types[$product['typeID']];
            $products[$key]['price'] = $this->Price->getPriceToView($product['price']);
            $products[$key]['grossPrice'] = $this->Price->getPriceToView($product['grossPrice']);
            if (isset($copyPrices[$product['copyPriceID']]) && $copyPrices[$product['copyPriceID']] > 0) {
                $copyPrices[$product['copyPriceID']]['price'] = $this->Price->getPriceToView(
                    $copyPrices[$product['copyPriceID']]['price']
                );
                $copyPrices[$product['copyPriceID']]['grossPrice'] = $this->Price->getPriceToView(
                    $copyPrices[$product['copyPriceID']]['grossPrice']
                );
                $products[$key]['copyPrice'] = $copyPrices[$product['copyPriceID']];
            }
        }

        return $products;
    }

    /**
     * @param $productID
     * @return mixed
     */
    public function patch_restoreAccept($productID)
    {
        $post = $this->Data->getAllPost();

        $accept = $post['accept'];
        $data['response'] = false;

        $loggedUser = $this->Auth->getLoggedUser();

        $product = $this->DpProduct->get('ID', $productID);
        $order = $this->DpOrder->get('ID', $product['orderID']);

        if ($order['userID'] != $loggedUser['ID']) {
            return $this->sendFailResponse('12');
        }

        $files = $this->DpProductFile->getByProduct($productID);

        foreach ($files as $file) {

            if ($file['accept'] != -1) {
                continue;
            }

            if ($this->DpProductFile->delete('ID', $file['ID'])) {
                $date = date('Y-m-d', strtotime($file['created']));
                $explodeName = explode('.', $file['name']);
                $ext = end($explodeName);
                if ($ext == 'pdf') {
                    array_pop($explodeName);
                    $minImageName = implode('.', $explodeName) . '.jpg';
                } else {
                    $minImageName = $file['name'];
                }
                $fileName = MAIN_UPLOAD . companyID . '/' . 'productFiles/' . $date . '/' . $file['folder'] . '/' . $file['productID'] . '/' . $file['ID'] . '/' . $file['name'];
                $minFileName = MAIN_UPLOAD . companyID . '/' . 'productFiles/' . $date . '/' . $file['folder'] . '/' . $file['productID'] . '/' . $file['ID'] . '/' . THUMB_IMAGE_PREFIX . $minImageName;
                $data['removedFiles'][] = $fileName;
                if (is_file($fileName)) {
                    unset($fileName);
                }
                if (is_file($minFileName)) {
                    unset($fileName);
                }

            }
        }

        if ($this->DpProduct->update($productID, 'accept', $accept)) {
            $data['response'] = true;
        }

        return $data;

    }

    public function patch_copy()
    {

    }

    public function post_exportOrders()
    {
        $post = $this->Data->getAllPost();

        $exportArray = array();

        if ($post['dateStart'] && $post['dateStart'] != "" && $post['dateEnd'] && $post['dateEnd'] != "") {
            $dateStart = $post['dateStart'];
            $dateEnd = $post['dateEnd'];
            $dateStart = date("Y-m-d 00:00:00", ($dateStart + 3600));
            $dateEnd = date("Y-m-d 23:59:59", ($dateEnd + 3600));
            $this->debug('sateStart', $dateStart);
            $this->debug('dateEnd', $dateEnd);
            $list = $this->DpProduct->getForExport($dateStart, $dateEnd);
            // array_push($exportArray, array('Raport z dni', $dateStart, $dateEnd));
        } else {
            $list = $this->DpProduct->getForExport();
        }

        $this->Setting->setModule('general');
        $this->Setting->setLang(NULL);
        $defaultLangID = $this->Setting->getValue('defaultLang');
        $defaultLangEntity = $this->LangSetting->getByID($defaultLangID);
        $lang = $defaultLangEntity['code'];

        //header info
        $headers = array();
        $headers['orderID'] = "Nr zamówienia";
        $headers['productID'] = "Nr produktu";
        $headers['clientName'] = "Klient";
        $headers['clientAddress'] = "Adres";
        $headers['countryCode'] = "Kraj";
        $headers['productName'] = "Nazwa produktu";
        $headers['productFormat'] = "Format produktu";
        $headers['productPaperCalcFormat'] = "Format papieru";
        $headers['attributes'] = "Cechy";
        $headers['volume'] = "Nakład";
        $headers['cube'] = "Objętość";
        $headers['weight'] = "Waga zamówienia";
        $headers['seller'] = "Sprzedawca";
        $headers['delivery'] = "Sposób dostawy";
        $headers['realisationMethod'] = "Termin realizacji";
        $headers['paymentMethod'] = "Metoda płatności";
        $headers['created'] = "Data zamówienia";
        $headers['realisation'] = "Data realizacji";
        array_push($exportArray, $headers);

        foreach ($list as $order) {
            $dataExport = array();

            $dataExport['orderID'] = $order['orderID'];

            $dataExport['productID'] = $order['ID'];

            $clientInfo = $this->Address->getByUser($order['userID']);
            $dataExport['clientName'] = $clientInfo[0]['companyName'] . ' ' . $clientInfo[0]['name'] . ' ' . $clientInfo[0]['lastname'];
            $dataExport['clientAddress'] = $clientInfo[0]['addressName'];
            $dataExport['countryCode'] = $clientInfo[0]['countryCode'];

            $dataExport['productName'] = $order['productName'];
            $dataExport['productFormat'] = $order['formatName'];
            $dataExport['productPaperCalcFormat'] = $order['paperWidth'] . "x" . $order['paperHeight'];

            $attributes = $this->UserCalcProductAttribute->getByCalcProductIds(array($order['calcID']));
            $attributesList = "";
            foreach ($attributes[strval($order['calcID'])] as $attr) {
                $attributesList .= $attr['langs'][strval($lang)]['name'] . ": " . $attr['optLangs'][strval($lang)]['name'] . " ";
            }

            $dataExport['attributes'] = $attributesList;

            $dataExport['volume'] = $order['volume'];
            $dataExport['pages'] = $order['pages'];
            $dataExport['weight'] = $order['weight'];

            $sellerInfo = $this->User->get('ID', $order['sellerID']);
            $dataExport['seller'] = $sellerInfo['name'];

            $addressesResult = $this->DpOrderAddress->getByOrder($order['orderID']);
            $addressInstance = $addressesResult[0];
            $deliveryNames = $this->DeliveryName->getNames(array($addressInstance['deliveryID']));
            $dataExport['delivery'] = $deliveryNames[strval($addressInstance['deliveryID'])][strval($lang)];


            $dataExport['realisationMethod'] = $order['realizationName'];

            $payment = $this->PaymentName->getByPaymentIDAndLang($order['paymentID'], strval($lang));
            $dataExport['paymentMethod'] = $payment[0]['name'];

            $dataExport['created'] = $order['created'];
            $dataExport['realisation'] = $order['realisationDate'];

            array_push($exportArray, $dataExport);
        }

        $dir = companyID . '/download/';
        if (!is_dir(STATIC_PATH . $dir)) {
            mkdir(STATIC_PATH . $dir, 0777, true);
        }
        $path = $dir . 'orders__' . date('Y-m-d_G-i-s') . '.xls';
        $this->ExportImport->newSheet('Orders');
        $this->ExportImport->setFromArray($exportArray);
        $this->ExportImport->path = STATIC_PATH . $path;
        $this->ExportImport->saveFile();

        return array('response' => true, 'url' => STATIC_URL . $path);
    }

    public function reportFiles($productID)
    {
        $list = $this->DpProductReportFile->getFilesForProduct($productID);
        foreach ($list as &$item) {
            $item['url'] = STATIC_URL . $this->fileFolder . companyID . '/' . $item['path'];
        }
        return $list;
    }

    public function post_reportFiles($productID)
    {
        $maxID = $this->UploadFile->getMaxID();
        $dirNumber = floor($maxID / 100);
        $filename = $_FILES['file']['name'];
        $destinationFolder = 'uploadedFiles/' . companyID . '/' . $dirNumber . '/';
        $filename = $this->Uploader->upload($_FILES, 'file', $destinationFolder, $filename, true);
        $response = ['response' => false];
        if (!$filename) {
            return $response;
        }
        $id = $this->UploadFile->setUpload($filename, 'productReport', $dirNumber . '/' . $filename);
        try {
            $minImage = $this->Uploader->resizeImage(MAIN_UPLOAD . $destinationFolder . $filename, 200, 200, false);
            $minImage->writeImage(MAIN_UPLOAD . $destinationFolder . Uploader::getMiniatureName($filename));
        } catch (ImagickException $e) {
            $response['info'] = $e->getMessage();
        }
        if (!$this->DpProductReportFile->create(['productID' => $productID, 'fileID' => $id], false)) {
            return $response;
        }

        $response['response'] = true;

        $uploadedFile = $this->UploadFile->getFileByID($id);

        $selectedProduct = $this->DpProduct->get('ID', intval($productID));
        $order = $this->DpOrder->getOne($selectedProduct['orderID']);
        $selectedProduct['orderNumber'] = $order['orderNumber'];
        $user = $this->User->get('ID', $order['userID']);

        $this->Setting->setModule('general');
        $this->Setting->setLang(NULL);
        $this->Setting->setDomainID($this->getDomainID());
        $defaultLangID = $this->Setting->getValue('defaultLang');
        $defaultLangEntity = $this->LangSetting->getByID($defaultLangID);
        $lang = $defaultLangEntity['code'];

        $userOption = $this->UserOption->get('uID', $user['ID']);
        if ($userOption && $userOption['lang']) {
            $lang = $userOption['lang'];
        }

        $calc = $this->UserCalc->getOne($selectedProduct['calcID']);
        $type = $this->PrintShopType->getByList2(array($calc['typeID']));
        if ($type) {
            $type = current($type);
        }
        $selectedProduct['name'] = $type['names'][$lang];
        $selectedProduct['volume'] = $calc['volume'];

        $reportFiles = [$uploadedFile];
        foreach ($reportFiles as &$report) {
            $explodedPath = explode('/', $report['path']);
            $report['url'] = STATIC_URL . DpProductReportFile::UPLOAD_PATH . '/' . $report['path'];
            $report['minUrl'] = STATIC_URL . DpProductReportFile::UPLOAD_PATH . '/' . $explodedPath[0] . '/' . Uploader::getMiniatureName($report['name']);
        }
        $mailContent = $this->renderNewReport($selectedProduct, $lang, $reportFiles);

        if (filter_var($user['user'], FILTER_VALIDATE_EMAIL) !== false) {
            $this->Mail->setBind('firstName', $user['name']);
            $this->Mail->setBind('files_info', $mailContent);

            $send = $this->Mail->sendMail($user['user'], $user['name'], 'newReportToClient', $lang);
            if (!$send) {
                $this->debug('error with mail');
                $response['response'] = false;
            }
        } else {
            $this->debug('Problem with email: ' . $user['user']);
            $response['response'] = false;
        }
        $response['item'] = $uploadedFile;
        return $response;
    }

    public function delete_reportFiles($productID, $uploadFileID)
    {
        $fileEntity = $this->UploadFile->getFileByID($uploadFileID);

        if (!$fileEntity) {
            return $this->sendFailResponse('06');
        }

        $filePath = MAIN_UPLOAD . $this->fileFolder . companyID . '/' . $fileEntity['path'];
        if ($this->DpProductReportFile->deleteByUploadID($fileEntity['ID'])) {
            if ($this->UploadFile->delete('ID', $fileEntity['ID'])) {
                if (unlink($filePath)) {
                    return ['response' => true];
                }
            }
        }
        return ['response' => false];
    }

    /**
     * @param $selectedProduct
     * @param $names
     * @param $volume
     * @param $lang
     * @param $files
     * @param $colorRow
     */
    private function renderAcceptFiles($selectedProduct, $names, $volume, $lang, $files = [], $colorRow = false): string
    {
        $templateID = 106;
        $templateName = 'product-files-list';

        $templateSetting = $this->TemplateSetting->getOne($templateID, 1);

        $templatePath = 'default/' . $templateID . '/' . $templateName . '.html';

        if ($templateSetting && $templateSetting['source'] == 1) {
            $templatePath = companyID . '/' . $templateID . '/' . $templateName . '.html';
        } elseif ($templateSetting && $templateSetting['source'] == 2) {
            $templatePath = companyID . '/' . $templateID . '/' . $this->getDomainID() . '/' . $templateName . '.html';
        }

        $loader = new FilesystemLoader(STATIC_PATH . 'templates');
        $twig = new Twig_Environment($loader, array());
        $twig->addExtension(new TranslateExtension());
        $template = $twig->load($templatePath);

        $product = array();
        $product['ID'] = $selectedProduct['ID'];
        $product['orderID'] = $selectedProduct['orderID'];
        $product['orderNumber'] = $selectedProduct['orderNumber'];
        $product['names'] = $names;
        $product['volume'] = $volume;

        return $template->render(
            array(
                'product' => $product,
                'files' => $files,
                'lang' => $lang,
                'colorRow' => $colorRow
            )
        );
    }

    private function renderNewReport($selectedProduct, $lang, $files): string
    {
        $templateID = 123;
        $templateName = 'product-report';

        $templateSetting = $this->TemplateSetting->getOne($templateID, 1);

        $templatePath = 'default/' . $templateID . '/' . $templateName . '.html';

        if ($templateSetting && $templateSetting['source'] == 1) {
            $templatePath = companyID . '/' . $templateID . '/' . $templateName . '.html';
        } elseif ($templateSetting && $templateSetting['source'] == 2) {
            $templatePath = companyID . '/' . $templateID . '/' . $this->getDomainID() . '/' . $templateName . '.html';
        }

        $loader = new FilesystemLoader(STATIC_PATH . 'templates');
        $twig = new Twig_Environment($loader, array());
        $twig->addExtension(new TranslateExtension());
        $template = $twig->load($templatePath);

        $product = array();
        $product['ID'] = $selectedProduct['ID'];
        $product['orderID'] = $selectedProduct['orderID'];

        return $template->render(
            array(
                'product' => $product,
                'files' => $files,
                'lang' => $lang
            )
        );
    }

    /**
     * @param $productID int
     * @param $accept int 1|-1
     * @param $processedFiles array
     * @param $rejectInfo string
     * @return array
     */
    public function changeStatusAndSendMail($productID, $accept, $processedFiles = [], $rejectInfo = ''): array
    {
        $response = true;
        $selectedProduct = $this->DpProduct->get('ID', intval($productID));
        $order = $this->DpOrder->getOne($selectedProduct['orderID']);
        $selectedProduct['orderNumber'] = $order['orderNumber'];
        $user = $this->User->get('ID', $order['userID']);
        $calc = $this->UserCalc->getOne($selectedProduct['calcID']);
        $this->Setting->setModule('general');
        $this->Setting->setLang(NULL);
        $this->Setting->setDomainID($this->getDomainID());
        $defaultLangID = $this->Setting->getValue('defaultLang');
        $defaultLangEntity = $this->LangSetting->getByID($defaultLangID);
        $lang = $defaultLangEntity['code'];

        $userOption = $this->UserOption->get('uID', $user['ID']);
        if ($userOption && $userOption['lang']) {
            $lang = $userOption['lang'];
        }
        $type = $this->PrintShopType->getByList2(array($calc['typeID']));
        if ($type) {
            $type = current($type);
        }

        $this->DpProduct->update($selectedProduct['ID'], 'accept', $accept);
        $this->DpProduct->update($selectedProduct['ID'], 'acceptCanceled', 1);
        $userCalcProduct = $this->DpProduct->getUserCalcProduct($productID);
        $files = $this->UserCalcProductFile->getFlatFiles($userCalcProduct['calcID']);

        if ($files) {

            $allowedThumbExtension = explode(',', THUMB_IMAGE_ALLOWED_EXTENSION);

            foreach ($files as $key => $file) {
                $actualDate = date('Y-m-d', strtotime($file['created']));

                $explodeName = explode('.', $file['name']);
                $ext = end($explodeName);

                $minImageName = false;

                if ($ext == THUMB_PDF_ALLOWED_EXTENSION) {
                    array_pop($explodeName);
                    $minImageName = implode('.', $explodeName) . '.jpg';
                } else if (in_array($ext, $allowedThumbExtension)) {
                    $minImageName = $file['name'];
                }

                $files[$key]['url'] = STATIC_URL . companyID . '/' . Uploader::getUploadPath($userCalcProduct['ID'], $file['ID']) . $file['name'];
                if ($minImageName) {
                    $files[$key]['minUrl'] = STATIC_URL . companyID . '/' . Uploader::getUploadPath($userCalcProduct['ID'], $file['ID']) . THUMB_IMAGE_PREFIX . $minImageName;
                } else {
                    $files[$key]['minUrl'] = STATIC_URL . companyID . '/' . 'images' . '/' . THUMB_IMAGE_DEFAULT;
                }

            }
        }

        $reportFiles = $this->DpProductReportFile->getFilesForProduct($selectedProduct['ID']);
        foreach ($reportFiles as &$report) {
            $explodedPath = explode('/', $report['path']);
            $report['url'] = STATIC_URL . DpProductReportFile::UPLOAD_PATH . '/' . $report['path'];
            $report['minUrl'] = STATIC_URL . DpProductReportFile::UPLOAD_PATH . '/' . $explodedPath[0] . '/' . Uploader::getMiniatureName($report['name']);
            $report['name'] .= ' /' . $this->LangComponent->translate('report')[$lang] . '/';
        }
        $updated = 0;
        $info = '';

        if ($accept == 1) {

            $this->DpProduct->update($selectedProduct['ID'], 'acceptDate', date('Y-m-d H:i:s'));
            $this->DpProduct->update($selectedProduct['ID'], 'acceptCanceled', 0);
            $params['itemID'] = $selectedProduct['orderID'];
            $params['appVersion'] = 1;
            $this->ProductionPath->doPath($params);

            if (!empty($files)) {
                foreach ($files as $key => $file) {
                    if (!$files[$key]['accept']) {
                        $this->UserCalcProductFile->setAccepted($file['ID'],
                            $this->Auth->getLoggedUser()['ID'],
                            $this->Auth->getLoggedUser()['firstname'] . ' ' . $this->Auth->getLoggedUser()['lastname']);
                        $files[$key]['accept'] = 1;
                    }

                }
            }

            if (empty($files) || count($reportFiles)) {
                $productsContent = $this->renderAcceptFiles($selectedProduct, $type['names'], $calc['volume'], $lang, array_merge($files, $reportFiles), false);

                $info = 'files_accepted';

                if (filter_var($user['user'], FILTER_VALIDATE_EMAIL) !== false) {
                    $this->Mail->setBind('firstName', $user['name']);
                    $this->Mail->setBind('files_info', $productsContent);

                    $send = $this->Mail->sendMail($user['user'], $user['name'], 'acceptFilesOk', $lang);
                    if (!$send) {
                        $this->debug('error with mail');
                    }
                } else {
                    $this->debug('Problem with email: ' . $user['user']);
                }

            }

            if (empty($files)) {
                return array(
                    'response' => true,
                    'info' => 'there_are_no_files_to_accept'
                );
            }

        } elseif ($accept == -1) {
            if (!$this->DpProductReportFile->deleteAllForProduct($selectedProduct['ID'])) {
                $response = false;
                $info = 'no all reports deleted';
            }
            if (!empty($files)) {
                foreach ($files as $key => $file) {
                    if (in_array($file['ID'], $processedFiles)) {
                        if ($this->UserCalcProductFile->update($file['ID'], 'accept', 1)) {
                            $files[$key]['accept'] = 1;
                        }
                    } else {
                        if ($this->UserCalcProductFile->update($file['ID'], 'accept', -1)) {
                            $updated++;
                            $files[$key]['accept'] = -1;
                        }
                    }
                }

                if ($updated > 0) {
                    $productsContent = $this->renderAcceptFiles($selectedProduct, $type['names'], $calc['volume'], $lang, array_merge($files, $reportFiles), true);

                    $this->DpProduct->update($productID, 'rejectInfo', $rejectInfo);

                    $info = 'files_rejected';

                    if (filter_var($user['user'], FILTER_VALIDATE_EMAIL) !== false) {
                        $this->Mail->setBind('firstName', $user['name']);
                        $this->Mail->setBind('files_info', $productsContent);
                        $this->Mail->setBind('rejectInfo', $rejectInfo);

                        $send = false;

                        try {
                            $send = $this->Mail->sendMail($user['user'], $user['name'], 'rejectFiles', $lang);
                        } catch (Exception $e) {
                            $this->debug('error with mail: ', $e->getMessage());
                        }

                        if (!$send) {
                            $this->debug('error with mail', $send);
                        }
                    } else {
                        $this->debug('Problem with email: ' . $user['user']);
                    }
                }
            }
        } elseif ($accept == 0) {
            $info = 'product_rejected';

            if (!$this->DpProductReportFile->deleteAllForProduct($selectedProduct['ID'])) {
                $response = false;
                $info = 'no all reports deleted';
            }

            $productsContent = $this->renderAcceptFiles($selectedProduct, $type['names'], $calc['volume'], $lang);

            if (filter_var($user['user'], FILTER_VALIDATE_EMAIL) !== false) {
                $this->Mail->setBind('first_name', $user['name']);
                $this->Mail->setBind('product_info', $productsContent);

                $send = false;

                try {
                    $send = $this->Mail->sendMail($user['user'], $user['name'], 'productRejected', $lang);
                } catch (Exception $e) {
                    $this->debug('error with mail: ', $e->getMessage());
                }

                if (!$send) {
                    $this->debug('error with mail', $send);
                }
            } else {
                $this->debug('Problem with email: ' . $user['user']);
            }
        }
        return array(
            'response' => $response,
            'info' => $info
        );
    }

    public function sendReportAcceptedMail($productID, $fileID)
    {
        $selectedProduct = $this->DpProduct->get('ID', intval($productID));
        $order = $this->DpOrder->getOne($selectedProduct['orderID']);
        $selectedProduct['orderNumber'] = $order['orderNumber'];
        $user = $this->User->get('ID', $order['userID']);
        $calc = $this->UserCalc->getOne($selectedProduct['calcID']);
        $type = $this->PrintShopType->getByList2(array($calc['typeID']));
        if ($type) {
            $type = current($type);
        }
        $this->Setting->setModule('general');
        $this->Setting->setLang(NULL);
        $this->Setting->setDomainID($this->getDomainID());
        $defaultLangID = $this->Setting->getValue('defaultLang');
        $defaultLangEntity = $this->LangSetting->getByID($defaultLangID);
        $lang = $defaultLangEntity['code'];
        $templateID = 123;
        $templateName = 'product-report';

        $templateSetting = $this->TemplateSetting->getOne($templateID, 1);

        $templatePath = 'default/' . $templateID . '/' . $templateName . '.html';

        if ($templateSetting && $templateSetting['source'] == 1) {
            $templatePath = companyID . '/' . $templateID . '/' . $templateName . '.html';
        } elseif ($templateSetting && $templateSetting['source'] == 2) {
            $templatePath = companyID . '/' . $templateID . '/' . $this->getDomainID() . '/' . $templateName . '.html';
        }

        $loader = new FilesystemLoader(STATIC_PATH . 'templates');
        $twig = new Twig_Environment($loader, array());
        $twig->addExtension(new TranslateExtension());
        $template = $twig->load($templatePath);

        $product = array();
        $product['ID'] = $selectedProduct['ID'];
        $product['orderID'] = $selectedProduct['orderID'];
        $product['orderNumber'] = $selectedProduct['orderNumber'];
        $product['name'] = $type['names'][$lang];
        $product['volume'] = $calc['volume'];

        $file = $this->DpProductReportFile->getFile($fileID);
        $explodedPath = explode('/', $file['path']);
        $file['url'] = STATIC_URL . DpProductReportFile::UPLOAD_PATH . '/' . $file['path'];
        $file['minUrl'] = STATIC_URL . DpProductReportFile::UPLOAD_PATH . '/' . $explodedPath[0] . '/' . Uploader::getMiniatureName($file['name']);
        $file['name'] .= ' /' . $this->LangComponent->translate('report')[$lang] . '/';

        $files = [$file];
        $productsContent = $template->render(
            array(
                'product' => $product,
                'files' => $files,
                'lang' => $lang
            )
        );

        $this->Mail->setBind('userName', $user['name'] . ' ' . $user['lastname']);
        $this->Mail->setBind('files_info', $productsContent);
        $this->Setting->setModule('additionalSettings');
        $adminMailRecipients = $this->Setting->getValue('adminMailRecipients');
        $adminMailRecipients = explode(',', $adminMailRecipients);
        foreach ($adminMailRecipients as $adminMailRecipient) {
            if (filter_var($adminMailRecipient, FILTER_VALIDATE_EMAIL) !== false) {
                $send = $this->Mail->sendMail($adminMailRecipient, 'admin', 'reportAcceptedToPrinthouse');
                if (!$send) {
                    $this->debug('error with mail');
                }
            }
        }

    }
}
