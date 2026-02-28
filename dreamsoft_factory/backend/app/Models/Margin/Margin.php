<?php

namespace DreamSoft\Models\Margin;

use DreamSoft\Core\Model;

class Margin extends Model
{
    public function __construct($root = false, $companyID = NULL)
    {
        $this->setTableName('margins', true);
        parent::__construct($root, $companyID);
    }

    public function customGetAll($priceListID, $natureID)
    {

        $query = ' SELECT * FROM ' . $this->getTableName() . ' WHERE natureID = :natureID AND priceTypeID= :priceTypeID 
        AND ISNULL(groupID) AND ISNULL(typeID)';
        if (!$this->db->exec($query, ['natureID' => $natureID, 'priceTypeID' => $priceListID])) {
            return false;
        }

        return $this->db->getAll();
    }

    public function customGetAllPriceNature($priceListID, $natureID)
    {

        $query = ' SELECT * FROM ' . $this->getTableName() . ' WHERE natureID = :natureID AND priceTypeID= :priceTypeID
        order by typeID desc, groupID desc';
        if (!$this->db->exec($query, ['natureID' => $natureID, 'priceTypeID' => $priceListID])) {
            return false;
        }

        return $this->db->getAll();
    }

    public function customGetAllInGroup($priceListID, $natureID, $groupID)
    {
        $query = ' SELECT * FROM ' . $this->getTableName() . ' 
        WHERE natureID = :natureID AND priceTypeID= :priceTypeID 
        AND groupID = :groupID';
        if (!$this->db->exec($query, ['natureID' => $natureID, 'priceTypeID' => $priceListID, 'groupID' => $groupID])) {
            return false;
        }

        return $this->db->getAll();
    }

    public function customGetAllInType($priceListID, $natureID, $typeID)
    {
        $query = ' SELECT * FROM ' . $this->getTableName() . ' 
        WHERE natureID = :natureID AND priceTypeID= :priceTypeID 
        AND typeID = :typeID';
        if (!$this->db->exec($query, ['natureID' => $natureID, 'priceTypeID' => $priceListID, 'typeID' => $typeID])) {
            return false;
        }

        return $this->db->getAll();
    }

    public function findMargins($priceListTypeID, $natureID, $pieces, $sheets, $sqmeters, $kilograms, $meters)
    {
        $all = $this->customGetAllPriceNature($priceListTypeID, $natureID);
        $percents = [];
        $fields = ['pieces' => $pieces, 'sheets' => $sheets, 'sqmeters' => $sqmeters, 'kilograms' => $kilograms, 'meters' => $meters];
        foreach ($fields as $key => $value) {
            foreach ($all as $margin) {
                if ($value && $value >= $margin["${key}Min"] && $value <= $margin["${key}Max"]) {
                    $percents[] = ['percentage'=>$margin['percentage'], 'groupID'=>$margin['groupID'], 'typeID'=>$margin['typeID']];
                }
            }
        }

        return $percents;
    }
}
