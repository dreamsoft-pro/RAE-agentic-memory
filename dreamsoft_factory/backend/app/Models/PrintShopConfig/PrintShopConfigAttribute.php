<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Libs\DataUtils;
use DreamSoft\Models\Behaviours\LangFilter;
use DreamSoft\Models\PrintShop\PrintShop;
use PDO;

/**
 * Class PrintShopConfigAttribute
 */
class PrintShopConfigAttribute extends PrintShop
{

    /**
     * @var string
     */
    protected $tableAttributeRanges;
    /**
     * @var string
     */
    protected $tableAttributeTypes;
    /**
     * @var string
     */
    protected $tableAttributeLangs;
    protected $tableAttributeDescriptionLangs;
    /**
     * @var LangFilter
     */
    private $LangFilter;

    /**
     * PrintShopConfigAttribute constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('config_attributes', $prefix);
        if ($prefix) {
            $this->tableAttributeRanges = $this->prefix . 'config_attributeRanges';
            $this->tableAttributeTypes = $this->prefix . 'config_attributeTypes';
            $this->tableAttributeLangs = $this->prefix . 'config_attributeLangs';
            $this->tableAttributeDescriptionLangs = $this->prefix . 'config_attribute_description_lang';
        }
        $this->LangFilter = new LangFilter();
    }

    /**
     * @return array|bool
     */
    public function getAll()
    {
        $query = 'SELECT `' . $this->getTableName() . '`.`ID`, 
                        `' . $this->getTableName() . '`.`name`,
                        `' . $this->getTableName() . '`.`iconID`,
                         `' . $this->getTableName() . '`.`adminName`,
                         `' . $this->getTableName() . '`.`type`,
                         `' . $this->getTableName() . '`.`natureID`,
                         `' . $this->getTableName() . '`.`sort`,
                         `' . $this->getTableName() . '`.`rangeID`,
                         `' . $this->getTableName() . '`.`multipleOptionsMax`,
                         `' . $this->getTableName() . '`.`displayImageOnMiniature`,
                         `' . $this->getTableName() . '`.`specialFunction`,
                         `' . $this->tableAttributeRanges . '`.`minPages`,
                         `' . $this->tableAttributeRanges . '`.`step`,
                         `' . $this->tableAttributeRanges . '`.`maxPages`,
                         `' . $this->tableAttributeLangs . '`.`lang` as lLang,
                         `' . $this->tableAttributeLangs . '`.`name` as lName,
                         `' . $this->tableAttributeDescriptionLangs . '`.`lang` as ldLang,
                         `' . $this->tableAttributeDescriptionLangs . '`.`description` as lDescription
                    FROM `' . $this->getTableName() . '`
                    LEFT JOIN `' . $this->tableAttributeRanges . '` ON `' . $this->tableAttributeRanges . '`.`ID` = `' . $this->getTableName() . '`.`rangeID`
                    LEFT JOIN `' . $this->tableAttributeLangs . '` ON `' . $this->tableAttributeLangs . '`.`attributeID` = `' . $this->getTableName() . '`.`ID`
                    LEFT JOIN `' . $this->tableAttributeDescriptionLangs . '` ON `' . $this->tableAttributeDescriptionLangs . '`.`attributeID` = `' . $this->getTableName() . '`.`ID`
                    ORDER BY `' . $this->getTableName() . '`.`sort`     ';

        if (!$this->db->exec($query)) return false;
        $res = $this->db->getAll(PDO::FETCH_ASSOC);
        if (!$res) return false;

        $result=DataUtils::includeLanguageTables($res,[['lLang','lName','names'],['ldLang','lDescription','description']]);

        $data = array();
        foreach ($result as $r) {
            $data[] = $r;
        }

        return $data;
    }

