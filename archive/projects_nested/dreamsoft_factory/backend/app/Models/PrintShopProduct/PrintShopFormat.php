<?php

namespace DreamSoft\Models\PrintShopProduct;

use DreamSoft\Models\Behaviours\LangFilter;
use DreamSoft\Models\PrintShop\PrintShop;

use PDO;

/**
 * Description of PrintShopFormat
 *
 * @author Rafał
 */
class PrintShopFormat extends PrintShop
{

    /**
     * @var string
     */
    protected $customFormat;
    /**
     * @var string
     */
    protected $printTypes;
    /**
     * @var string
     */
    protected $formatLangs;

    /**
     * @var LangFilter
     */
    protected $LangFilter;

    /**
     * PrintShopFormat constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('products_formats', $prefix);
        if ($prefix) {
            $this->customFormat = $this->prefix . 'products_customFormat';
            $this->printTypes = $this->prefix . 'products_printTypes';
            $this->formatLangs = $this->prefix . 'products_formatLangs';
        }
        $this->LangFilter = new LangFilter();
    }

    /**
     * @param null $active
     * @return array|bool|mixed
     */
    public function getAll($active = NULL)
    {
        if ($this->groupID === false) return false;
        if ($this->typeID === false) return false;

        $query = 'SELECT format.*,cFormat.minWidth, '
            . 'cFormat.minHeight, '
            . 'cFormat.minDepth, '
            . 'cFormat.maxWidth, '
            . 'cFormat.maxHeight,  '
            . 'cFormat.maxDepth, '
            . 'cFormat.widthStep, '
            . 'cFormat.heightStep, '
            . 'cFormat.depthStep, '
            . ' GROUP_CONCAT( DISTINCT CONCAT(printTypes.printTypeID,":",COALESCE(printTypes.minVolume,""),"-",COALESCE(printTypes.maxVolume,"")) ORDER BY printTypes.printTypeID SEPARATOR ";") as printTypesList, '
            .' GROUP_CONCAT( DISTINCT CONCAT_WS("::", formatlangs.lang, formatlangs.name) SEPARATOR "||" ) as langs '
            . 'FROM `ps_products_formats` as format
                LEFT JOIN `' . $this->customFormat . '` as cFormat '
            . ' ON cFormat.formatID = format.ID
                LEFT JOIN `' . $this->printTypes . '` as printTypes 
                ON printTypes.formatID = format.ID
                LEFT JOIN `' . $this->formatLangs . '` as formatlangs 
                ON formatlangs.formatID = format.ID
                WHERE `groupID` = :groupID AND `typeID` = :typeID ';

        if ($active != NULL) {
            $query .= ' AND format.active = :active ';
            $binds['active'] = $active;
        }

        $query .= '
                GROUP BY format.ID ORDER BY `order` 
                ';

        $binds[':groupID'] = $this->groupID;
        $binds[':typeID'] = $this->typeID;

        if (!$this->db->exec($query, $binds)) return false;

        $res = $this->db->getAll(PDO::FETCH_ASSOC);

        return $this->LangFilter->splitArray($res, 'langs');
    }

    /**
     * @param $formats
     * @return bool
     */
    public function sort($formats)
    {
        $result = true;
        foreach ($formats as $index => $formatID) {

            $query = 'UPDATE `ps_products_formats` SET `order` = :index WHERE `ID` = :formatID ';

            $binds[':formatID'] = array($formatID, 'int');
            $binds[':index'] = $index;
            if (!$this->db->exec($query, $binds)) {
                $result = false;
            }
        }
        return $result;
    }

    /**
     * @return bool|array
     */
    public function getActive()
    {
        if ($this->groupID === false) return false;
        if ($this->typeID === false) return false;

        $query = 'SELECT * FROM `ps_products_formats` 
                WHERE `groupID` = :groupID AND `typeID` = :typeID 
                AND `custom` = 0 AND `active` = 1
                ORDER BY `order` ';

        $binds[':groupID'] = $this->groupID;
        $binds[':typeID'] = $this->typeID;

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getAll(PDO::FETCH_ASSOC);
    }

    /**
     * @param $formats
     * @return bool|array
     */
    public function getByIDs($formats)
    {
        if (empty($formats)) {
            return false;
        }
        $query = 'SELECT ID, name FROM `ps_products_formats` 
                WHERE `ID` IN (' . implode(',', $formats) . ') AND `active` = 1 
                ORDER BY `order` ';

        $binds = array();

        if (!$this->db->exec($query, $binds)) return false;

        return $this->db->getAll(PDO::FETCH_ASSOC);
    }

