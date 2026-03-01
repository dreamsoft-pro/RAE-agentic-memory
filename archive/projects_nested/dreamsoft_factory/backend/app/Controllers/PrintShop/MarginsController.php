<?php

namespace DreamSoft\Controllers\PrintShop;

use DreamSoft\Core\Controller;
use DreamSoft\Models\Margin\Margin;

class MarginsController extends Controller
{
    /**
     * @var Margin
     */
    private $Margin;

    public function __construct($parameters = array())
    {
        $this->Margin = Margin::getInstance();
        parent::__construct($parameters);
    }

    public function index($priceListID, $natureID, $groupID=null, $typeID=null)
    {
        if($groupID){
            return $this->Margin->customGetAllInGroup($priceListID, $natureID, $groupID);
        }else if($typeID){
            return $this->Margin->customGetAllInType($priceListID, $natureID, $typeID);
        }
        return $this->Margin->customGetAll($priceListID, $natureID);
    }

    public function post_index()
    {
        $data = $this->Data->getAllPost();
        return ['response' => $this->Margin->create($data)];
    }

    public function put_index($marginId)
    {
        $data = $this->Data->getAllPost();
        return ['response' => $this->Margin->updateAll($marginId, $data)];
    }

    public function delete_index($marginId)
    {
        return ['response' => $this->Margin->delete('ID', $marginId)];
    }

}
