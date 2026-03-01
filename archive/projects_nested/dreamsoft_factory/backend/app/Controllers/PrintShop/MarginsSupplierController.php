<?php

namespace DreamSoft\Controllers\PrintShop;

use DreamSoft\Core\Controller;
use DreamSoft\Models\Margin\MarginSupplier;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionDescription;

class MarginsSupplierController extends Controller
{
    /**
     * @var MarginSupplier
     */
    private $MarginSupplier;
    /**
     * @var PrintShopConfigOptionDescription
     */
    private $PrintShopConfigOptionDescription;

    public function __construct($parameters = array())
    {
        $this->MarginSupplier = MarginSupplier::getInstance();
        $this->PrintShopConfigOptionDescription = PrintShopConfigOptionDescription::getInstance();
        parent::__construct($parameters);
    }

    public function index()
    {
        return $this->MarginSupplier->getAll();
    }

    public function post_index()
    {
        $data = $this->Data->getAllPost();
        return ['response' => $this->MarginSupplier->create($data)];
    }

    public function put_index($marginId)
    {
        $data = $this->Data->getAllPost();
        return ['response' => $this->MarginSupplier->updateAll($marginId, $data)];
    }

    public function delete_index($marginId)
    {
        return ['response' => $this->MarginSupplier->delete('ID', $marginId)];
    }

    public function getAllSuppliers()
    {
        $this->PrintShopConfigOptionDescription->setDomainID($this->getDomainID());
        return array_merge($this->PrintShopConfigOptionDescription->getAllValuesByTypeName('manufacturer'), $this->PrintShopConfigOptionDescription->getAllValuesByTypeName('supplier'));
    }

}
