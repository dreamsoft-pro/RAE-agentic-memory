<?php

namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Models\ProductionPath\DeviceSpeed;

class DeviceSpeedsController extends Controller
{
    /**
     * @var DeviceSpeed
     */
    protected $DeviceSpeed;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->DeviceSpeed = DeviceSpeed::getInstance();
    }

    public function index($deviceID)
    {
        return $this->DeviceSpeed->getListByDevice($deviceID);
    }

    public function post_index($deviceID)
    {
        $result=$this->DeviceSpeed->create(['deviceID'=>$deviceID]+$this->Data->getAllPost());
        $response=['response'=>$result];
        if(!$result){
            $response['error']=$this->DeviceSpeed->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function delete_index($deviceID, $speedID)
    {
        $result=$this->DeviceSpeed->delete('ID', $speedID);
        $response=['response'=>$result];
        if(!$result){
            $response['error']=$this->DeviceSpeed->db->getError()['mysql']['message'];
        }
        return $response;
    }
}