    /**
     * @param $ID
     * @return bool|mixed
     */
    public function customGet($ID)
    {

        $query = 'SELECT `ps_products_formats`.*, 
                `' . $this->customFormat . '`.`minWidth`,
                `' . $this->customFormat . '`.`minHeight`,
                `' . $this->customFormat . '`.`maxWidth`,
                `' . $this->customFormat . '`.`maxHeight`,
                GROUP_CONCAT( DISTINCT CONCAT_WS("::", fl.lang, fl.name) SEPARATOR "||" ) as langs 
                FROM `ps_products_formats` 
                LEFT OUTER JOIN (`' . $this->customFormat . '`) 
                ON (`' . $this->customFormat . '`.`formatID` = `ps_products_formats`.`ID`)'
            .' LEFT JOIN `'.$this->formatLangs.'` fl ON fl.formatID = `ps_products_formats`.ID '
            . ' WHERE `ps_products_formats`.`ID` = :ID ';

        $binds[':ID'] = $ID;


        if (!$this->db->exec($query, $binds)) return false;

        $res =  $this->db->getRow(PDO::FETCH_ASSOC);

        return $this->LangFilter->splitOne($res, 'langs');
    }

    /**
     * @param $key
     * @param $ID
     * @param bool $multiple
     * @return mixed
     */
    public function parentGet($key, $ID, $multiple = false)
    {
        return parent::get($key, $ID, $multiple);
    }

    /**
     * @param $name
     * @param $adminName
     * @param $width
     * @param $height
     * @param $depth
     * @param $slope
     * @param $netWidth
     * @param $netHeight
     * @param $slopeExternalLeft
     * @param $slopeExternalRight
     * @param $slopeExternalTop
     * @param $slopeExternalBottom
     * @param $slopeExternalFront
     * @param $slopeExternalBack
     * @param $addRidgeThickness
     * @param $wingtipFront
     * @param $wingtipFrontMin
     * @param $wingtipBack
     * @param $wingtipBackMin
     * @param $maximumTotalGrossWidth
     * @param $binding
     * @param int $interchangeability
     * @param int $custom
     * @return bool|string
     */
    public function createByParams(
                                   $name, $adminName, $width, $height,$depth, $slope, $netWidth,
                                   $netHeight, $slopeExternalLeft, $slopeExternalRight, $slopeExternalTop,
                                   $slopeExternalBottom, $slopeExternalFront, $slopeExternalBack,
                                   $addRidgeThickness, $wingtipFront, $wingtipFrontMin, $wingtipBack,
                                   $wingtipBackMin, $maximumTotalGrossWidth, $binding, $interchangeability, $custom
    )
    {
        if ($this->groupID === false) return false;
        if ($this->typeID === false) return false;

        if (empty($width)) $width = null;
        if (empty($height)) $height = null;

        $params['groupID'] = $this->groupID;
        $params['typeID'] = $this->typeID;
        $params['name'] = $name;
        $params['adminName'] = $adminName;
        $params['width'] = $width;
        $params['height'] = $height;
        $params['depth'] = $depth;
        $params['custom'] = $custom;
        $params['slope'] = $slope;
        $params['netWidth'] = $netWidth;
        $params['netHeight'] = $netHeight;
        $params['slopeExternalLeft'] = $slopeExternalLeft;
        $params['slopeExternalRight'] = $slopeExternalRight;
        $params['slopeExternalTop'] = $slopeExternalTop;
        $params['slopeExternalBottom'] = $slopeExternalBottom;
        $params['slopeExternalFront'] = $slopeExternalFront;
        $params['slopeExternalBack'] = $slopeExternalBack;
        $params['addRidgeThickness'] = $addRidgeThickness;
        $params['wingtipFront'] = $wingtipFront;
        $params['wingtipFrontMin'] = $wingtipFrontMin;
        $params['wingtipBack'] = $wingtipBack;
        $params['wingtipBackMin'] = $wingtipBackMin;
        $params['maximumTotalGrossWidth'] = $maximumTotalGrossWidth;
        $params['binding'] = $binding;
        $params['interchangeability'] = $interchangeability;
        $params['order'] = ($this->getMaxID() + 1);

        return $this->create($params);
    }

    /**
     * @param $params
     * @return bool|string
     */
    public function parentCreate($params)
    {
        return parent::create($params);
    }