    /**
     * @param $name
     * @param $type
     * @param null $rangeID
     * @param null $adminName
     * @return bool|string
     */
    public function customCreate($name, $type, $natureID,  $rangeID, $adminName, $multipleOptionsMax, $displayImageOnMiniature,$specialFunction)
    {
        $query = 'SELECT max(`sort`)+1 FROM `' . $this->getTableName() . '` ';

        if (!$this->db->exec($query)) return false;

        $sort = $this->db->getOne();
        if ($sort == null) $sort = 1;

        if (empty($rangeID)) $rangeID = null;
        if (empty($specialFunction))
            $specialFunction = null;
        $query = ' SELECT MAX(ID) FROM `' . $this->getTableName() . '` LIMIT 1';
        if ($this->db->exec($query)) {
            $tmpLast = $this->db->getOne();
            $tmpLast++;
        }

        $query = 'INSERT INTO `' . $this->getTableName() . '` 
            ( `ID`, `name`, `type`, `natureID`, `adminName`, `rangeID`, `multipleOptionsMax`, `displayImageOnMiniature`, `specialFunction`, `sort` ) VALUES
            ( :tmpLast, :name, :type, :natureID, :adminName, :rangeID, :multipleOptionsMax, :displayImageOnMiniature, :specialFunction, :sort )
                ';
        $binds[':tmpLast'] = $tmpLast;
        $binds[':name'] = $name;
        $binds[':type'] = $type;
        $binds[':natureID'] = $natureID;
        $binds[':rangeID'] = $rangeID;
        $binds[':adminName'] = $adminName;
        $binds[':multipleOptionsMax'] = $multipleOptionsMax;
        $binds[':displayImageOnMiniature'] = $displayImageOnMiniature;
        $binds[':specialFunction'] = $specialFunction;
        $binds[':sort'] = $sort;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->lastInsertID();
    }

