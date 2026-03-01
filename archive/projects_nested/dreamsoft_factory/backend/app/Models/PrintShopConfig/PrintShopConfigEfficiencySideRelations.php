<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Models\PrintShop\PrintShop;
use PDO;

class PrintShopConfigEfficiencySideRelations extends PrintShop
{

    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('device_side_relations_overrides', $prefix);
    }

    /**
     * @return array|bool
     */
    public function getOrderedList()
    {
        $query = 'SELECT * FROM `ps_device_side_relations_overrides` 
                WHERE `attrID` = :attrID AND `optID` = :optID';
        if ($this->controllerID) {
            $query .= ' AND `controllerID` = :controllerID ';
            $binds[':controllerID'] = $this->controllerID;
        }
        $query .=' ORDER BY efficiencyChange';
        $binds[':attrID'] = array($this->attrID, 'int');
        $binds[':optID'] = array($this->optID, 'int');

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getAll();

    }
    public function getOrderedListByRelation()
    {
        $query = 'select *,sideRelationHeight/sideRelationWidth as relation from ps_device_side_relations_overrides 
            WHERE `attrID` = :attrID AND `optID` = :optID';
        if ($this->controllerID) {
            $query .= ' AND `controllerID` = :controllerID ';
            $binds[':controllerID'] = $this->controllerID;
        }
        $query.=' order by relation';
        $binds[':attrID'] = array($this->attrID, 'int');
        $binds[':optID'] = array($this->optID, 'int');
        if (!$this->db->exec($query, $binds)) return false;
        return $this->db->getAll();
    }
}
