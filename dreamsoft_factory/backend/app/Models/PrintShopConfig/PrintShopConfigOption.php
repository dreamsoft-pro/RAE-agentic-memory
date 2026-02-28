<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Models\Behaviours\LangFilter;
use DreamSoft\Models\PrintShop\PrintShop;
use DreamSoft\Models\PrintShopProduct\PrintShopGroupLanguage;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeLanguage;
use DreamSoft\Models\Product\CategoryLang;
use DreamSoft\Models\Upload\UploadFile;
use PDO;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionDescription;
use DreamSoft\Libs\DataUtils;
/**
 * Class PrintShopConfigOption
 *
 * @package DreamSoft\Models\PrintShopConfig
 */
class PrintShopConfigOption extends PrintShop
{
    private $tableProductsOption;
    private $tableOptionRealizationTime;
    protected $tableOptionTooltipLangs;
    private $tableOptionLangs;

    /**
     * @var LangFilter
     */
    protected $LangFilter;

    /**
     * @var PrintShopConfigOptionDescription
     */
    private $PrintShopConfigOptionDescription;

    /**
     * @var PrintShopGroupLanguage
     */
    private $PrintShopGroupLanguage;

    /**
     * @var CategoryLang
     */
    private $CategoryLang;

    /**
     * @var UploadFile
     */
    private $UploadFile;

    /**
     * @var string
     */
    private $iconFolder;

