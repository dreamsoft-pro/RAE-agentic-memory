<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Models\PrintShop\PrintShop;
use PDO;

class PrintShopConfigEfficiency extends PrintShop
{

    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('device_efficiency_overrides', $prefix);
    }

    /**
     * @return array|bool
     */
    public function customGet()
    {
        if (empty($this->attrID)) return false;
        if (empty($this->optID)) return false;

        $query = 'SELECT * FROM `ps_device_efficiency_overrides` 
                WHERE `attrID` = :attrID AND `optID` = :optID';
        if ($this->controllerID) {
            $query .= ' AND `controllerID` = :controllerID ';
            $binds[':controllerID'] = $this->controllerID;
        }
        $binds[':attrID'] = array($this->attrID, 'int');
        $binds[':optID'] = array($this->optID, 'int');

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getRow(PDO::FETCH_ASSOC);

    }

}
