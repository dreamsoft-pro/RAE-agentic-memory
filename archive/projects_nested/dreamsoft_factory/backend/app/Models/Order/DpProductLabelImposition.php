<?php

namespace DreamSoft\Models\Order;

use DreamSoft\Core\Model;

class DpProductLabelImposition extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('productLabelImposition', true);
    }


}
