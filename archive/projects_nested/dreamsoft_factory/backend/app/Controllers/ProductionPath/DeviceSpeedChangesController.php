<?php

namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Models\ProductionPath\DeviceSideRelations;
use DreamSoft\Models\ProductionPath\DeviceSpeedChange;

class DeviceSpeedChangesController extends Controller
{
    /**
     * @var DeviceSpeedChange
     */
    private $DeviceSpeedChange;
    /**
     * @var DeviceSideRelations
     */
    private $DeviceSideRelations;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->DeviceSpeedChange = DeviceSpeedChange::getInstance();
        $this->DeviceSideRelations = DeviceSideRelations::getInstance();
    }

    public function index($deviceID)
    {
        return $this->DeviceSpeedChange->getOrderedList($deviceID);
    }

    public function post_index($deviceID)
    {
        $result = $this->DeviceSpeedChange->create(['deviceID' => $deviceID] + $this->Data->getAllPost());
        $response = ['response' => $result];
        if (!$result) {
            $response['error'] = $this->DeviceSpeedChange->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function delete_index($deviceID, $speedID)
    {
        $result = $this->DeviceSpeedChange->delete('ID', $speedID);
        $response = ['response' => $result];
        if (!$result) {
            $response['error'] = $this->DeviceSpeedChange->db->getError()['mysql']['message'];
        }
        return $response;
    }
    public function sideRelations($deviceID)
    {
        return $this->DeviceSideRelations->getOrderedList($deviceID);
    }

    public function post_sideRelations($deviceID)
    {
        $result = $this->DeviceSideRelations->create(['deviceID' => $deviceID] + $this->Data->getAllPost());
        $response = ['response' => $result];
        if (!$result) {
            $response['error'] = $this->DeviceSideRelations->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function delete_sideRelations($deviceID, $id)
    {
        $result = $this->DeviceSideRelations->delete('ID', $id);
        $response = ['response' => $result];
        if (!$result) {
            $response['error'] = $this->DeviceSideRelations->db->getError()['mysql']['message'];
        }
        return $response;
    }
}
