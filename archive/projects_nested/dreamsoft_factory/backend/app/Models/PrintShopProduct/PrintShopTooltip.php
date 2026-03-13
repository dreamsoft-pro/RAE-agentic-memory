<?php

namespace DreamSoft\Models\PrintShopProduct;

use DreamSoft\Models\PrintShop\PrintShop;
use PDO;

/**
 * Description of PrintshopTooltip
 *
 * @author Rafał
 */
class PrintShopTooltip extends PrintShop {
    
    public function __construct(){
        parent::__construct();
        $prefix = true;
        $this->setTableName('products_tooltips', $prefix);
    }

    /**
     * @param $typeID
     * @param $attributes
     * @return array|bool
     */
    public function getByAttributes($typeID, $attributes)
    {
        if (empty($attributes)) {
            return false;
        }

        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE typeID = :typeID AND '
            . ' attrID IN (' . implode(',', array_values($attributes)) . ') ';

        $binds['typeID'] = $typeID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll(PDO::FETCH_ASSOC);
        if (!$res) {
            return false;
        }

        $result = array();
        foreach ($res as $key => $val) {
            $result[$val['attrID']][$val['langCode']] = $val['tooltip'];
        }
        return $result;
    }
    
}
