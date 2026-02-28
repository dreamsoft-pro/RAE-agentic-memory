<?php
namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Controllers\Components\Standard;

use DreamSoft\Controllers\Components\Filter;
use DreamSoft\Models\Address\Address;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Models\Order\DpProductFile;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopUser\UserCalcProductAttribute;
use DreamSoft\Models\PrintShopUser\UserCalcProductSpecialAttribute;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Controllers\Components\ProductionPath;
use DreamSoft\Models\ProductionPath\Ongoing;
use DreamSoft\Models\ProductionPath\OngoingLog;

class ScheduleController extends Controller
{
    /**
     * @var Filter
     */
    protected $Filter;
     /**
     * @var Address
     */
    protected $Address;
    /**
     * @var DpProduct
     */
    protected $DpProduct;
    /**
     * @var DpProductFile
     */
    protected $DpProductFile;
    /**
     * @var PrintShopType
     */
    protected $PrintShopType;
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
     * @var UserCalcProductSpecialAttribute
     */
    protected $UserCalcProductSpecialAttribute;
    /**
     * @var ProductionPath
     */
    private $ProductionPath;
    /**
     * @var Ongoing
     */
    private $Ongoing;
    /**
     * @var OngoingLog
     */
    private $OngoingLog;
    /**
     * @var Standard
     */
    private $Standard;
    /**
     * @var array
     */
    private $configs;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Standard = Standard::getInstance();

        $this->Filter = Filter::getInstance();
        $this->Address = Address::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->DpProductFile = DpProductFile::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->UserCalcProductAttribute = UserCalcProductAttribute::getInstance();
        $this->UserCalcProductSpecialAttribute = UserCalcProductSpecialAttribute::getInstance();
        $this->ProductionPath = new ProductionPath();
        $this->Ongoing = Ongoing::getInstance();
        $this->OngoingLog = OngoingLog::getInstance();

        $this->setConfigs();
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

        $sortBy = array('-priority', '-productionOrder', '-ID');

        $configs = $this->getConfigs();

        $filters = $this->Filter->prepare($configs, $params);

        $list = $this->DpProduct->getList($filters, $offset, $limit, $sortBy);

