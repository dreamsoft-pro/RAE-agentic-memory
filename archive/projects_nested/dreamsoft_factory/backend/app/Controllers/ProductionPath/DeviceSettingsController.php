<?php

namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Models\ProductionPath\Device;
use DreamSoft\Models\ProductionPath\DeviceSpeed;

class DeviceSettingsController extends Controller
{
    /**
     * @var Device
     */
    private $Device;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Device = Device::getInstance();
    }

    public function index($deviceID)
    {
        return $this->Device->get('ID',$deviceID);
    }

    public function put_index($deviceID)
    {
        $result = $this->Device->updateAll($deviceID, $this->Data->getPost(['sheetSizeMin', 'sheetSizeMax', 'grammageMax', 'grammageMin', 'thicknessMin', 'thicknessMax', 'stiffnessMin', 'stiffnessMax', 'multiOperator', 'multiProcess', 'defaultPath', 'countAdditionalOperation', 'runningTasksAlert', 'operationPlannedTime', 'worksInSaturday', 'worksInSunday', 'defaultOperationTime']));
        $response = ['response' => $result];
        if (!$result) {
            $response['error'] = $this->Device->db->getError()['mysql']['message'];
        }
        return $response;
    }

}
