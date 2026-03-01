<?php

use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigEfficiency;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigEfficiencySideRelations;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigEfficiencySpeed;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigEfficiencySpeedChanges;

class EfficiencyConfigController extends Controller
{
    /**
     * @var PrintShopConfigEfficiency
     */
    private $PrintShopConfigEfficiency;
    /**
     * @var PrintShopConfigEfficiencySpeed
     */
    private $PrintShopConfigEfficiencySpeed;
    /**
     * @var PrintShopConfigEfficiencySpeedChanges
     */
    private $PrintShopConfigEfficiencySpeedChanges;
    /**
     * @var PrintShopConfigEfficiencySideRelations
     */
    private $PrintShopConfigEfficiencySideRelations;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopConfigEfficiency = PrintShopConfigEfficiency::getInstance();
        $this->PrintShopConfigEfficiencySpeed = PrintShopConfigEfficiencySpeed::getInstance();
        $this->PrintShopConfigEfficiencySpeedChanges = PrintShopConfigEfficiencySpeedChanges::getInstance();
        $this->PrintShopConfigEfficiencySideRelations = PrintShopConfigEfficiencySideRelations::getInstance();
    }

    public function index($attrID, $optionID, $controllerID)
    {
        if (!$controllerID) {
            $controllerID = null;
        }
        $this->PrintShopConfigEfficiency->setAttrID($attrID);
        $this->PrintShopConfigEfficiency->setOptID($optionID);
        $this->PrintShopConfigEfficiency->setControllerID($controllerID);
        $efficiency = $this->PrintShopConfigEfficiency->customGet();
        if ($efficiency) {
            return $efficiency;
        }
        if (!$controllerID) {
            return [];
        }
        //find device from controller TODO
    }

    public function put_index($attrID, $optionID, $controllerID)
    {
        if (!$controllerID) {
            $controllerID = null;
        }
        if (!$this->Data->getPost('ID')) {
            $response = ['response' => $this->PrintShopConfigEfficiency->create(['attrID' => $attrID, 'optID' => $optionID, 'controllerID' => $controllerID]
                + $this->Data->getPost(['deviceTime', 'stackImpositionTime', 'stackHeight', 'printedStackHeight', 'transportTime']))];
            if (!$response['response']) {
                $response['error'] = $this->PrintShopConfigEfficiency->db->getError()['mysql']['message'];
            }
            return $response;
        } else {
            $response = ['response' => $this->PrintShopConfigEfficiency->updateAll($this->Data->getPost('ID'), ['attrID' => $attrID, 'optID' => $optionID, 'controllerID' => $controllerID]
                + $this->Data->getPost(['deviceTime', 'stackImpositionTime', 'stackHeight', 'printedStackHeight', 'transportTime']))];
            if (!$response['response']) {
                $response['error'] = $this->PrintShopConfigEfficiency->db->getError()['mysql']['message'];
            }
            return $response;
        }

    }

    public function speeds($attrID, $optionID, $controllerID)
    {
        $this->PrintShopConfigEfficiencySpeed->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySpeed->setOptID($optionID);
        $this->PrintShopConfigEfficiencySpeed->setControllerID($controllerID);
        $localResult = $this->PrintShopConfigEfficiencySpeed->getOrderedList();
        if ($controllerID) {
            //TODO device
        }
        return $localResult;

    }

    public function post_speeds($attrID, $optionID, $controllerID)
    {
        if (!$controllerID) {
            $controllerID = null;
        }
        $this->PrintShopConfigEfficiencySpeed->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySpeed->setOptID($optionID);
        $this->PrintShopConfigEfficiencySpeed->setControllerID($controllerID);
        $response = ['response' => $this->PrintShopConfigEfficiencySpeed->create(['attrID' => $attrID, 'optID' => $optionID, 'controllerID' => $controllerID] + $this->Data->getAllPost())];
        if (!$response['response']) {
            $response['error'] = $this->PrintShopConfigEfficiencySpeed->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function delete_speeds($attrID, $optionID, $controllerID, $speedID)
    {
        $response = ['response' => $this->PrintShopConfigEfficiencySpeed->delete('ID', $speedID)];
        if (!$response['response']) {
            $response['error'] = $this->PrintShopConfigEfficiencySpeed->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function speedChanges($attrID, $optionID, $controllerID)
    {
        $this->PrintShopConfigEfficiencySpeedChanges->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySpeedChanges->setOptID($optionID);
        $this->PrintShopConfigEfficiencySpeedChanges->setControllerID($controllerID);
        $localResult = $this->PrintShopConfigEfficiencySpeedChanges->getOrderedList();
        if ($controllerID) {
            //TODO device
        }
        return $localResult;
    }

    public function post_speedChanges($attrID, $optionID, $controllerID)
    {
        if (!$controllerID) {
            $controllerID = null;
        }
        $this->PrintShopConfigEfficiencySpeedChanges->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySpeedChanges->setOptID($optionID);
        $this->PrintShopConfigEfficiencySpeedChanges->setControllerID($controllerID);
        $response = ['response' => $this->PrintShopConfigEfficiencySpeedChanges->create(['attrID' => $attrID, 'optID' => $optionID, 'controllerID' => $controllerID] + $this->Data->getAllPost())];
        if (!$response['response']) {
            $response['error'] = $this->PrintShopConfigEfficiencySpeedChanges->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function delete_speedChanges($attrID, $optionID, $controllerID, $speedChangeID)
    {
        $response = ['response' => $this->PrintShopConfigEfficiencySpeedChanges->delete('ID', $speedChangeID)];
        if (!$response['response']) {
            $response['error'] = $this->PrintShopConfigEfficiencySpeedChanges->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function sideRelations($attrID, $optionID, $controllerID)
    {
        $this->PrintShopConfigEfficiencySideRelations->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySideRelations->setOptID($optionID);
        $this->PrintShopConfigEfficiencySideRelations->setControllerID($controllerID);
        $localResult = $this->PrintShopConfigEfficiencySideRelations->getOrderedList();
        if ($controllerID) {
            //TODO device
        }
        return $localResult;
    }

    public function post_sideRelations($attrID, $optionID, $controllerID)
    {
        if (!$controllerID) {
            $controllerID = null;
        }
        $this->PrintShopConfigEfficiencySideRelations->setAttrID($attrID);
        $this->PrintShopConfigEfficiencySideRelations->setOptID($optionID);
        $this->PrintShopConfigEfficiencySideRelations->setControllerID($controllerID);
        $response = ['response' => $this->PrintShopConfigEfficiencySideRelations->create(['attrID' => $attrID, 'optID' => $optionID, 'controllerID' => $controllerID] + $this->Data->getAllPost())];
        if (!$response['response']) {
            $response['error'] = $this->PrintShopConfigEfficiencySideRelations->db->getError()['mysql']['message'];
        }
        return $response;
    }

    public function delete_sideRelations($attrID, $optionID, $controllerID, $sideRelationID)
    {
        $response = ['response' => $this->PrintShopConfigEfficiencySideRelations->delete('ID', $sideRelationID)];
        if (!$response['response']) {
            $response['error'] = $this->PrintShopConfigEfficiencySideRelations->db->getError()['mysql']['message'];
        }
        return $response;
    }
}