    /**
     * @param $groupID
     * @param $typeID
     * @return bool
     */
    public function deleteByGroupType($groupID, $typeID)
    {
        $query = 'DELETE FROM `ps_products_formats` 
                WHERE `groupID` = :groupID AND `typeID` = :typeID
                ';

        $binds[':groupID'] = $groupID;
        $binds[':typeID'] = $typeID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    /**
     * @return bool
     */
    public function getMaxID()
    {
        $query = 'SELECT MAX(`ps_products_formats`.ID) FROM `ps_products_formats` LIMIT 1';

        if (!$this->db->exec($query)) return false;

        return $this->db->getOne();
    }


    /**
     * @param $formatID
     * @param $minWidth
     * @param $minHeight
     * @param $maxWidth
     * @param $maxHeight
     * @return bool
     */
    public function createCustom($formatID, $minWidth, $minHeight, $minDepth, $maxWidth, $maxHeight, $maxDepth    )
    {

        $query = 'INSERT INTO `ps_products_customFormat` 
            ( `formatID`, `minWidth`, `minHeight`, `minDepth`, `maxWidth`, `maxHeight`, `maxDepth` ) VALUES
            ( :formatID, :minWidth, :minHeight, :minDepth, :maxWidth, :maxHeight, :maxDepth )';

        $binds[':formatID'] = $formatID;
        $binds[':minWidth'] = $minWidth;
        $binds[':minHeight'] = $minHeight;
        $binds[':minDepth'] = $minDepth;
        $binds[':maxWidth'] = $maxWidth;
        $binds[':maxHeight'] = $maxHeight;
        $binds[':maxDepth'] = $maxDepth;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->lastInsertID();
    }

    /**
     * @param $id
     * @param $name
     * @param $value
     * @return bool
     */
    public function update($id, $name, $value)
    {
        $query = 'UPDATE `ps_products_formats` 
            SET `' . $name . '` = :value
            WHERE ID = :id';

        $binds[':value'] = $value;
        $binds[':id'] = $id;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    /**
     * @param $id
     * @param $name
     * @param $value
     * @return bool
     */
    public function updateCustom($id, $name, $value)
    {
        $query = 'UPDATE `' . $this->customFormat . '` 
            SET `' . $name . '` = :value
            WHERE formatID = :id';

        if (empty($value)) {
            $value = null;
        }
        $binds[':value'] = $value;
        $binds[':id'] = $id;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    /**
     * @param $ID
     * @return bool
     */
    public function customDelete($ID)
    {
        $format = $this->get('ID', $ID);
        if ($format['custom'] == 1) {
            $this->deleteCustom($format['customID']);
        }
        $this->deleteVolume($ID);

        $query = 'DELETE FROM `ps_products_formats` WHERE 
                  `ID` = :ID ';

        $binds[':ID'] = $ID;
        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    /**
     * @param $ID
     * @return bool
     */
    public function deleteCustom($ID)
    {
        $query = 'DELETE FROM `' . $this->customFormat . '` WHERE 
                  `ID` = :ID ';

        $binds[':ID'] = $ID;
        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @param $formatID
     * @param $printTypeID
     * @param null $minVolume
     * @param null $maxVolume
     * @return bool|string
     */
    public function createPrintType($formatID, $printTypeID, $minVolume = NULL, $maxVolume = NULL)
    {

        $query = 'INSERT INTO `ps_products_printTypes` 
            ( `formatID`, `printTypeID`, `minVolume`, `maxVolume` ) VALUES
            ( :formatID, :printTypeID, :minVolume, :maxVolume )';

        $binds['formatID'] = $formatID;
        $binds['printTypeID'] = $printTypeID;
        $binds['minVolume'] = $minVolume;
        $binds['maxVolume'] = $maxVolume;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->lastInsertID();
    }

    /**
     * @param $formatID
     * @param $name
     * @param $value
     * @return bool
     */
    public function updatePrintType($formatID, $name, $value)
    {
        $query = 'UPDATE `' . $this->printTypes . '` 
            SET `' . $name . '` = :value
            WHERE formatID = :ID';

        if (empty($value)) {
            $value = null;
        }
        $binds[':value'] = $value;
        $binds[':ID'] = $formatID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }

    /**
     * @param $formatID
     * @return bool
     */
    public function deletePrintTypes($formatID)
    {
        $query = 'DELETE FROM `' . $this->printTypes . '` WHERE 
                  `formatID` = :formatID ';

        $binds[':formatID'] = $formatID;
        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return true;
    }

    /**
     * @param $formatID
     */
    public function deleteVolume($formatID)
    {

    }

    /**
     * @param $ID
     * @return mixed
     */
    public function getOne($ID)
    {
        $query = 'SELECT f.*,
        GROUP_CONCAT( DISTINCT CONCAT_WS("::", fl.lang, fl.name) SEPARATOR "||" ) as langs 
        FROM `ps_products_formats` f
        LEFT JOIN `'.$this->formatLangs.'` fl ON fl.formatID = f.ID
        WHERE `ID` = :ID ';

        $binds['ID'] = $ID;

        $this->db->exec($query, $binds);

        $res = $this->db->getRow();

        return $this->LangFilter->splitOne($res, 'langs');

    }
}

