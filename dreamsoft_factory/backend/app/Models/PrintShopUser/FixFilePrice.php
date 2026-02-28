<?php

namespace DreamSoft\Models\PrintShopUser;


use DreamSoft\Core\Model;


class FixFilePrice extends Model
{

    public function __construct()
    {
        parent::__construct();
        $this->prefix = 'ps_user_';
        $this->setTableName('fixFilePrices', true);
    }

}
