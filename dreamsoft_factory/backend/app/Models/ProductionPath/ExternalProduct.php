<?php

namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

class ExternalProduct extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('external_products', true);
    }

}
