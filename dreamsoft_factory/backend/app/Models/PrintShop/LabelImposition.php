<?php


namespace DreamSoft\Models\PrintShop;


use DreamSoft\Core\Model;

class LabelImposition extends Model

{
    public function __construct($root = false, $companyID = NULL)
    {
        $this->setTableName('ps_labelImposition',false);
        parent::__construct($root, $companyID);
    }

    public function getForType($typeID){
        $this->db->exec('select * from ps_labelImposition where productTypeID=:productTypeID',['productTypeID'=>$typeID]);
        return $this->db->getRow();
    }

}
