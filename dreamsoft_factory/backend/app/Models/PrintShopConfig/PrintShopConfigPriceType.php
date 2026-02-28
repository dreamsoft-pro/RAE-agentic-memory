<?php


namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Models\PrintShop\PrintShop;

class PrintShopConfigPriceType extends PrintShop
{

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('config_priceTypes', true);
    }

    public function getForDevices()
    {
        $query = 'SELECT * FROM `ps_config_priceTypes` where devicesType=1';
        if (!$this->db->exec($query)) return false;
        return $this->db->getAll();
    }
}
