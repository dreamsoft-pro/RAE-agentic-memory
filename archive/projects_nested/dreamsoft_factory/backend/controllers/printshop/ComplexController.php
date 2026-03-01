<?php

use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShop\PrintShopComplex;
use DreamSoft\Models\PrintShop\PrintShopComplexGroup;
use DreamSoft\Models\PrintShop\PrintShopComplexRelatedFormat;

class ComplexController extends Controller
{
    public $useModels = array();

    protected $PrintShopComplex;
    protected $PrintShopComplexGroup;
    protected $PrintShopComplexRelatedFormat;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopComplex = PrintShopComplex::getInstance();
        $this->PrintShopComplexGroup = PrintShopComplexGroup::getInstance();
        $this->PrintShopComplexRelatedFormat = PrintShopComplexRelatedFormat::getInstance();
    }

    public function complex($groupID, $typeID, $ID = NULL)
    {
        $this->PrintShopComplex->setTypeID($typeID);

        $data = intval($ID) > 0 ? $this->PrintShopComplex->customGet($ID) : $this->PrintShopComplex->getAll();
        return $data ?: array();
    }

    public function complexPublic($groupID, $typeID, $ID = NULL)
    {
        return $this->complex($groupID, $typeID, $ID);
    }

    public function post_complex($groupID, $typeID)
    {
        $baseID = $typeID;
        $typeID = $this->Data->getPost('typeID');
        $complexGroupID = $this->Data->getPost('complexGroupID');

        if ($typeID) {
            $lastID = $this->PrintShopComplex->create(compact('baseID', 'typeID', 'complexGroupID'));
            $return = $this->PrintShopComplex->customGet($lastID);
            if (!$return) {
                return ['response' => false];
            }
            return $return;
        } else {
            return $this->sendFailResponse('01');
        }
    }

    public function delete_complex($groupID, $typeID, $ID)
    {
        $complex = $this->PrintShopComplex->customGet($ID);
        if (intval($ID) > 0) {
            if (!$this->PrintShopComplex->delete('ID', $ID)) {
                return $this->sendFailResponse('09');
            }

            if ($complex['complexGroupID'] != null && !$this->PrintShopComplex->usedGroup($complex['complexGroupID'])) {
                $this->PrintShopComplexGroup->delete('ID', $complex['complexGroupID']);
            }
            return ['response' => true];
        } else {
            return ['response' => false];
        }
    }

    public function post_group($groupID, $typeID, $complexID)
    {
        $name = $this->Data->getPost('name');
        $complexGroupID = $this->PrintShopComplexGroup->create(compact('name'));
        if ($complexGroupID && $this->PrintShopComplex->update($complexID, 'complexGroupID', $complexGroupID)) {
            return ['response' => true, 'complexGroupID' => $complexGroupID];
        }
        return ['response' => false];
    }

    public function put_group($groupID, $typeID)
    {
        $name = $this->Data->getPost('name');
        $ID = $this->Data->getPost('ID');
        if ($this->PrintShopComplexGroup->update($ID, 'name', $name)) {
            return ['response' => true];
        }
        return ['response' => false];
    }

    public function relatedFormat($groupID, $params, $typeID, $baseFormatID)
    {
        $complexID = $params['complexID'];
        $data = intval($baseFormatID) > 0 ? $this->PrintShopComplexRelatedFormat->getByBaseFormatID($baseFormatID, $complexID) : $this->PrintShopComplexRelatedFormat->getAll();
        return $data ?: array();
    }

    public function post_relatedFormat($groupID, $typeID, $baseFormatID)
    {
        $formats = $this->Data->getPost('formats');
        $complexID = $this->Data->getPost('complexID');
        $this->PrintShopComplexRelatedFormat->deleteByComplex($baseFormatID, $complexID);
        
        foreach ($formats as $format) {
            $format['baseFormatID'] = $baseFormatID;
            $format['complexID'] = $complexID;
            if (!$this->PrintShopComplexRelatedFormat->create($format)) {
                return $this->sendFailResponse('03');
            }
        }
        return ['response' => true];
    }

    public function getByBaseID($groupID, $typeID, $baseTypeID)
    {
        $data = $this->PrintShopComplex->getByBaseID($baseTypeID);
        if (empty($data)) {
            return $this->sendFailResponse('06');
        }

        $aggregateBaseTypes = array_column($data, 'ID');
        $relatedFormats = $this->PrintShopComplexRelatedFormat->getByList($aggregateBaseTypes);

        foreach ($data as $key => $complex) {
            $data[$key]['relatedFormats'] = $relatedFormats[$complex['ID']] ?? array();
        }

        return $data;
    }
}
