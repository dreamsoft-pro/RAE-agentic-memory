<?php

use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShop\PrintShopRealizationTime;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopProduct\PrintShopVolume;
use DreamSoft\Models\PrintShop\PrintShopRealizationTimeDetail;

class VolumesController extends Controller
{
    protected PrintShopVolume $PrintShopVolume;
    protected PrintShopRealizationTime $PrintShopRealizationTime;
    protected PrintShopType $PrintShopType;
    protected PrintShopRealizationTimeDetail $PrintShopRealizationTimeDetail;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopVolume = PrintShopVolume::getInstance();
        $this->PrintShopRealizationTime = PrintShopRealizationTime::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->PrintShopRealizationTimeDetail = PrintShopRealizationTimeDetail::getInstance();
    }

public function volumes($groupID, $typeID, $ID = NULL)
{
    $this->PrintShopVolume->setGroupID($groupID);
    $this->PrintShopVolume->setTypeID($typeID);

    if (intval($ID) > 0) {
        $data = $this->PrintShopVolume->get('ID', $ID);
        if ($data) {
            $data['formats'] = $this->PrintShopVolume->getFormats($ID);
        } else {
            $data = [];
        }
    } else {
        $data = $this->PrintShopVolume->getAll() ?: [];
        if (!empty($data)) {
            foreach ($data as $key => $v) {
                $formats = $this->PrintShopVolume->getFormats($v['ID']);
                $formatsIDs = array();

                if (!empty($formats)) {
                    foreach ($formats as $row) {
                        $formatsIDs[] = $row['formatID'];
                    }
                }
                $data[$key]['formats'] = $formatsIDs;
            }
        }
    }

    return $data;
}

    public function post_volumes($groupID, $typeID)
    {
        $this->PrintShopVolume->setGroupID($groupID);
        $this->PrintShopVolume->setTypeID($typeID);

        $volume = $this->Data->getPost('volume');
        $return = ['response' => false];

        if ($volume) {
            $ID = $this->PrintShopVolume->customExist($volume);
            if (!$ID) {
                $ID = $this->PrintShopVolume->customCreate($volume);
                $return = $this->PrintShopVolume->get('ID', $ID);
            } else {
                $return['info'] = 'Taki nakład już jest. Dude!';
            }
        }

        return $return;
    }

    public function patch_volumes($groupID, $typeID)
    {
        $this->PrintShopVolume->setGroupID($groupID);
        $this->PrintShopVolume->setTypeID($typeID);

        $action = $this->Data->getPost('action');
        $return = ['response' => false];

        switch ($action) {
            case 'formats':
                $formats = $this->Data->getPost('formats');
                $volumeID = $this->Data->getPost('ID');
                $res = $this->PrintShopVolume->deleteVolumeFormats($volumeID);
                if ($formats && !empty($formats) && $volumeID) {
                    $res = array_reduce($formats, function ($carry, $formatID) use ($volumeID) {
                        if (!$this->PrintShopVolume->existFormat($formatID, $volumeID)) {
                            return $carry && $this->PrintShopVolume->setFormat($formatID, $volumeID);
                        }
                        return $carry;
                    }, true);
                }
                $return['response'] = $res;
                break;

            case 'import':
                $data = $this->PrintShopVolume->getAllVolumes();
                $imports = 0;
                foreach ($data as $v) {
                    if ($v['formatID'] && !$this->PrintShopVolume->existFormat($v['formatID'], $v['ID'])) {
                        $imports += intval($this->PrintShopVolume->setFormat($v['formatID'], $v['ID']));
                    }
                }
                $return['info'] = $imports . ' - volumes format imported';
                $return['response'] = $imports > 0;
                break;

            case 'setCustomVolume':
                $custom = $this->Data->getPost('custom');
                $return['response'] = $custom == 1 ? $this->PrintShopVolume->customCreate() > 0 : $this->PrintShopVolume->deleteCustom();
                break;

            case 'setInvisibleVolume':
                $invisible = intval($this->Data->getPost('invisible'));
                $volumeID = $this->Data->getPost('ID');
                $return['response'] = $this->PrintShopVolume->update($volumeID, 'invisible', $invisible);
                if (!$return['response']) {
                    $return = $this->sendFailResponse('03');
                }
                break;
        }

        return $return;
    }

    public function post_setMaxVolume($groupID, $typeID)
    {
        $maxVolume = $this->Data->getPost('maxVolume');
        $this->PrintShopType->setGroupID($groupID);

        return ['response' => $this->PrintShopType->setMaxVolume($typeID, $maxVolume ?: null)];
    }
    public function post_setStepVolume($groupID, $typeID)
    {
        $stepVolume = $this->Data->getPost('stepVolume');
        $this->PrintShopType->setGroupID($groupID);

        return ['response' => $this->PrintShopType->setStepVolume($typeID, $stepVolume ?: null)];
    }

    public function delete_volumes($groupID, $typeID, $ID)
    {
        if ($ID) {
            $this->PrintShopVolume->setGroupID($groupID);
            $this->PrintShopVolume->setTypeID($typeID);
            $one = $this->PrintShopVolume->get('ID', $ID);

            if ($this->PrintShopVolume->defaultDelete($one['volume'])) {
                $this->PrintShopVolume->deleteVolumeFormats($ID);
                $this->PrintShopRealizationTime->setGroupID($groupID);
                $this->PrintShopRealizationTime->setTypeID($typeID);
                $this->PrintShopRealizationTime->setVolume($one['volume']);
                $realizationTimeDetailID = $this->PrintShopRealizationTime->getDetailsForVolume();
                $removedRTDetails = strval($this->PrintShopRealizationTimeDetail->delete('ID', $realizationTimeDetailID));
                return ['response' => true, 'infoRemovedRTDetails' => 'Removed: ' . $removedRTDetails . '. '];
            }
        }

        return ['response' => false];
    }

    public function customVolume($groupID, $typeID)
    {
        $this->PrintShopVolume->setGroupID($groupID);
        $this->PrintShopVolume->setTypeID($typeID);
        $return['custom'] = $this->PrintShopVolume->getCustom() ? 1 : 0;
        return $return;
    }
}
