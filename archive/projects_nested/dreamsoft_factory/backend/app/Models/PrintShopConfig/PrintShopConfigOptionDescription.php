<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Models\PrintShop\PrintShop;
use PDO;

class PrintShopConfigOptionDescription extends PrintShop
{

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('config_option_description', true);
    }

    public function customExists($typeID, $domainID)
    {
        $query = 'SELECT * FROM `ps_config_option_description` 
                    WHERE `optionDescriptionTypeID` = :optionDescriptionTypeID
                      AND  `attributeID` = :attributeID 
                      AND  `optionID` = :optionID
                      AND  `domainID` = :domainID';

        $binds[':optionDescriptionTypeID'] = $typeID;
        $binds[':attributeID'] = $this->attrID;
        $binds[':optionID'] = $this->optID;
        $binds[':domainID'] = $domainID;

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getOne();
    }

    public function customCreate($optionDescriptionTypeID, $value, $domainID)
    {
        $query = 'INSERT INTO `ps_config_option_description` 
            ( `attributeID`, `optionID`, `optionDescriptionTypeID`, `value`, `domainID`) VALUES
            ( :attributeID, :optionID, :optionDescriptionTypeID, :value, :domainID )';

        $binds[':attributeID'] = $this->attrID;
        $binds[':optionID'] = $this->optID;
        $binds[':optionDescriptionTypeID'] = $optionDescriptionTypeID;
        $binds[':value'] = $value;
        $binds[':domainID'] = $domainID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->lastInsertID();
    }

    public function batchInsert($insertArray)
    {
        $query = 'INSERT INTO `ps_config_option_description` 
            ( `attributeID`, `optionID`, `optionDescriptionTypeID`, `value`, `domainID`) VALUES ';
            
        $isFirstRow = true;
        foreach($insertArray as $singleData){
            if($isFirstRow == true){
                $isFirstRow = false;
            }else{
                $query .= ',';
            } 
            $query .= '('.$singleData['attributeID'].', '.$singleData['optionID'].', '.$singleData['optionDescriptionTypeID'].', '.$this->db->getPdo()->quote($singleData['value']).', '.$singleData['domainID'].')';          
        }
        if (!$this->db->exec($query)) {
            return false;
        }
        return true;
    }

    public function removeAllDescriptionsForOption($attributeID, $domainID, $optionID)
    {
        $query = 'DELETE FROM `ps_config_option_description` WHERE optionID = :optionID AND domainID = :domainID AND attributeID = :attributeID;';
            
        $binds[':attributeID'] = $attributeID;
        $binds[':optionID'] = $optionID;
        $binds[':domainID'] = $domainID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    public function customUpdate($optionDescriptionTypeID, $value, $domainID)
    {
        $query = 'UPDATE `ps_config_option_description` 
            SET `value` = :value
            WHERE `attributeID` = :attributeID
            AND `optionID` = :optionID
            AND `optionDescriptionTypeID` = :optionDescriptionTypeID
            AND `domainID` = :domainID';

        $binds[':value'] = $value;
        $binds[':attributeID'] = $this->attrID;
        $binds[':optionID'] = $this->optID;
        $binds[':optionDescriptionTypeID'] = $optionDescriptionTypeID;
        $binds[':domainID'] = $domainID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    public function customGetAll($group, $domainID)
    {
        $query = 'SELECT `ID`, `name`, `editor` FROM `ps_config_option_description_type` WHERE `group` = :group';

        if (!$this->db->exec($query, [':group' => $group])) return false;

        $types = $this->db->getAll();
        $query = 'SELECT `optionDescriptionTypeID`, `value` FROM `ps_config_option_description` 
                    WHERE `attributeID` = :attributeID 
                    AND `optionID` = :optionID AND `domainID` = :domainID';
        if (!$this->db->exec($query, [':attributeID' => $this->attrID, ':optionID' => $this->optID, ':domainID' => $domainID])) return false;
        $values = $this->db->getAll();
        foreach ($values as $value) {
            foreach ($types as &$type) {
                if ($type['ID'] === $value['optionDescriptionTypeID']) {
                    $type['value'] = $value['value'];
                    break;
                }
            }
        }
        return $types;
    }

    public function getByTypeName($name)
    {
        $query = 'SELECT d.value FROM `ps_config_option_description` d
        JOIN  ps_config_option_description_type t on  t.ID = d.optionDescriptionTypeID     
            WHERE 
        t.`name` = :name AND d.attributeID=:attributeID AND d.optionID=:optionID AND d.domainID=:domainID';

        if (!$this->db->exec($query, [':attributeID' => $this->attrID,
            ':optionID' => $this->optID,
            ':domainID' => $this->domainID,
            ':name' => $name])) return false;
        $row=$this->db->getRow();
        if($row){
            return $row['value'];
        }
        return null;
    }

    public function getForOption()
    {
        $query = 'SELECT d.value,t.name FROM `ps_config_option_description` d
        JOIN  ps_config_option_description_type t on  t.ID = d.optionDescriptionTypeID     
            WHERE 
        d.attributeID=:attributeID AND d.optionID=:optionID AND d.domainID=:domainID';

        if (!$this->db->exec($query, [':attributeID' => $this->attrID,
            ':optionID' => $this->optID,
            ':domainID' => $this->domainID])) return false;
        return $this->db->getAll();
    }

    public function getValuesByTypeName($name)
    {
        $query = 'SELECT d.value FROM `ps_config_option_description` d
        JOIN  ps_config_option_description_type t on  t.ID = d.optionDescriptionTypeID     
            WHERE 
        t.`name` = :name AND d.attributeID=:attributeID AND d.domainID=:domainID
        group by d.value 
        order by d.value';

        if (!$this->db->exec($query, [':attributeID' => $this->attrID,
            ':domainID' => $this->domainID,
            ':name' => $name])) return false;
        return $this->db->getAll(PDO::FETCH_COLUMN);
    }

    public function getAllValuesByTypeName($name)
    {
        $query = 'SELECT d.value FROM `ps_config_option_description` d
        JOIN  ps_config_option_description_type t on  t.ID = d.optionDescriptionTypeID     
            WHERE 
        t.`name` = :name AND d.domainID=:domainID AND d.value != ""
        group by d.value 
        order by d.value';

        if (!$this->db->exec($query, [':domainID' => $this->domainID,
            ':name' => $name])) return false;
        return $this->db->getAll(PDO::FETCH_COLUMN);
    }

    public function getValuesForType($typeName)
    {
        $query = 'SELECT d.* FROM `ps_config_option_description` d
        JOIN  ps_config_option_description_type t on  t.ID = d.optionDescriptionTypeID     
            WHERE 
        t.`name` = :name AND d.attributeID=:attributeID AND d.optionID=:optionID AND d.domainID=:domainID';

        if (!$this->db->exec($query, [':attributeID' => $this->attrID,
            ':optionID' => $this->optID,
            ':domainID' => $this->domainID,
            ':name' => $typeName])) return false;
        return $this->db->getAll();
    }

    public function getDescriptionIDByName($name)
    {
        $query = 'SELECT `ID` FROM `ps_config_option_description_type` WHERE `name` = :name AND `group` = "paper"';

        $binds[':name'] = $name;
        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getOne();
    }

    /**
     * @param $names array
     * @return false|mixed|null
     */
    public function getTypesData($names)
    {
        $names = array_map(function ($item) {
            return "'$item'";
        }, $names);
        $query = 'SELECT ID, name from ps_config_option_description_type    
            WHERE 
        name in(' . join(',', $names) . ')';

        if (!$this->db->exec($query)) return false;
        return $this->db->getAll();
    }

}
