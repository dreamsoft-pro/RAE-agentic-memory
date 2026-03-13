<?php

namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

class ExternalData extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('external_data', true);
    }


    public function getByParams($orderID, $deviceID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `orderID` = :orderID AND `deviceID` = :deviceID ';

        $binds['orderID'] = $orderID;
        $binds['deviceID'] = $deviceID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getRow();
    }
}
