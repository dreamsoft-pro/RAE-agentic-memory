<?php
namespace DreamSoft\Models\Order;


use DreamSoft\Core\Model;
use DreamSoft\Models\Behaviours\QueryFilter;


class DpCartsData extends Model
{
    /**
     * @var QueryFilter
     */
    protected $QueryFilter;

    /**
     * DpOrder constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->QueryFilter = QueryFilter::getInstance();
        $this->setTableName('carts_data', true);
    }

    public function updateProductAddresses($productID, $orderID, $productAddresses){
        $query = 'UPDATE `' . $this->getTableName() . '` 
            SET `productAddresses` = :productAddresses
            WHERE `productID` = :productID AND `orderID` = :orderID
            ';
        $binds[':productID'] = $productID;
        $binds[':orderID'] = $orderID;
        $binds[':productAddresses'] = $productAddresses;

        if (!$this->db->exec($query, $binds)) return false;

        return true;
    }

    public function updateUserCart($calcID, $userID){
        $query = 'UPDATE `' . $this->getTableName() . '` 
            SET `userID` = :userID
            WHERE `calcID` = :calcID
            ';
        $binds[':calcID'] = $calcID;
        $binds[':userID'] = $userID;

        if (!$this->db->exec($query, $binds)) return false;

        return true;
    }
}