<?php

namespace DreamSoft\Models\PrintShopUser;
/**
 * Description of UserCalcProductAttribute
 *
 */

use DreamSoft\Core\Model;
use DreamSoft\Models\Behaviours\LangFilter;
use DreamSoft\Models\Behaviours\UrlMaker;

class UserCalcProductFile extends Model
{
    /**
     * @var UrlMaker
     */
    private $UrlMaker;
    /**
     * @var LangFilter
     */
    protected $LangFilter;

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('ps_user_calc_product_files', false);
        $this->UrlMaker = new UrlMaker();
        $this->LangFilter = new LangFilter();
    }

    public function add($params)
    {

        if (empty($params)) {
            return false;
        }

        foreach ($params as $key => $value) {
            if ($key === 'name') {
                $params[$key] = $this->UrlMaker->permalink($value);
            }
        }
        return $this->create($params);
    }

    public function getByProduct($dpProductID)
    {
        $this->db->exec('select ucpa.attrPages as filesNumber from dp_products p
                  join ps_user_calc_products cp on cp.calcID=p.calcID
                  join ps_user_calc_product_attributes ucpa on ucpa.calcProductID=cp.ID
                  join ps_config_attributes ca on ca.ID=ucpa.attrID
                    where  p.ID=:dpProductID and ca.name="patterns_number"', ['dpProductID' => $dpProductID]);
        $requiredFilesNumber = $this->db->getOne();
        $this->db->exec('select ucpa.ID cpAttrID,ca.*, cp.ID calcProductID, co.doubleSidedSheet, 
       GROUP_CONCAT( DISTINCT CONCAT_WS("::", attrLang.lang, attrLang.name) SEPARATOR "||" ) as langs,
       GROUP_CONCAT( DISTINCT CONCAT_WS("::", optLang.lang, optLang.name) SEPARATOR "||" ) as optLangs,
       GROUP_CONCAT( DISTINCT CONCAT_WS("::", ptl.lang, ptl.name) SEPARATOR "||" ) as typeLangs
        from dp_products p
        join ps_user_calc_products cp on cp.calcID=p.calcID
        join ps_user_calc_product_attributes ucpa on ucpa.calcProductID=cp.ID
        join ps_config_attributes ca on ca.ID=ucpa.attrID
        join ps_config_options co on co.ID=ucpa.optID
        join ps_products_types pt on pt.ID=cp.typeID
        join ps_config_attributeLangs as attrLang on ca.ID = attrLang.attributeID
        join ps_config_optionLangs as optLang ON co.ID = optLang.optionID
        join ps_products_typeLangs ptl on ptl.typeID=pt.ID
        where  p.ID=:dpProductID  and ucpa.fileUploadAvailable=1
        group by ucpa.ID ORDER BY `ca`.`sort`;', ['dpProductID' => $dpProductID]);
        $productAttrs = $this->db->getAll();
        $calcProductIDs = array_column($productAttrs, 'calcProductID');
        $cpAttrIDs = array_column($productAttrs, 'cpAttrID');
        
        $this->db->exec('SELECT 
                pf.*, 
                pa.attrID, 
                pa.optID, 
                mie.`type`,
                pa.calcProductID,
                pa.ID AS userCalcProductAttrOptionID
            FROM ps_user_calc_product_attributes pa
            JOIN ps_user_calc_product_files pf ON pf.userCalcProductAttrOptionID = pa.ID
            JOIN dp_modelsIconsExtensions mie ON mie.ID = pf.modelExtensionID
            WHERE pa.calcProductID IN (' . implode(',', $calcProductIDs) . ') 
              AND pa.ID IN (' . implode(',', $cpAttrIDs) . ')
            ORDER BY pf.ID, pf.backSideTarget ASC');
        $allFiles = $this->db->getAll();
        
        foreach ($productAttrs as &$attr) {
            $attr['files'] = array_filter($allFiles, function($file) use ($attr) {
                return $file['calcProductID'] == $attr['calcProductID'] && $file['userCalcProductAttrOptionID'] == $attr['cpAttrID'];
            });
        
            $filesCount = $attr['doubleSidedSheet'] && count($attr['files']) == 1 ? 2 : 1;
            if (count($attr['files']) == 1 && $attr['files'][0]['type'] == 'pdf') {
                $filesCount = 1;
            }
            if ($requiredFilesNumber) {
                $filesCount *= $requiredFilesNumber;
            }
            if (count($attr['files']) < $filesCount) {
                $limit = $filesCount - count($attr['files']);
                for ($i = 0; $i < $limit; $i++) {
                    $attr['files'][] = [];
                }
            }
        }
        
        $productAttrs = $this->LangFilter->splitArray($productAttrs, 'optLangs');
        $productAttrs = $this->LangFilter->splitArray($productAttrs, 'langs');
        $productAttrs = $this->LangFilter->splitArray($productAttrs, 'typeLangs');
        return $productAttrs;
    }

    public function getOptionFiles($calcProductID, $userCalcProductAttrOptionID){
        $this->db->exec('select pf.*
                from ps_user_calc_product_attributes pa
                join ps_user_calc_product_files pf on pf.userCalcProductAttrOptionID=pa.ID
                join dp_modelsIconsExtensions mie on mie.ID=pf.modelExtensionID
                where calcProductID=:calcProductID and userCalcProductAttrOptionID=:userCalcProductAttrOptionID',
            ['calcProductID' => $calcProductID, 'userCalcProductAttrOptionID' => $userCalcProductAttrOptionID]);
    return $this->db->getAll();
    }
    public function getFlatFiles($calcID){
        $this->db->exec('select dp_products.ID 
            from dp_products
            where calcID=:calcID',['calcID'=>$calcID]);
        $productAttrs=$this->getByProduct($this->db->getOne());
        $files=[];
        foreach ($productAttrs as $pa){
            foreach ($pa['files'] as $file){
                if(!empty($file)){
                    $files[]=$file;
                }
            }
        }
        return $files;
    }

    public function getByUserCalcProducts($userCalcProductID)
    {
        $this->db->exec('select p.ID 
            from dp_products p
            join ps_user_calc_products ucp on ucp.calcID=p.calcID
            where ucp.ID=:ID', ['ID' => $userCalcProductID]);
        return $this->getByProduct($this->db->getOne());
    }
    public function setAccepted($ID, $userID, $userName)
    {
        $query = 'update '.$this->getTableName().' set accept=1, 
                                   acceptChangeDate=CURRENT_TIMESTAMP(),
                                   acceptRejectUserID=:acceptRejectUserID,
                                   acceptRejectUserName=:acceptRejectUserName
                    where ID=:ID';
        if ($this->db->exec($query, ['ID' => $ID,
            'acceptRejectUserID' => $userID,
            'acceptRejectUserName' => $userName])) {
            return true;
        }
        return false;
    }

    public function getByOrderList($orders)
    {
        $this->db->exec('select ID, orderID from dp_products where orderID in(' . implode(',', $orders) . ')');
        $dpProducts = $this->db->getAll();
        $return = [];
        foreach ($dpProducts as $dpProduct) {
            $return[$dpProduct['ID']] = $this->getByProduct($dpProduct['ID']);
        }
        return $return;
    }
}