    /**
     * PrintShopConfigOption constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('config_options', $prefix);
        if ($prefix) {
            $this->tableProductsOption = $this->prefix . 'products_options';
            $this->tableOptionRealizationTime = $this->prefix . 'config_optionRealizationTime';
            $this->tableOptionLangs = $this->prefix . 'config_optionLangs';
            $this->tableOptionTooltipLangs = $this->prefix . 'config_option_tooltip_lang';
        }
        $this->LangFilter = new LangFilter();
        $this->PrintShopConfigOptionDescription = PrintShopConfigOptionDescription::getInstance();
        $this->PrintShopGroupLanguage = PrintShopGroupLanguage::getInstance();

        $this->CategoryLang = CategoryLang::getInstance();
        $this->UploadFile = UploadFile::getInstance();
        $this->iconFolder = 'uploadedFiles/' . companyID . '/icons/';
    }

    public function customCreate($name, $adminName, $oneSide = null): bool|string
    {
        if (empty($this->attrID)) {
            return false;
        }

        $query = 'SELECT max(`sort`)+1 FROM `' . $this->getTableName() . '` WHERE `attrID` = :attrID ';
        $binds[':attrID'] = $this->attrID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $sort = $this->db->getOne();
        $sort = $sort ?: 1;
        $binds = [];
        $query = 'SELECT MAX(ID) FROM `' . $this->getTableName() . '` LIMIT 1';
        if ($this->db->exec($query)) {
            $tmpLast = $this->db->getOne() + 1;
        }

        $query = 'INSERT INTO `' . $this->getTableName() . '` 
                  (`ID`, `attrID`, `name`, `adminName`, `sort`, `oneSide`) VALUES
                  (:tmpLast, :attrID, :name, :adminName, :sort, :oneSide)';
        $binds = [
            ':tmpLast' => $tmpLast,
            ':attrID' => $this->attrID,
            ':name' => $name,
            ':adminName' => $adminName,
            ':sort' => $sort,
            ':oneSide' => $oneSide
        ];

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->lastInsertID();
    }

    public function getAll(): array|bool
    {
        $query = 'SELECT `' . $this->getTableName() . '`.*, `' . $this->tableOptionLangs . '`.`lang` as lLang,
                    `' . $this->tableOptionTooltipLangs . '`.`lang` as tLang, 
                    `' . $this->tableOptionLangs . '`.`name` as lName,
                    `' . $this->tableOptionTooltipLangs . '`.`tooltip` as lTooltip
                    FROM `' . $this->getTableName() . '` 
                    LEFT JOIN `' . $this->tableOptionTooltipLangs . '` ON `' . $this->tableOptionTooltipLangs . '`.`optionID` = `' . $this->getTableName() . '`.`ID` 
                    LEFT JOIN `' . $this->tableOptionLangs . '` ON `' . $this->tableOptionLangs . '`.`optionID` = `' . $this->getTableName() . '`.`ID` 
                  ';
        $binds = [];

        if (!empty($this->attrID)) {
            $query .= ' WHERE `attrID` = :attrID  ';
            $binds[':attrID'] = $this->attrID;
        }

        $query .= ' ORDER BY `' . $this->getTableName() . '`.`sort` ';

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll(PDO::FETCH_ASSOC);

        $result=DataUtils::includeLanguageTables($res,[['lLang','lName','names'],['tLang','lTooltip','tooltip']]);

        return array_values($result);
    }

    public function customGet($id): array|bool
    {
        $query = 'SELECT `' . $this->getTableName() . '`.*, 
                         `' . $this->tableOptionLangs . '`.`lang` as lLang, 
                         `' . $this->tableOptionLangs . '`.`name` as lName
                  FROM `' . $this->getTableName() . '`
                  LEFT JOIN `' . $this->tableOptionLangs . '` ON `' . $this->tableOptionLangs . '`.`optionID` = `' . $this->getTableName() . '`.`ID`
                  WHERE `' . $this->getTableName() . '`.`ID` = :ID ';
        $binds[':ID'] = $id;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll(PDO::FETCH_ASSOC);
        $result = [];

        foreach ($res as $r) {
            $lLang = $lName = null;
            if (!empty($r['lLang'])) {
                $lLang = $r['lLang'];
                $lName = $r['lName'];
            }
            unset($r['lLang'], $r['lName']);
            $result = array_merge($result, $r);
            if (!empty($lLang)) {
                $result['names'][$lLang] = $lName;
            }
        }

        return $result;
    }

    public function sort($options): bool
    {
        $result = true;

        foreach ($options as $index => $optID) {
            if (empty($optID)) {
                continue;
            }

            $query = 'UPDATE `' . $this->getTableName() . '` SET `sort` = :index WHERE `ID` = :optID ';
            $binds[':optID'] = $optID;
            $binds[':index'] = $index;

            if (!$this->db->exec($query, $binds)) {
                $result = false;
            }
        }

        return $result;
    }

    public function setActive($id, $active = 1): bool
    {
        $query = 'UPDATE `' . $this->getTableName() . '` 
                  SET `active` = :active
                  WHERE `ID` = :id ';
        $binds = [
            ':id' => $id,
            ':active' => $active
        ];

        return $this->db->exec($query, $binds) ? true : false;
    }

    public function getRealizationTime($ID): array|bool
    {
        $query = 'SELECT * FROM `' . $this->tableOptionRealizationTime . '` WHERE `ID` = :ID ';
        $binds[':ID'] = $ID;

        return $this->db->exec($query, $binds) ? $this->db->getAll(PDO::FETCH_ASSOC) : false;
    }

    public function getRealizationTimes($optionID = null): array|bool
    {
        $optionID = $optionID ?? $this->optID;

        $query = 'SELECT * FROM `' . $this->tableOptionRealizationTime . '` WHERE `optionID` = :optionID ';
        $binds[':optionID'] = $optionID;

        return $this->db->exec($query, $binds) ? $this->db->getAll(PDO::FETCH_ASSOC) : false;
    }

    public function updateRealizationTime($ID, $key, $value): bool|string
    {
        $query = 'UPDATE `' . $this->tableOptionRealizationTime . '` 
                  SET `' . $key . '` = :' . $key . '
                  WHERE `ID` = :ID ';
        $binds = [
            ':ID' => $ID,
            ':' . $key => $value
        ];

        return $this->db->exec($query, $binds) ? $this->db->lastInsertID() : false;
    }

    public function createRealizationTime($optionID, $volume, $days): bool|string
    {
        $query = 'INSERT INTO `' . $this->tableOptionRealizationTime . '` 
                  (`optionID`, `volume`, `days`) 
                  VALUES (:optionID, :volume, :days)';
        $binds = [
            ':optionID' => $optionID,
            ':volume' => $volume,
            ':days' => $days
        ];

        return $this->db->exec($query, $binds) ? $this->db->lastInsertID() : false;
    }

    public function customGetByList($list): array|bool
    {
        if (empty($list)) {
            return false;
        }

        $list = array_unique($list);

        $query = 'SELECT `options`.*, 
                         GROUP_CONCAT(DISTINCT CONCAT_WS("::", optLang.lang, optLang.name) SEPARATOR "||") as langs 
                  FROM `' . $this->getTableName() . '` as options
                  LEFT JOIN `ps_config_optionLangs` as optLang ON `options`.ID = optLang.optionID 
                  WHERE `options`.`ID` IN (' . implode(',', $list) . ') 
                  GROUP BY `options`.ID ASC';

        if (!$this->db->exec($query)) {
            return false;
        }

        $res = $this->db->getAll();
        $res = $this->LangFilter->splitArray($res, 'langs');

        $result = [];

        foreach ($res as $row) {
            $result[$row['ID']] = $row;
        }

        return $result;
    }

    public function getPrintRotated($printTypeID): bool|string
    {
        $query = 'SELECT printRotated FROM ps_config_options WHERE `ID` = :controllerID ';
        $binds[':controllerID'] = $printTypeID;

        return $this->db->exec($query, $binds) ? $this->db->getOne() : false;
    }

    public function getAllActiveWithDescriptions(): array|bool
    {
        $query = 'SELECT `' . $this->getTableName() . '`.*, 
                         `' . $this->tableOptionLangs . '`.`lang` as lLang, 
                         `' . $this->tableOptionLangs . '`.`name` as lName
                  FROM `' . $this->getTableName() . '` 
                  LEFT JOIN `' . $this->tableOptionLangs . '` ON `' . $this->tableOptionLangs . '`.`optionID` = `' . $this->getTableName() . '`.`ID` 
                  WHERE active=1 AND `attrID` = :attrID  
                  ORDER BY `' . $this->getTableName() . '`.`sort` ';
        $binds[':attrID'] = $this->attrID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $optionsRes = $this->db->getAll(PDO::FETCH_ASSOC);
        $options = [];

        foreach ($optionsRes as $r) {
            $lLang = $lName = null;
            if (!empty($r['lLang'])) {
                $lLang = $r['lLang'];
                $lName = $r['lName'];
            }
            unset($r['lLang'], $r['lName']);
            $key = $r['ID'];
            if (!isset($options[$key])) {
                $options[$key] = [];
            }
            $options[$key] = array_merge($options[$key], $r);
            if (!empty($lLang)) {
                if (!isset($options[$key]['names'])) {
                    $options[$key]['names'] = [];
                }
                $options[$key]['names'][$lLang] = $lName;
            }
        }

        $options = array_values($options);
        $this->PrintShopConfigOptionDescription->setAttrID($this->attrID);

        foreach ($options as &$row) {
            $this->PrintShopConfigOptionDescription->setOptID($row['ID']);
            $descriptions = $this->PrintShopConfigOptionDescription->customGetAll('paper', $this->domainID);
            $row['descriptions'] = [];
            array_map(function ($description) use (&$row) {
                $row['descriptions'][$description['name']] = $description['value'];
            }, $descriptions);
            $row['descriptions']['weight'] = $row['weight'];
        }

        return $options;
    }

    public function getOption($optID): array|bool
    {
        $query = 'SELECT `' . $this->getTableName() . '`.*, 
                         `' . $this->tableOptionLangs . '`.`lang` as lLang, 
                         `' . $this->tableOptionLangs . '`.`name` as lName
                  FROM `' . $this->getTableName() . '` 
                  LEFT JOIN `' . $this->tableOptionLangs . '` ON `' . $this->tableOptionLangs . '`.`optionID` = `' . $this->getTableName() . '`.`ID` 
                  WHERE `' . $this->getTableName() . '`.`ID` = :optID';
        $binds[':optID'] = $optID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $optionsRes = $this->db->getAll(PDO::FETCH_ASSOC);
        $options = [];

        foreach ($optionsRes as $r) {
            $lLang = $lName = null;
            if (!empty($r['lLang'])) {
                $lLang = $r['lLang'];
                $lName = $r['lName'];
            }
            unset($r['lLang'], $r['lName']);
            $key = $r['ID'];
            if (!isset($options[$key])) {
                $options[$key] = [];
            }
            $options[$key] = array_merge($options[$key], $r);
            if (!empty($lLang)) {
                if (!isset($options[$key]['names'])) {
                    $options[$key]['names'] = [];
                }
                $options[$key]['names'][$lLang] = $lName;
            }
        }

        $options = array_values($options);
        $this->PrintShopConfigOptionDescription->setAttrID($this->attrID);

        foreach ($options as &$row) {
            $this->PrintShopConfigOptionDescription->setOptID($row['ID']);
            $descriptions = $this->PrintShopConfigOptionDescription->customGetAll('paper', $this->domainID);
            $row['descriptions'] = [];
            array_map(function ($description) use (&$row) {
                $row['descriptions'][$description['name']] = $description['value'];
            }, $descriptions);
            $row['descriptions']['weight'] = $row['weight'];
        }

        return $options;
    }

    public function getProductsUsingOptions(): array
    {
        $query = 'SELECT t.ID typeID, t.groupID, t.iconID, o.optID, pc.categoryID, l.* 
                  FROM ps_products_types t
                  JOIN ps_products_typeLangs l ON l.typeID=t.ID
                  JOIN ps_products_options o ON o.typeID=t.ID
                  JOIN dp_productCategories pc ON pc.itemID=t.ID
                  WHERE o.attrID=:attrID;';
        $this->db->exec($query, ['attrID' => $this->attrID]);
        $all = $this->db->getAll();
        $result = [];

        foreach ($all as $item) {
            if (!isset($result[$item['typeID']])) {
                $result[$item['typeID']] = [
                    'typeID' => $item['typeID'], 
                    'iconID' => $item['iconID'], 
                    'names' => [], 
                    'options' => []
                ];
            }
            $result[$item['typeID']]['names'][$item['lang']] = $item['name'];
            $result[$item['typeID']]['typeurl'][$item['lang']] = $item['slug'];
            $result[$item['typeID']]['options'][] = $item['optID'];
        }

        foreach ($result as $key => $val) {
            foreach ($this->PrintShopGroupLanguage->get('groupID', $val['groupID'], true) as $gl) {
                $result[$key]['groupurl'][$gl['lang']] = $gl['slug'];
            }
            foreach ($this->CategoryLang->get('categoryID', $val['categoryID'], true) as $tl) {
                $result[$key]['categoryurl'][$tl['lang']] = $tl['slug'];
            }
            if ($result[$key]['iconID']) {
                $icon = $this->UploadFile->get('ID', $result[$key]['iconID']);
                $minFolder = current(explode('/', $icon['path']));
                $result[$key]['iconUrl'] = STATIC_URL . $this->iconFolder . $minFolder . '/' . $icon['name'];
            } else {
                $result[$key]['iconUrl'] = STATIC_URL . companyID . '/' . 'images' . '/' . THUMB_IMAGE_DEFAULT;
            }
        }

        return array_values($result);
    }

    public function getTypeWithUsingOptions($typeID): array
    {
        $query = 'SELECT t.ID typeID, t.groupID, t.iconID, o.optID, l.* 
                  FROM ps_products_types t
                  JOIN ps_products_typeLangs l ON l.typeID=t.ID
                  JOIN ps_products_options o ON o.typeID=t.ID
                  WHERE o.attrID=:attrID AND t.ID = :typeID;';
        $this->db->exec($query, ['attrID' => $this->attrID, 'typeID' => $typeID]);
        $all = $this->db->getAll();
        $result = [];

        foreach ($all as $item) {
            if (!isset($result[$item['typeID']])) {
                $result[$item['typeID']] = [
                    'typeID' => $item['typeID'], 
                    'iconID' => $item['iconID'], 
                    'names' => [], 
                    'options' => []
                ];
            }
            $result[$item['typeID']]['names'][$item['lang']] = $item['name'];
            $result[$item['typeID']]['typeurl'][$item['lang']] = $item['slug'];
            $result[$item['typeID']]['options'][] = $item['optID'];
        }

        return $result;
    }

    public function getComplexProductForDisplay($typeID): array
    {
        $query = 'SELECT t.ID typeID, t.groupID, t.iconID, pc.categoryID, l.* 
                  FROM ps_products_types t
                  JOIN ps_products_typeLangs l ON l.typeID=t.ID
                  JOIN dp_productCategories pc ON pc.itemID=t.ID
                  WHERE t.ID = :typeID;';
        $this->db->exec($query, ['typeID' => $typeID]);
        $all = $this->db->getAll();
        $result = [];

        foreach ($all as $item) {
            if (!isset($result[$item['typeID']])) {
                $result[$item['typeID']] = [
                    'typeID' => $item['typeID'], 
                    'iconID' => $item['iconID'], 
                    'names' => []
                ];
            }
            $result[$item['typeID']]['names'][$item['lang']] = $item['name'];
            $result[$item['typeID']]['typeurl'][$item['lang']] = $item['slug'];
        }

        foreach ($result as $key => $val) {
            foreach ($this->PrintShopGroupLanguage->get('groupID', $val['groupID'], true) as $gl) {
                $result[$key]['groupurl'][$gl['lang']] = $gl['slug'];
            }
            foreach ($this->CategoryLang->get('categoryID', $val['categoryID'], true) as $tl) {
                $result[$key]['categoryurl'][$tl['lang']] = $tl['slug'];
            }
            if ($result[$key]['iconID']) {
                $icon = $this->UploadFile->get('ID', $result[$key]['iconID']);
                $minFolder = current(explode('/', $icon['path']));
                $result[$key]['iconUrl'] = STATIC_URL . $this->iconFolder . $minFolder . '/' . $icon['name'];
            } else {
                $result[$key]['iconUrl'] = STATIC_URL . companyID . '/' . 'images' . '/' . THUMB_IMAGE_DEFAULT;
            }
        }

        return array_values($result);
    }
}
