<?php

use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShopConfig\PrintShopRelativeOptionsFilter;

class RelativeOptionsController extends Controller
{
    /**
     * @var PrintShopRelativeOptionsFilter
     */
    private $PrintShopRelativeOptionsFilter;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopRelativeOptionsFilter = PrintShopRelativeOptionsFilter::getInstance();
    }

    public function index($attrID, $optID)
    {
        return $this->PrintShopRelativeOptionsFilter->getOptionFilter($attrID, $optID);
    }

    public function put_index($attrID, $optID)
    {
        if (!$this->PrintShopRelativeOptionsFilter->delete(['attrID', 'optID'], [$attrID, $optID])) {
            return ['response' => false, 'error' => $this->PrintShopRelativeOptionsFilter->db->getError()['mysql']['message']];
        }
        $filter = $this->Data->getAllPost();
        foreach ($filter as $config) {
            if (!$this->PrintShopRelativeOptionsFilter->create([
                'attrID' => $attrID,
                'optID' => $optID,
                'descriptionTypeID' => $config['typeID'],
                'name' => $config['name'],
                'valueType' => $config['valueType'],
                'value' => $config['value']], false)) {
                return ['response' => false, 'error' => $this->PrintShopRelativeOptionsFilter->db->getError()['mysql']['message']];
            }
        }
        return ['response' => true];
    }

}
