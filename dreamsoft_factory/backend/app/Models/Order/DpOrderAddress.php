<?php

namespace DreamSoft\Models\Order;

/**
 * Description of DpOrderAddress
 *
 * @author Rafał
 */

use DreamSoft\Controllers\Components\Price;
use DreamSoft\Core\Model;
use DreamSoft\Libs\DataUtils;
use DreamSoft\Models\PrintShopUser\UserDeliveryPrice;
use PDO;

class DpOrderAddress extends Model
{

    protected $addressProductsTable;
    protected $addressSource;
    protected $deliveryPrices;
    protected $basePrices;
    /**
     * @var UserDeliveryPrice
     */
    protected $UserDeliveryPrice;
    /**
     * @var Price
     */
    protected $Price;
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('orderAddress', true);
        $this->addressProductsTable = 'dp_orderAddressProducts';
        $this->addressSource = 'address';
        $this->deliveryPrices = 'ps_user_deliveryPrices';
        $this->basePrices = 'dp_base_prices';
        $this->Price = Price::getInstance();
        $this->UserDeliveryPrice = UserDeliveryPrice::getInstance();
    }

    /**
     * @param $orderIDs
     * @param null $type
     * @return bool
     */
    public function getOrdersAddresses($orderIDs, $type = null, $ver = null)
    {
        if (empty($orderIDs)) {
            return false;
        }
        $binds = array();
        $query = 'SELECT orderAddress.orderID, addressProduct.volume, address.*, orderAddress.senderID, orderAddress.ID as orderAddressID, orderAddress.type, 
            orderAddress.senderID, orderAddress.deliveryID, orderAddress.joined, orderAddress.collectionPointID, orders.userID, addressProduct.productID  
            FROM `' . $this->getTableName() . '` as orderAddress 
            LEFT JOIN  `' . $this->addressSource . '` as address ON orderAddress.addressID = address.ID
            LEFT JOIN  `dp_orders` as orders ON orders.ID = orderAddress.orderID 
            LEFT JOIN  `dp_orderAddressProducts` as addressProduct ON orderAddress.ID = addressProduct.orderAddressID 
            WHERE orderAddress.orderID IN (' . implode(',', $orderIDs) . ') ';
        if ($type) {
            $query .= ' AND orderAddress.type = :type';
            $binds['type'] = $type;
        }
        if (!$ver) {
            $query .= ' AND orderAddress.`current` = 1 ';
        } else {
            $query .= ' AND orderAddress.ver = :ver ';
            $binds['ver'] = $ver;
        }

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = $this->db->getAll();
        $orderAddressIDs = array();
        $senderIDs = array();
        foreach ($result as $each) {
            $orderAddressIDs[] = $each['orderAddressID'];
            if (intval($each['senderID']) > 0) {
                $senderIDs[] = $each['senderID'];
            }
        }

        return $result;
    }

    /**
     * @param $senderList
     * @return array|bool
     */
    public function getSenderOrdersAddresses($senderList)
    {
        if (empty($senderList)) {
            return false;
        }
        $query = 'SELECT address.*, orderAddress.ID as orderAddressID, orderAddress.type 
            FROM `' . $this->getTableName() . '` as orderAddress 
            LEFT JOIN  `' . $this->addressSource . '` as address ON orderAddress.addressID = address.ID
            WHERE orderAddress.senderID IN (' . implode(',', $senderList) . ') ';

        if (!$this->db->exec($query)) {
            return false;
        }

        $res = $this->db->getAll();

        if (!$res) {
            return false;
        }

        $result = array();
        foreach ($res as $r) {
            $result[$r['orderAddressID']] = $r;
        }
        return $result;
    }

    /**
     * @param $orderAddressIDs
     * @return bool|array
     */
    public function getAddressProducts($orderAddressIDs)
    {
        if (empty($orderAddressIDs)) {
            return false;
        }

        $query = 'SELECT orderAddress.ID, 
                         addressProducts.orderAddressID, 
                         addressProducts.productID, 
                         addressProducts.volume,
                         basePrice.price,
                         basePrice.ID as priceID,
                         basePrice.grossPrice,
                         basePrice.currency,
                         deliveryPrices.joined  
                          FROM `' . $this->addressProductsTable . '` as addressProducts
            LEFT JOIN `' . $this->deliveryPrices . '` as deliveryPrices ON 
            deliveryPrices.productID = addressProducts.productID AND deliveryPrices.volume = addressProducts.volume AND 
            deliveryPrices.deliveryID = orderAddress.deliveryID 
            LEFT JOIN `' . $this->basePrices . '` as basePrice ON basePrice.ID = deliveryPrices.priceID 
            LEFT JOIN `dp_orderAddress` as orderAddress ON orderAddress.ID = addressProducts.orderAddressID 
            WHERE addressProducts.orderAddressID IN (' . implode(',', $orderAddressIDs) . ') AND deliveryPrices.volume = addressProducts.volume
            GROUP BY addressProducts.orderAddressID ';

        if (!$this->db->exec($query)) {
            return false;
        }
        return $this->db->getAll();
    }

    /**
     * @param $orderID
     * @param int $type
     * @return bool
     */
    public function deleteByOrder($orderID, $type = 1)
    {
        $query = ' DELETE FROM `' . $this->getTableName() . '` WHERE `orderID` = :orderID AND `type` = :type ';

        $binds['orderID'] = $orderID;
        $binds['type'] = $type;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @param $list
     * @return bool|array
     */
    public function getByList($list)
    {
        if (empty($list)) {
            return false;
        }

        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `ID` IN (' . implode(',', $list) . ') ';

        if (!$this->db->exec($query)) {
            return false;
        }

        $res = $this->db->getAll();
        if (!$res) {
            return false;
        }

        foreach ($res as $key => $value) {
            $result[$value['ID']] = $value;
        }
        return $result;
    }

    /**
     * @param $orderID
     * @param int $type
     * @return bool|array
     */
    public function getByOrder($orderID, $type = 1)
    {
        $query = ' SELECT orderAddress.*, orderAddressProduct.productID, orderAddressProduct.volume  FROM `' . $this->getTableName() . '` as orderAddress
        LEFT JOIN `' . $this->addressProductsTable . '` as orderAddressProduct ON orderAddressProduct.`orderAddressID` = orderAddress.`ID`
        WHERE orderAddress.`orderID` = :orderID AND orderAddress.`type` = :type ';

        $binds['orderID'] = $orderID;
        $binds['type'] = $type;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->getAll();
    }

    public function getOrdersInvoiceAddresses($orderIDs)
    {
        if (empty($orderIDs)) {
            return false;
        }
        $query = 'SELECT * FROM `' . $this->getTableName() . '` as orderAddress 
            WHERE orderAddress.orderID IN (' . implode(',', $orderIDs) . ') ';

        $query .= ' AND orderAddress.type = 2';


        $binds = array();

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();

        if (!$res) {
            return false;
        }

        $result = array();
        foreach ($res as $r) {
            $result[$r['orderID']] = $r;
        }
        return $result;
    }

    public function deliveriesHistory($orderID)
    {
        if (!$this->db->exec('select orderAddress.*,
       orderAddressUpdates.created, orderAddressUpdates.userName, orderAddressUpdates.reason,
       GROUP_CONCAT( DISTINCT CONCAT_WS("::", deliveryNames.lang, deliveryNames.name) SEPARATOR "||")  langs,
    GROUP_CONCAT( DISTINCT CONCAT_WS("::", orderAddressProducts.productID, orderAddressProducts.volume) SEPARATOR "||")  products
from dp_orderAddress orderAddress
         left join dp_orderAddressUpdatesAssoc orderAddressUpdatesAssoc on orderAddressUpdatesAssoc.orderAddressID=orderAddress.ID
         left join dp_orderAddressUpdates orderAddressUpdates on orderAddressUpdates.ID=orderAddressUpdatesAssoc.updateID
         left join dp_config_deliveries deliveries on deliveries.ID=orderAddress.deliveryID
         left join dp_config_deliveryNames deliveryNames on deliveryNames.deliveryID=deliveries.ID
         left join dp_orderAddressProducts orderAddressProducts on orderAddressProducts.orderAddressID=orderAddress.ID
where orderAddress.orderID=:orderID
and type=1
group by orderAddress.ID
order by orderAddress.ver desc;', ['orderID' => $orderID])) {
            return false;
        }
        $list = $this->db->getAll();
        foreach ($list as &$oa) {
            DataUtils::langVersions($oa);
            $products = DataUtils::groupConcatToTree($oa['products']);
            $productsData=[];
            $priceSum=0;
            foreach ($products as $prodID => $volume) {
                if (!$this->db -> exec('select types.name
                     from
                     dp_products dpProducts
                     left join ps_user_calc calc on dpProducts.calcID=calc.ID
                     left join ps_products_types types on types.ID=calc.typeID
                     where dpProducts.ID=:ID', ['ID' => $prodID])) {
                    return false;
                }
                $prodName = $this->db->getOne();
                $productsData[]=['name'=>$prodName, 'volume'=>$volume];
                $priceData = $this->UserDeliveryPrice->getByOrderAddress($volume, $oa['deliveryID'], $prodID);
                $priceSum+=$priceData['grossPrice'];
            }
            $oa['products'] = $productsData;
            $oa['price'] = $this->Price->getPriceToView($priceSum);
        }
        return $list;
    }

    /**
     * @return bool
     */
    public function makeHistorical($orderID, $loggedUser, $reason, $type, $orderAddressIds)
    {
        if (empty($orderAddressIds)) {
            return false;
        }

        if (!$this->db->exec("select count(1) from dp_orderAddress  where orderID=:orderID and `current` = 1 and type = :type and ID not in(" . join(',', $orderAddressIds) . ")", ['orderID' => $orderID, 'type' => $type])) {
            return false;
        }
        $oldAddressesCount=$this->db->getOne() ;

        if($oldAddressesCount>0){
            if (!$this->db->exec("update dp_orderAddress set `current` = 0 where orderID=:orderID and `current` = 1 and type = :type and ID not in(" . join(',', $orderAddressIds) . ")", ['orderID' => $orderID, 'type' => $type])) {
                return false;
            }
            if (!$this->db->exec("select ifnull(max(ver),0) from dp_orderAddress  where orderID=:orderID and type = :type and `current` = 0", ['orderID' => $orderID, 'type' => $type])) {
                return false;
            }
            $nextVer = $this->db->getOne() +1;
            if (!$this->db->exec("update dp_orderAddress set ver = :ver where ID in(" . join(',', $orderAddressIds) . ")", ['ver' => $nextVer])) {
                return false;
            }
        }

        if (!$this->db->exec("select ifnull(max(ID),0)+1 from dp_orderAddressUpdates")) {
            return false;
        }
        $nextID = $this->db->getOne();
        if (!$this->db->exec("insert into dp_orderAddressUpdates (ID, userID, userName, isSuperUser,  reason) values( :ID, :userID, :userName , :isSuperUser, :reason)",
            ['ID' => $nextID, 'userID' => $loggedUser['ID'], 'userName' => "{$loggedUser['firstname']} {$loggedUser['lastname']}", 'isSuperUser' => $loggedUser['super'], 'reason' => $reason])) {
            return false;
        }

        foreach ($orderAddressIds as $id) {
            if (!$this->db->exec("insert into dp_orderAddressUpdatesAssoc (updateID, orderAddressID) values(:updateID, :orderAddressID)",
                ['updateID' => $nextID, 'orderAddressID' => $id])) {
                return false;
            }

        }

        return true;
    }

}
