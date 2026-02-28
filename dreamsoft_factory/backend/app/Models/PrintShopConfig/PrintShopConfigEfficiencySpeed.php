<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Models\PrintShop\PrintShop;
use PDO;

class PrintShopConfigEfficiencySpeed extends PrintShop
{

    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('device_speeds_overrides', $prefix);
    }

    /**
     * @return array|bool
     */
    public function getOrderedList()
    {
        $query = 'SELECT * FROM `ps_device_speeds_overrides` 
                WHERE `attrID` = :attrID AND `optID` = :optID';
        if ($this->controllerID) {
            $query .= ' AND `controllerID` = :controllerID ';
            $binds[':controllerID'] = $this->controllerID;
        }
        $query .= ' ORDER BY volume';
        $binds[':attrID'] = array($this->attrID, 'int');
        $binds[':optID'] = array($this->optID, 'int');

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getAll(PDO::FETCH_ASSOC);

    }

}
