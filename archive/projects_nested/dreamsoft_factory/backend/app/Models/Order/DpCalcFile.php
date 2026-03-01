<?php
namespace DreamSoft\Models\Order;


use DreamSoft\Core\Model;


class DpCalcFile extends Model
{
    protected $userTable;

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('calcFiles', true);
    }

}