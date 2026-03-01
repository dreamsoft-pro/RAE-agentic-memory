<?php

namespace DreamSoft\Models\PrintShopProduct;

use DreamSoft\Models\PrintShop\PrintShop;

/**
 * Description of PrintShopTypeTax
 *
 * @author Rafał
 */
class PrintShopTypeTax extends PrintShop
{

    private $tableTax;
    /**
     * PrintShopTypeTax constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('products_typeTaxes', true);
        $this->tableTax = $this->prefix . 'tax';
    }


    /**
     * @param $list
     * @param $groupID
     * @param null $typeID
     * @return bool
     */
    public function createFromList($list, $groupID, $typeID = NULL)
    {

        if (!$typeID) {
            $this->removeByGroup($groupID);
        } else {
            $this->removeByType($typeID);
        }

        if (empty($list)) {
            return false;
        }

        $params['groupID'] = $groupID;
        $params['typeID'] = $typeID;
        $params['domainID'] = $this->getDomainID();
        $created = 0;
        foreach ($list as $taxID) {
            $params['taxID'] = $taxID;
            if ($this->create($params) > 0) {
                $created++;
            }
        }
        if ($created > 0) {
            return true;
        }
        return false;
    }

    /**
     * @param $groupID
     * @return bool
     */
    public function removeByGroup($groupID)
    {
        $query = 'DELETE FROM `' . $this->getTableName() . '` 
        WHERE `groupID` = :groupID AND `typeID` IS NULL AND `domainID` = :domainID ';

        $binds['groupID'] = $groupID;
        $binds['domainID'] = $this->getDomainID();

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    /**
     * @param $typeID
     * @return bool
     */
    public function removeByType($typeID)
    {
        $query = 'DELETE FROM `' . $this->getTableName() . '` WHERE `typeID` = :typeID AND `domainID` = :domainID ';

        $binds['typeID'] = $typeID;
        $binds['domainID'] = $this->getDomainID();

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    /**
     * @param $groupID
     * @return array|bool
     */
    public function getByGroup($groupID)
    {
        $query = 'SELECT `taxID` FROM `' . $this->getTableName() . '` 
        WHERE `groupID` = :groupID AND `typeID` IS NULL AND `domainID` = :domainID ';

        $binds['groupID'] = $groupID;
        $binds['domainID'] = $this->getDomainID();

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();
        if (!$res) {
            return false;
        }
        $result = array();
        foreach ($res as $value) {

            $result[] = $value['taxID'];

        }

        return $result;
    }

    /**
     * @param $typeID
     * @return array|bool
     */
    public function getByType($typeID)
    {
        $query = 'SELECT `taxID` FROM `' . $this->getTableName() . '`
         WHERE `typeID` = :typeID AND `domainID` = :domainID ';

        $binds['typeID'] = $typeID;
        $binds['domainID'] = $this->getDomainID();

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();
        if (!$res) {
            return false;
        }
        $result = array();
        foreach ($res as $value) {

            $result[] = $value['taxID'];

        }
        return $result;
    }
}
