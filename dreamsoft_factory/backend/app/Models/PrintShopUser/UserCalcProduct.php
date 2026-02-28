<?php

namespace DreamSoft\Models\PrintShopUser;

use DreamSoft\Core\Model;
use DreamSoft\Models\Behaviours\LangFilter;

/**
 * Class UserCalcProduct
 * @package DreamSoft\Models\PrintShopUser
 */
class UserCalcProduct extends Model
{

    protected $formatLangs;
    protected $formats;
    protected $types;
    protected $groups;

    /**
     * @var LangFilter
     */
    protected $LangFilter;

    /**
     * UserCalcProduct constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->prefix = 'ps_user_';
        $this->setTableName('calc_products', true);
        $this->groups = 'ps_products_groups';
        $this->types = 'ps_products_types';
        $this->typeLangs = 'ps_products_typeLangs';
        $this->formats = 'ps_products_formats';
        $this->formatLangs = 'ps_products_formatLangs';
        $this->LangFilter = new LangFilter();
    }

    /**
     * @param $ids
     * @return array|bool
     */
    public function getByCalcIds($ids)
    {
        if (empty($ids)) {
            return false;
        }

        $query = 'SELECT calcProduct.*, groupTable.name as groupName, `type`.name as typeName, format.name as formatName,
                 GROUP_CONCAT( DISTINCT CONCAT_WS("::", formatLang.lang, formatLang.name) SEPARATOR "||" ) as formatLangs,
                 GROUP_CONCAT( DISTINCT CONCAT_WS("::", typeLang.lang, typeLang.name) SEPARATOR "||" ) as typeLangs,
                 GROUP_CONCAT( DISTINCT CONCAT_WS("::", pll.lang, pll.name) SEPARATOR "||" ) as plLangs,
                  format.slope as formatSlope, `type`.skipUpload, format.custom as customFormat, 
                  format.unit as formatUnit, pl.name as priceListName, concat("'.STATIC_URL.'","uploadedFiles/' . companyID . '/priceListIcons/",uf.path) priceTypeIcon
  			 FROM `' . $this->getTableName() . '` as calcProduct ';
        $query .= ' LEFT JOIN `' . $this->groups . '` as groupTable ON groupTable.`ID` = calcProduct.`groupID` ';
        $query .= ' LEFT JOIN `' . $this->types . '` as type ON type.`ID` = calcProduct.`typeID` ';
        $query .= ' LEFT JOIN `' . $this->typeLangs . '` as typeLang ON type.`ID` = typeLang.`typeID` ';
        $query .= ' LEFT JOIN `' . $this->formats . '` as format ON format.`ID` = calcProduct.`formatID` ';
        $query .= ' LEFT JOIN `' . $this->formatLangs . '` as formatLang ON format.`ID` = formatLang.`formatID` ';
        $query .= ' LEFT JOIN ps_config_printTypes pt on pt.ID=calcProduct.printTypeID';
        $query .= ' LEFT JOIN ps_config_priceLists pl on pl.ID=pt.pricelistID';
        $query .= ' LEFT JOIN ps_config_priceListLanguages pll on pll.priceListID=pl.ID';
        $query .= ' LEFT JOIN uploadedFiles uf on uf.ID =  pl.iconID';
        $query .= ' WHERE calcProduct.`calcID` IN (' . implode(',', $ids) . ') ';

        $query .= ' GROUP BY calcProduct.ID ';

        $binds = array();
        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = array();
        $res = $this->db->getAll();

        $res = $this->LangFilter->splitArray($res, 'formatLangs');
        $res = $this->LangFilter->splitArray($res, 'typeLangs');
        $res = $this->LangFilter->splitArray($res, 'plLangs');

        foreach ($res as $each) {
            if (!isset($result[$each['calcID']])) {
                $result[$each['calcID']] = array();
            }
            $result[$each['calcID']][] = $each;
        }

        return $result;
    }


    /**
     * @param $ids
     * @return array|bool
     */
    public function getByProductCalcIds($ids)
    {
        if (empty($ids)) {
            return false;
        }

        $query = 'SELECT calcProduct.*, groupTable.name as groupName, `type`.name as typeName, format.name as formatName,
                 GROUP_CONCAT( DISTINCT CONCAT_WS("::", formatLang.lang, formatLang.name) SEPARATOR "||" ) as formatLangs,
                  format.slope as formatSlope, `type`.skipUpload, format.custom as customFormat, 
                  format.unit as formatUnit 
  			 FROM `' . $this->getTableName() . '` as calcProduct ';
        $query .= ' LEFT JOIN `' . $this->groups . '` as groupTable ON groupTable.`ID` = calcProduct.`groupID` ';
        $query .= ' LEFT JOIN `' . $this->types . '` as type ON type.`ID` = calcProduct.`typeID` ';
        $query .= ' LEFT JOIN `' . $this->formats . '` as format ON format.`ID` = calcProduct.`formatID` ';
        $query .= ' LEFT JOIN `' . $this->formatLangs . '` as formatLang ON format.`ID` = formatLang.`formatID` ';
        $query .= ' WHERE calcProduct.`ID` IN (' . implode(',', $ids) . ') ';

        $query .= ' GROUP BY calcProduct.ID ';

        $binds = array();
        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = array();
        $res = $this->db->getAll();

        $res = $this->LangFilter->splitArray($res, 'formatLangs');

        foreach ($res as $each) {
            if (!isset($result[$each['ID']])) {
                $result[$each['ID']] = array();
            }
            $result[$each['ID']][] = $each;
        }

        return $result;
    }

    /**
     * @param $ids
     * @return array|bool
     */
    public function getByList($ids)
    {
        if (empty($ids)) {
            return false;
        }
        $query = 'SELECT calcProduct.*, groupTable.name as groupName, type.name as typeName, format.name as formatName,
                 GROUP_CONCAT( DISTINCT CONCAT_WS("::", formatLang.lang, formatLang.name) SEPARATOR "||" ) as formatLangs,
                  format.slope as formatSlope 
  			 FROM `' . $this->getTableName() . '` as calcProduct ';
        $query .= ' LEFT JOIN `' . $this->groups . '` as groupTable ON groupTable.`ID` = calcProduct.`groupID` ';
        $query .= ' LEFT JOIN `' . $this->types . '` as type ON type.`ID` = calcProduct.`typeID` ';
        $query .= ' LEFT JOIN `' . $this->formats . '` as format ON format.`ID` = calcProduct.`formatID` ';
        $query .= ' LEFT JOIN `' . $this->formatLangs . '` as formatLang ON format.`ID` = formatLang.`formatID` ';
        $query .= ' WHERE calcProduct.`ID` IN (' . implode(',', $ids) . ') ';

        $query .= ' GROUP BY calcProduct.ID ';

        $binds = array();

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = array();
        $res = $this->db->getAll();

        $res = $this->LangFilter->splitArray($res, 'formatLangs');

        foreach ($res as $each) {
            $result[$each['ID']] = $each;
        }

        return $result;
    }

    function getDpProduct($ID)
    {
        $this->db->exec('select dp.* from ps_user_calc_products cp
            join dp_products dp on cp.calcID = dp.calcID
            where cp.ID=:ID', ['ID' => $ID]);
        return $this->db->getRow();
    }
}
