<?php

namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Models\ProductionPath\DeviceServices;
use DreamSoft\Models\ProductionPath\DeviceSpeed;

class DeviceServicesController extends Controller
{
    /**
     * @var DeviceServices
     */
    protected $DeviceServices;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->DeviceServices = DeviceServices::getInstance();
    }

    public function index($deviceID)
    {
        return $this->DeviceServices->getListByID($deviceID);
    }

    public function post_index($deviceID)
    {
        $result = $this->DeviceServices->create(['deviceID' => $deviceID] + $this->Data->getAllPost());
        $response = ['response' => $result];
        if (!$result) {
            $response['error'] = $this->DeviceServices->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function delete_index($deviceID, $id)
    {
        $result = $this->DeviceServices->delete('ID', $id);
        $response = ['response' => $result];
        if (!$result) {
            $response['error'] = $this->DeviceServices->db->getError()['mysql']['message'];
        }
        return $response;
    }
}
