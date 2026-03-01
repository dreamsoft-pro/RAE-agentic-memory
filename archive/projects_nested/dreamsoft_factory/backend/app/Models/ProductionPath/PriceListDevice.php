<?php

namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

class PriceListDevice extends Model
{

    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('priceListDevices', $prefix);
    }
    public function getByPriceListID($priceListID)
    {
        $query = 'SELECT deviceID FROM `dp_priceListDevices` '
            . ' WHERE `priceListID` = :priceListID ';

        $binds[':priceListID'] = $priceListID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();
    }
}

?>
