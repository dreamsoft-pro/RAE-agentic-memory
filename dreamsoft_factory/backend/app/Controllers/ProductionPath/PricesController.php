<?php

namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Models\ProductionPath\DevicePrice;

class PricesController extends Controller
{
    /**
     * @var DevicePrice
     */
    protected $DevicePrice;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->DevicePrice = DevicePrice::getInstance();
    }

    public function index($deviceID)
    {
        return $this->DevicePrice->getListByRange($deviceID);
    }

    public function post_index($deviceID)
    {
        $data['deviceID'] = $deviceID;
        $data['amount'] = $this->Data->getPost('amount');
        $data['unitPrice'] = $this->Data->getPost('unitPrice');
        $data['unitCost'] = $this->Data->getPost('unitCost');
        $result=$this->DevicePrice->create($data);
        $response=['response'=>$result];
        if(!$result){
            $response['error']=$this->DevicePrice->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function delete_index($deviceID, $priceID)
    {
        $result=$this->DevicePrice->delete('ID', $priceID);
        $response=['response'=>$result];
        if(!$result){
            $response['error']=$this->DevicePrice->db->getError()['mysql']['message'];
        }
        return $response;
    }
}