    public function customUpdate($id, $name,$iconID, $type, $natureID, $adminName, $multipleOptionsMax, $displayImageOnMiniature, $specialFunction, $attrSizeName = NULL)
    {
        $query = 'UPDATE `' . $this->getTableName() . '` 
            SET `name` = :name, `iconID` = :iconID, `type` = :type, `natureID` = :natureID, `adminName` = :adminName, 
            `attrSizeName` = :attrSizeName, `multipleOptionsMax` = :multipleOptionsMax,
             `displayImageOnMiniature` = :displayImageOnMiniature, `specialFunction` = :specialFunction
            WHERE `ID` = :id
            ';

        $binds[':id'] = $id;
        $binds[':name'] = $name;
        $binds[':iconID'] = $iconID;
        $binds[':type'] = $type;
        $binds[':natureID'] = $natureID;
        $binds[':adminName'] = $adminName;
        $binds[':attrSizeName'] = $attrSizeName;
        $binds[':multipleOptionsMax'] = $multipleOptionsMax;
        $binds[':displayImageOnMiniature'] = $displayImageOnMiniature;
        $binds[':specialFunction'] = $specialFunction;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @param $ID
     * @param $rangeID
     * @return bool
     */
    public function setRangeID($ID, $rangeID)
    {
        $query = 'UPDATE `' . $this->getTableName() . '` 
            SET `rangeID` = :rangeID
            WHERE `ID` = :ID
            ';
        $binds[':rangeID'] = $rangeID;
        $binds[':ID'] = $ID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @param null $id
     * @return bool|array
     */
    public function customGet($id = null)
    {
        $query = 'SELECT `' . $this->getTableName() . '`.`ID`, 
                        `' . $this->getTableName() . '`.`name`,
                         `' . $this->getTableName() . '`.`adminName`,
                         `' . $this->getTableName() . '`.`type`,
                         `' . $this->getTableName() . '`.`natureID`,
                         `' . $this->getTableName() . '`.`sort`,
                         `' . $this->getTableName() . '`.`rangeID`,
                         `' . $this->getTableName() . '`.`multipleOptionsMax`,
                         `' . $this->getTableName() . '`.`displayImageOnMiniature`,
                         `' . $this->tableAttributeRanges . '`.`minPages`,
                         `' . $this->tableAttributeRanges . '`.`step`,
                         `' . $this->tableAttributeRanges . '`.`maxPages`,
                         `' . $this->getTableName() . '`.`attrSizeName`,
                         `' . $this->getTableName() . '`.`specialFunction`,
                         AT.function
                FROM `' . $this->getTableName() . '` 
                LEFT JOIN `' . $this->tableAttributeRanges . '` ON `' . $this->tableAttributeRanges . '`.`ID` = `' . $this->getTableName() . '`.`rangeID`
                LEFT JOIN `' . $this->tableAttributeTypes . '` AS AT ON `' . $this->getTableName() . '`.`type` = AT.`ID`
                WHERE `' . $this->getTableName() . '`.`ID` = :id ';

        if ($id === null) $id = $this->attrID;
        $binds[':id'] = $id;

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getRow(PDO::FETCH_ASSOC);
    }

    /**
     * @param $minPages
     * @param $step
     * @param null $maxPages
     * @return bool|int
     */
    public function createRange($minPages, $step, $maxPages = null)
    {
        $query = 'INSERT INTO `' . $this->tableAttributeRanges . '` 
            ( `minPages`, `step`, `maxPages` ) VALUES
            ( :minPages, :step, :maxPages )
                ';

        if (empty($maxPages)) $maxPages = null;

        $binds[':minPages'] = $minPages;
        $binds[':step'] = $step;
        $binds[':maxPages'] = $maxPages;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->lastInsertID();
    }

    /**
     * @param $id
     * @param $minPages
     * @param $step
     * @param null $maxPages
     * @return bool
     */
    public function updateRange($id, $minPages, $step, $maxPages = null)
    {
        $query = 'UPDATE `' . $this->tableAttributeRanges . '` 
            SET `minPages` = :minPages, `step` = :step, `maxPages` = :maxPages
            WHERE `ID` = :id
            ';

        if (empty($maxPages)) $maxPages = null;

        $binds[':id'] = $id;
        $binds[':minPages'] = $minPages;
        $binds[':step'] = $step;
        $binds[':maxPages'] = $maxPages;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @param $id
     * @return bool|array
     */
    public function getRange($id)
    {
        $query = 'SELECT * FROM `' . $this->tableAttributeRanges . '` WHERE `ID` = :id ';

        $binds[':id'] = $id;

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getRow(PDO::FETCH_ASSOC);
    }

    /**
     * @param $id
     * @return bool
     */
    public function deleteRange($id)
    {
        $query = 'DELETE FROM `' . $this->tableAttributeRanges . '` WHERE 
                  `ID` = :id ';

        $binds[':id'] = $id;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @param $attributes
     * @return bool
     */
    public function sort($attributes)
    {
        $result = true;
        foreach ($attributes as $index => $attrID) {
            if (empty($attrID))
                continue;

            $query = 'UPDATE `' . $this->getTableName() . '` SET `sort` = :index WHERE `ID` = :attrID ';

            $binds[':attrID'] = array($attrID, 'int');
            $binds[':index'] = $index;
            if (!$this->db->exec($query, $binds)) {
                $result = false;
            }
        }
        return $result;
    }

    /**
     * @param $id
     * @param int $active
     * @return bool
     */
    public function setActive($id, $active = 1)
    {
        $query = 'UPDATE `' . $this->getTableName() . '` 
            SET `active` = :active
            WHERE `ID` = :id
            ';

        $binds[':id'] = $id;
        $binds[':active'] = $active;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @return bool|array
     */
    public function getTypes()
    {
        $query = 'SELECT * FROM `' . $this->tableAttributeTypes . '` ';

        if (!$this->db->exec($query)) return false;

        return $this->db->getAll(PDO::FETCH_ASSOC);
    }

    /**
     * @param $id
     * @return bool|array
     */
    public function getType($id)
    {
        $query = 'SELECT * FROM `' . $this->tableAttributeTypes . '` WHERE `ID` = :id ';

        $binds[':id'] = $id;

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getRow(PDO::FETCH_ASSOC);
    }

    /**
     * @param $list
     * @return array|bool|mixed
     */
    public function customGetByList($list)
    {

        if (empty($list)) {
            return false;
        }

        $list = array_unique($list);

        $query = 'SELECT attributes.*, 
              GROUP_CONCAT( DISTINCT CONCAT_WS("::", attrLang.lang, attrLang.name) SEPARATOR "||" ) as langs 
              FROM `' . $this->getTableName() . '` as attributes
              LEFT JOIN `ps_config_attributeLangs` as  attrLang ON attributes.ID = attrLang.attributeID'
            . ' WHERE attributes.`ID` IN ( ' . implode(',', $list) . ' )
             GROUP BY attributes.ID ASC ';

        $binds = array();

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();

        if( !$res ) {
            return false;
        }

        $res = $this->LangFilter->splitArray($res, 'langs');

        $result = array();

        foreach ($res as $row) {
            $result[$row['ID']] = $row;
        }

        return $result;
    }


}
