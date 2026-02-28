<?php

use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigExclusion;

class ExclusionsController extends Controller
{
    protected $PrintShopConfigExclusion;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopConfigExclusion = PrintShopConfigExclusion::getInstance();
    }

    public function exclusions($attrID, $optionID)
    {
        $this->PrintShopConfigExclusion->setAttrID($attrID);
        $this->PrintShopConfigExclusion->setOptID($optionID);

        $results = $this->PrintShopConfigExclusion->getAll();
        $res = [];

        foreach ($results as $result) {
            $res[$result['excAttrID']][$result['excOptID']] = 1;
        }

        return $res ?: [];
    }

    public function productExclusions($groupID, $typeID)
    {
        return $this->PrintShopConfigExclusion->getForProduct($groupID, $typeID) ?: [];
    }

    public function patch_exclusions($attrID, $optionID)
    {
        $this->PrintShopConfigExclusion->setAttrID($attrID);
        $this->PrintShopConfigExclusion->setOptID($optionID);

        $exclusions = $this->Data->getAllPost();
        $resultOfSave = $this->PrintShopConfigExclusion->customDelete();

        foreach ($exclusions as $exclusion) {
            if (is_numeric($exclusion['excAttrID']) && is_numeric($exclusion['excOptID'])) {
                $resultOfSave = $this->PrintShopConfigExclusion->customCreate($exclusion['excAttrID'], $exclusion['excOptID']);
            }
        }

        return ['response' => $resultOfSave];
    }
}