        if (!empty($list)) {
            $typeArr = array();
            $calcArr = array();
            $aggregateProducts = array();
            $aggregateUsers = array();
            foreach ($list as $row) {
                $calcArr[] = $row['calcID'];
                $typeArr[] = $row['typeID'];
                $aggregateProducts[] = $row['ID'];
                if( $row['userID'] ) {
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

            $files = $this->DpProductFile->getByList($aggregateProducts);

            $attributes = $this->UserCalcProductAttribute->getByCalcProductIds($calcProductsIds);
            $specialAttributes = $this->UserCalcProductSpecialAttribute->getByCalcProductIds($calcProductsIds);

            foreach ($calcProducts as $calcProductKey => $products) {
                foreach ($products as $productKey => $product) {

                    if( $product['formatUnit'] == 2 ) {
                        $calcProducts[$calcProductKey][$productKey]['formatWidth'] /= 10;
                        $calcProducts[$calcProductKey][$productKey]['formatHeight'] /= 10;
                    }

                    if( array_key_exists($product['ID'], $attributes) ) {
                        $calcProducts[$calcProductKey][$productKey]['attributes'] = $attributes[$product['ID']];
                    }
                    if(array_key_exists($product['ID'], $specialAttributes)) {
                        $calcProducts[$calcProductKey][$productKey]['specialAttributes'] = $specialAttributes[$product['ID']];
                    }
                    if(array_key_exists($product['ID'], $ongoings)) {
                        $calcProducts[$calcProductKey][$productKey]['ongoings'] = $ongoings[$product['ID']];
                    }

                }
            }

            $aggregateUsers = array_unique($aggregateUsers);
            $defaultAddresses = $this->Address->getDefaultByList($aggregateUsers);

            foreach ($list as $key => $row) {
                $list[$key]['type'] = $types[$row['typeID']];
                $list[$key]['products'] = $calcProducts[$row['calcID']];
                $list[$key]['fileList'] = $files[$row['ID']];
                if (isset($files[$row['ID']])) {
                    $list[$key]['filesCount'] = count($files[$row['ID']]);
                } else {
                    $list[$key]['filesCount'] = 0;
                }
                if( isset($defaultAddresses[$row['userID']]) ) {
                    $list[$key]['defaultAddress'] = $defaultAddresses[$row['userID']];
                }
            }
        }

        return $list;
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
     * @param $ongoings
     * @return array
     */
    private function prepareOngoings($ongoings)
    {
        $result = array();
        if( !$ongoings ) {
            return $result;
        }

        foreach ($ongoings as $calcProductID => $calculationOngoings) {

            $result[$calcProductID]['count'] = 0;
            $result[$calcProductID]['finished'] = 0;
            $result[$calcProductID]['plannedTime'] = 0;
            $result[$calcProductID]['endProduction'] = false;

            usort($calculationOngoings, function($a, $b) { return $a['ID'] - $b['ID']; });

            foreach ($calculationOngoings as $ongoing) {
                $result[$calcProductID]['count']++;
                $result[$calcProductID]['plannedTime'] += $ongoing['estimatedTime'];
                if($ongoing['finished']) {
                    $result[$calcProductID]['finished']++;
                }
                if($ongoing['inProgress']) {
                    $result[$calcProductID]['currentStage'] = $result[$calcProductID]['finished'] + 1;
                    $result[$calcProductID]['currentOperation'] = $ongoing['operationName'];
                    $result[$calcProductID]['currentDate'] = $ongoing['currentDate'];
                }
                if( count($calculationOngoings) == $ongoing['order'] ) {
                    $ongoing['widthPercent'] = 0;
                } else {
                    $ongoing['widthPercent'] = round(100/(count($calculationOngoings)-1), 0);
                }

                $ongoing['plannedEnd'] = null;
                if($ongoing['plannedStart'] != null){
                    $ongoing['plannedEnd'] = date("Y-m-d H:i:s",  strtotime($ongoing['plannedStart'])+$ongoing['estimatedTime']);
                }

                $logs = $this->OngoingLog->get('ongoingID', $ongoing['ID'], true);
                $ongoing['logs'] = $logs;

                $ongoing['startLog'] = $this->OngoingLog->getStartLog($ongoing['ID']);
                $ongoing['endLog'] = $this->OngoingLog->getLastLog($ongoing['ID']);

                $result[$calcProductID]['list'][] = $ongoing;
            }

            $startLog = $this->OngoingLog->getStartLog($calculationOngoings[0]['ID']);
            $endLog = $this->OngoingLog->getLastLog($calculationOngoings[sizeof($calculationOngoings)-1]['ID']);
            $minusIndex = 2;
            while(!$endLog && $minusIndex <= sizeof($calculationOngoings)){
                $endLog = $this->OngoingLog->getLastLog($calculationOngoings[sizeof($calculationOngoings)-$minusIndex]['ID']);
                $minusIndex++;
            }
            
            $result[$calcProductID]['startDate'] = null;
            $result[$calcProductID]['endDate'] = null;
            if($startLog){
                $result[$calcProductID]['startDate'] = $startLog['date'];
            }
            if($endLog){
                $result[$calcProductID]['endDate'] = $endLog['date'];
            }

            $result[$calcProductID]['plannedStart'] = $calculationOngoings[0]['plannedStart'];
            if($result[$calcProductID]['plannedStart'] != null){
                $result[$calcProductID]['plannedEnd'] = date("Y-m-d H:i:s",  strtotime($result[$calcProductID]['plannedStart'])+$result[$calcProductID]['plannedTime']);
            }
            

            if( !array_key_exists('currentStage', $result[$calcProductID]) ) {
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
     * @return array
     */
    public function patch_sort()
    {
        $post = $this->Data->getAllPost();
        $post = array_reverse($post);
        if ($this->DpProduct->sortProduction($post)) {
            return array('response' => true);
        } else {
            return $this->sendFailResponse('03');
        }
    }

    public function post_updateOngoings()
    {
        $data = $this->Data->getAllPost();

        foreach($data as $ongoing){
            $this->Ongoing->update($ongoing['ongoingID'], 'plannedStart', $ongoing['plannedStart']);
            $this->Ongoing->update($ongoing['ongoingID'], 'estimatedTime', $ongoing['estimatedTime']);
        }

        return array('response' => true);
    }
}