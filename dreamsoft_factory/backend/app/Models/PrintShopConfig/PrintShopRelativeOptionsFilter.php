<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Models\PrintShop\PrintShop;
use PDO;

class PrintShopRelativeOptionsFilter extends PrintShop
{

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('alternative_options_filter', true);
    }

    public function getOptionFilter($attrID, $optID){
        $query = 'SELECT * FROM ps_alternative_options_filter where
                    attrID=:attrID and optID=:optID';

        if (!$this->db->exec($query,['attrID'=>$attrID,'optID'=>$optID])) return false;

        return $this->db->getAll(PDO::FETCH_ASSOC);
    }

    public function getUsedOptions($attrID){
        $query = 'SELECT optID FROM ps_alternative_options_filter where
                    attrID=:attrID group by optID';

        if (!$this->db->exec($query,['attrID'=>$attrID])) return false;

        return $this->db->getAll(PDO::FETCH_COLUMN);
    }
}
