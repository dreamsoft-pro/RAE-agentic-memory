<?php

use DreamSoft\Core\Controller;
use DreamSoft\Models\Lang\LangSetting;
use DreamSoft\Models\Mongo\MgFormat;
use DreamSoft\Models\PrintShopProduct\{
    PrintShopFormatLanguage, PrintShopFormat, PrintShopFormatName, PrintShopPreFlight, PrintShopPrintTypeWorkspace
};
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrintType;
use DreamSoft\Controllers\Components\Standard;
use DreamSoft\Models\PrintShop\{
    PrintShopComplex, PrintShopComplexRelatedFormat
};

class FormatsController extends Controller
{
    public $useModels = ['LangSetting'];
    protected PrintShopFormat $PrintShopFormat;
    protected LangSetting $LangSetting;
    protected PrintShopFormatName $PrintShopFormatName;
    protected PrintShopConfigPrintType $PrintShopConfigPrintType;
    protected PrintShopPreFlight $PrintShopPreFlight;
    protected PrintShopFormatLanguage $PrintShopFormatLanguage;
    protected PrintShopComplexRelatedFormat $PrintShopComplexRelatedFormat;
    protected PrintShopComplex $PrintShopComplex;
    private PrintShopPrintTypeWorkspace $PrintShopPrintTypeWorkspace;
    private $Standard;
    private $MgFormat;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopFormat = PrintShopFormat::getInstance();
        $this->PrintShopFormatLanguage = PrintShopFormatLanguage::getInstance();
        $this->PrintShopConfigPrintType = PrintShopConfigPrintType::getInstance();
        $this->PrintShopPreFlight = PrintShopPreFlight::getInstance();
        $this->PrintShopComplexRelatedFormat = PrintShopComplexRelatedFormat::getInstance();
        $this->PrintShopComplex = PrintShopComplex::getInstance();
        $this->LangSetting = LangSetting::getInstance();
        $this->PrintShopFormatName = PrintShopFormatName::getInstance();
        $this->PrintShopPrintTypeWorkspace = PrintShopPrintTypeWorkspace::getInstance();
        $this->Standard = Standard::getInstance();
        $this->MgFormat = MgFormat::getInstance();
    }

    public function setDomainID($ID)
    {
        parent::setDomainID($ID);
        $this->LangSetting->setDomainID($ID);
    }

    private function _formats($groupID, $typeID, $complexID = NULL, $ID = NULL, $public = 0)
    {
        $this->PrintShopFormat->setGroupID($groupID);
        $this->PrintShopFormat->setTypeID($typeID);

        if (intval($ID) > 0) {
            return $this->PrintShopFormat->getOne($ID);
        } 

        $active = $public == 1 ? 1 : NULL;
        $data = $this->PrintShopFormat->getAll($active);
        if (empty($data)) {
            return [];
        }

        $data = $this->fillWithDefaultLangName($data);
        $allIDs = array_column($data, 'ID');
        
        foreach ($data as $key => $val) {
            $data[$key]['printTypes'] = $this->processPrintTypes($val['printTypesList']);
            if ($val['unit'] == 2) {
                $data = $this->convertUnitsToCentimeter($data, $key, [
                    'height', 'width', 'depth', 'slope', 'maxHeight', 'maxWidth', 'maxDepth', 'minHeight', 'minWidth','minDepth'
                ]);
            }
            unset($data[$key]['printTypesList']);
        }

        $data = $this->checkPrintTypeWorkspacesExist($data);

        if ($complexID) {
            $data = $this->attachRelatedFormats($data, $complexID, $allIDs, $typeID);
        }

        return $data;
    }

    private function convertToCentimeter($value)
    {
        return intval($value) > 0 ? $value / 10 : $value;
    }

    private function convertUnitsToCentimeter($data, $key, $fields)
    {
        foreach ($fields as $field) {
            $data[$key][$field] = $this->convertToCentimeter($data[$key][$field]);
        }
        return $data;
    }

    private function processPrintTypes($printTypesList)
    {
        $printTypes = [];
        $exp = explode(';', $printTypesList);
        foreach ($exp as $e) {
            if (strlen($e) == 0) continue;
            $exp2 = explode(':', $e);
            $minVolume = $maxVolume = $stepVolume = NULL;
            if (isset($exp2[1])) {
                list($minVolume, $maxVolume, $stepVolume) = explode('-', $exp2[1]);
            }
            $printTypes[] = [
                'printTypeID' => $exp2[0],
                'minVolume' => $minVolume,
                'maxVolume' => $maxVolume,
                'stepVolume' => 1
            ];
        }
        return $printTypes;
    }

    private function checkPrintTypeWorkspacesExist($data)
    {
        if (!$data) {
            return $data;
        }

        $formatsAggregate = array_column($data, 'ID');
        $printTypesAggregate = [];
        foreach ($data as $row) {
            foreach ($row['printTypes'] as $printType) {
                $printTypesAggregate[] = $printType['printTypeID'];
            }
        }

        $printTypeWorkspaces = $this->PrintShopPrintTypeWorkspace->getByAggregateData(
            array_unique($printTypesAggregate),
            array_unique($formatsAggregate)
        );

        foreach ($data as $formatKey => $row) {
            foreach ($row['printTypes'] as $printTypeKey => $printType) {
                $data[$formatKey]['printTypes'][$printTypeKey]['printTypeWorkspaceExist'] = isset($printTypeWorkspaces[$row['ID']][$printType['printTypeID']]);
            }
        }

        return $data;
    }

    private function fillWithDefaultLangName($formats)
    {
        $languages = $this->LangSetting->getAll();

        if (!$languages) {
            return $formats;
        }

        $activeLanguages = array_filter($languages, fn($lang) => $lang['active'] == 1);

        foreach ($formats as $key => $format) {
            foreach ($activeLanguages as $al) {
                if (!isset($format['langs'][$al['code']]) || empty($format['langs'][$al['code']])) {
                    $formats[$key]['langs'][$al['code']]['name'] = $format['name'];
                }
            }
        }

        return $formats;
    }

    public function formats($groupID, $typeID, $ID = NULL)
    {
        return $this->_formats($groupID, $typeID, NULL, $ID, 0) ?? [];
    }

    public function formatsPublic($groupID, $typeID, $complexID, $ID = NULL)
    {
        return $this->_formats($groupID, $typeID, $complexID, $ID, 1) ?? [];
    }

    public function post_formats($groupID, $typeID)
    {
        $this->PrintShopFormat->setGroupID($groupID);
        $this->PrintShopFormat->setTypeID($typeID);

        $postData = $this->Data->getAllPost();
        $fields = ['name', 'adminName', 'width', 'height', 'depth', 'slope', 'custom', 'interchangeability', 'minWidth',
            'minHeight','minDepth', 'maxWidth', 'maxHeight','maxDepth' , 'netWidth', 'netHeight', 'slopeExternalLeft',
            'slopeExternalRight', 'slopeExternalFront', 'slopeExternalBack', 'slopeExternalTop', 'slopeExternalBottom',
            'addRidgeThickness', 'wingtipFront', 'wingtipFrontMin', 'wingtipBack', 'wingtipBackMin',
            'maximumTotalGrossWidth', 'binding', 'unit', 'widthStep', 'heightStep', 'depthStep'];

        foreach ($fields as $field) {
            $$field = $this->Data->getPost($field) ?? null;
        }

        $unit = $unit ?: 1;
        $interchangeability = $interchangeability ?: 0;
        $custom = $custom ?: 0;
        $names = $this->Data->getPost('names');

        foreach (['width', 'height', 'depth', 'minWidth', 'minHeight', 'minDepth', 'maxWidth', 'maxHeight', 'maxDepth',
                     'slope', 'netWidth', 'netHeight', 'slopeExternalLeft', 'slopeExternalRight', 'slopeExternalTop',
                     'slopeExternalBottom', 'slopeExternalFront', 'slopeExternalBack', 'wingtipFront',
                     'wingtipFrontMin', 'wingtipBack', 'wingtipBackMin', 'maximumTotalGrossWidth'] as $field) {
            $$field = $this->Standard->normalizeLength($$field, $unit);
        }

        if (($name || $names) && $slope !== null) {
            $lastID = $this->PrintShopFormat->createByParams(
                $name, $adminName, $width, $height, $depth, $slope, $netWidth, $netHeight, $slopeExternalLeft,
                $slopeExternalRight, $slopeExternalTop, $slopeExternalBottom, $slopeExternalFront,
                $slopeExternalBack, $wingtipFront, $addRidgeThickness, $wingtipFrontMin, $wingtipBack,
                $wingtipBackMin, $maximumTotalGrossWidth, $binding, $interchangeability, $custom
            );

            if ($custom) {
                $this->PrintShopFormat->createCustom($lastID, $minWidth, $minHeight, $minDepth, $maxWidth, $maxHeight,$maxDepth);
            }

            $this->MgFormat->getAdapter()->insertOne([
                'formatID' => $lastID,
                'width' => $width,
                'height' => $height,
                'depth' => $depth,
                'slope' => $slope,
                'name' => $name,
                'typeID' => $typeID,
                'external' => true,
                '__v' => 1,
                'Attributes' => array(),
                'Themes' => array(),
                'Views' => array()
            ]);

            $return = $this->PrintShopFormat->customGet($lastID) ?: ['response' => false];

            if ($names) {
                foreach ($names as $lang => $name) {
                    if (!$this->PrintShopFormatLanguage->set($lang, $name, $lastID)) {
                        return $this->sendFailResponse('09');
                    }
                    $return['langs'][$lang]['name'] = $name;
                }
            }

            if ($unit > 1) {
                $this->PrintShopFormat->update($lastID, 'unit', $unit);
                $return['unit'] = $unit;
                $fields = [
                    'width', 'height', 'depth', 'maxHeight', 'maxWidth','maxDepth', 'minHeight',
                    'minWidth','minDepth', 'slope', 'netWidth', 'netHeight', 'slopeExternalLeft',
                    'slopeExternalRight', 'slopeExternalTop', 'slopeExternalBottom', 'wingtipFront',
                    'wingtipFrontMin', 'wingtipBack', 'wingtipBackMin', 'maximumTotalGrossWidth'
                ];
                foreach ($fields as $field) {
                    $return = $this->convertEntityToCentimeter($return, $field);
                }
            }

            return $return;
        }

        return $this->sendFailResponse('01');
    }

    public function put_formats($groupID, $typeID)
    {
        $this->PrintShopFormat->setGroupID($groupID);
        $this->PrintShopFormat->setTypeID($typeID);

        $post = $this->Data->getAllPost();
        $names = $post['langs'] ?? [];
        unset($post['langs']);

        $baseKeys = [
            'name', 'adminName', 'width', 'height', 'depth', 'slope', 'custom', 'interchangeability', 'active', 'unit',
            'netWidth', 'netHeight', 'slopeExternalLeft', 'slopeExternalRight', 'slopeExternalTop', 
            'slopeExternalBottom',  'slopeExternalFront', 'slopeExternalBack', 'addRidgeThickness', 'wingtipFront',
            'wingtipFrontMin', 'wingtipBack', 'wingtipBackMin', 'maximumTotalGrossWidth', 'binding'
        ];
        $customKeys = ['minWidth', 'maxWidth', 'minHeight', 'maxHeight','minDepth',
                       'maxDepth,','widthStep', 'heightStep', 'depthStep' ];

        $ID = $post['ID'] ?? null;
        if (!$ID) {
            return ['response' => false];
        }
        unset($post['ID'], $post['customID']);
        
        $unit = $post['unit'];
        $custom = $post['custom'] ?? false;
        $res = true;

        foreach ($post as $key => $value) {
            if (in_array($key, $baseKeys)) {
                $value = $this->normalizeField($key, $value, $unit);
                $res &= $this->PrintShopFormat->update($ID, $key, $value);
            }
            if ($custom && in_array($key, $customKeys)) {
                $value = $this->normalizeField($key, $value, $unit);
                $res &= $this->PrintShopFormat->updateCustom($ID, $key, $value);
            }
            if (in_array($key, ['width', 'height', 'slope', 'name'])) {
                $this->MgFormat->getAdapter()->updateOne(['formatID' => $ID], ['$set' => [$key => $value]]);
            }
        }

        foreach ($names as $lang => $name) {
            if (strlen($name['name']) == 0) continue;
            $res &= $this->PrintShopFormatLanguage->set($lang, $name['name'], $ID);
        }

        return ['response' => $res];
    }

    private function normalizeField($key, $value, $unit)
    {
        if (in_array($key, ['width', 'height', 'depth', 'slope', 'netWidth', 'netHeight', 'slopeExternalLeft',
                            'slopeExternalRight', 'slopeExternalTop', 'slopeExternalBottom', 
                            'wingtipFront', 'wingtipFrontMin', 'wingtipBack', 'wingtipBackMin', 
                            'maximumTotalGrossWidth']) && $unit == 2) {
            return $value * 10;
        }
        if ($key === 'active') {
            return intval($value);
        }
        return $value == '' ? null : $value;
    }

    public function patch_formats($groupID, $typeID, $formatID)
    {
        $action = $this->Data->getPost('action');
        $data['response'] = false;

        if ($action === 'setPrintTypes') {
            return $this->setPrintTypes($formatID, $this->Data->getPost('printTypes'));
        }

        if ($action === 'setPrintTypeWorkspaces') {
            return $this->setPrintTypeWorkspaces(
                $formatID,
                $this->Data->getPost('printTypeID'),
                $this->Data->getPost('workspaces')
            );
        }

        return $data;
    }

    private function setPrintTypes($formatID, $printTypes)
    {
        $data['response'] = false;
        $savedCounter = 0;

        if ($printTypes) {
            $this->PrintShopFormat->deletePrintTypes($formatID);
            foreach ($printTypes as $row) {
                if ($this->PrintShopFormat->createPrintType(
                    $formatID, $row['printTypeID'],
                    $row['minVolume'],
                    $row['maxVolume']
                    ) > 0) { $savedCounter++; }
            }
            if ($savedCounter > 0) {
                $data['response'] = true;
                $data['savedCounter'] = $savedCounter;
            }
        } else {
            $data['response'] = $this->PrintShopFormat->deletePrintTypes($formatID);
            $data['info'] = 'removed_all';
        }

        return $data;
    }

    private function setPrintTypeWorkspaces($formatID, $printTypeID, $workspaces)
    {
        $data['response'] = false;
        $savedCounter = 0;

        if ($workspaces) {
            $this->PrintShopPrintTypeWorkspace->deleteByParams($printTypeID, $formatID);
            foreach ($workspaces as $row) {
                $params = [
                    'formatID' => $formatID,
                    'printTypeID' => $printTypeID,
                    'workspaceID' => $row['workspaceID'],
                    'usePerSheet' => $row['usePerSheet'],
                    'operationDuplication' => $row['operationDuplication']
                ];
                if ($this->PrintShopPrintTypeWorkspace->create($params) > 0) {
                    $savedCounter++;
                }
            }
            if ($savedCounter > 0) {
                $data['response'] = true;
                $data['savedCounter'] = $savedCounter;
            }
        } else {
            $data['response'] = $this->PrintShopPrintTypeWorkspace->deleteByParams($printTypeID, $formatID);
            $data['info'] = 'removed_all';
        }

        return $data;
    }

    public function delete_formats($groupID, $typeID, $ID)
    {
        if (intval($ID) > 0 && $this->PrintShopFormat->customDelete($ID)) {
            $this->PrintShopFormat->deletePrintTypes($ID);
            $this->PrintShopPreFlight->delete('formatID', $ID);
            $this->PrintShopFormatLanguage->delete('ID', $ID);
            $this->MgFormat->getAdapter()->deleteOne(['formatID' => intval($ID)]);
            return ['response' => true];
        }
        return ['response' => false];
    }

    public function patch_sortFormats()
    {
        $post = $this->Data->getAllPost();
        $this->Standard->setModel($this->PrintShopFormat);
        return $this->Standard->sort($post);
    }

    public function customName($typeID)
    {
        return $this->prepareCustomNames($this->PrintShopFormatName->getByType($typeID));
    }

    private function prepareCustomNames($data)
    {
        if (!$data) {
            return [];
        }

        $list = [];
        foreach ($data as $row) {
            $list[$row['lang']] = $row['name'];
        }
        return $list;
    }

    public function patch_customName($typeID)
    {
        $post = $this->Data->getAllPost();
        if ($post['names'] === null) {
            return $this->sendFailResponse('02');
        }

        $updated = $saved = $deleted = 0;

        if (empty($post['names'])) {
            $deleted += $this->PrintShopFormatName->delete('typeID', $typeID);
        }

        foreach ($post['names'] as $lang => $name) {
            $existFormatNameID = $this->PrintShopFormatName->nameExist($typeID, $lang);
            if ($existFormatNameID) {
                if (strlen($name) == 0) {
                    $deleted += $this->PrintShopFormatName->delete('ID', $existFormatNameID);
                } else {
                    $updated += $this->PrintShopFormatName->update($existFormatNameID, 'name', $name);
                }
            } else {
                $params = [
                    'lang' => $lang,
                    'name' => $name,
                    'typeID' => $typeID
                ];
                if ($this->PrintShopFormatName->create($params) > 0) {
                    $saved++;
                }
            }
        }

        if (($updated + $saved + $deleted) > 0) {
            $customNames = $this->PrintShopFormatName->getByType($typeID);
            return [
                'response' => true,
                'saved' => $saved,
                'updated' => $updated,
                'deleted' => $deleted,
                'customNames' => $this->prepareCustomNames($customNames)
            ];
        }

        return ['response' => false];
    }

    private function attachRelatedFormats($data, $complexID, $allIDs, $typeID)
    {
        $complex = $this->PrintShopComplex->getBase($complexID);

        if (!$complex) {
            return $data;
        }

        $typesComplex = $this->PrintShopComplex->getByBaseID($complex['baseID'], $complex['complexGroupID']);
        $typesArr = array_column(array_filter($typesComplex, fn($tc) => $tc['typeID'] != $typeID), 'typeID');

        if (!$typesArr) {
            return $data;
        }

        $relatedFormats = $this->PrintShopComplexRelatedFormat->getByBaseFormatIDs($allIDs, $typesArr, $complex['ID']);
        if (!$relatedFormats) {
            return $data;
        }

        $rf = [];
        foreach ($relatedFormats as $relatedFormat) {
            $formatID = $relatedFormat['baseFormatID'];
            $rf[$formatID][] = $relatedFormat;
        }

        foreach ($data as $key => $val) {
            if (isset($rf[$val['ID']])) {
                $data[$key]['relatedFormats'] = $rf[$val['ID']];
            }
        }

        return $data;
    }
}
