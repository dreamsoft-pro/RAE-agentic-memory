<?php

use DreamSoft\Controllers\Components\Price;
use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShopProduct\PrintShopIncrease;

class IncreasesController extends Controller
{
    protected $PrintShopIncrease;
    protected $Price;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopIncrease = PrintShopIncrease::getInstance();
        $this->Price = Price::getInstance();
    }

    public function increases($groupID, $typeID, $formatID = null)
    {
        $this->PrintShopIncrease->setGroupID($groupID);
        $this->PrintShopIncrease->setTypeID($typeID);

        $data = $this->PrintShopIncrease->customGetAll($formatID);
        $res = [];

        if (!empty($data)) {
            foreach ($data as $i) {
                if (in_array($i['unit'], ['price', 'price_per_unit'])) {
                    $i['value'] = $this->Price->getNumberToView($i['value']);
                }
                $res[$i['formatID']][] = $i;
            }
        }

        sort($res);

        return $res ?: [];
    }

    public function patch_increases($groupID, $typeID)
    {
        $this->PrintShopIncrease->setGroupID($groupID);
        $this->PrintShopIncrease->setTypeID($typeID);

        $value = $this->Data->getPost('value');
        $amount = $this->Data->getPost('amount');
        $type = $this->Data->getPost('type');
        $formatID = $this->Data->getPost('formatID');
        $remove = $this->Data->getPost('remove');

        $oneType = $this->PrintShopIncrease->getType($type);
        if (in_array($oneType['unit'], ['price', 'price_per_unit'])) {
            $value = $this->Price->getPriceToDb($value);
        }

        if ($remove) {
            $res = $this->PrintShopIncrease->delete('ID', $remove);
            return ['response' => $res, 'info' => 'remove'];
        }

        $ID = $this->PrintShopIncrease->exist($amount, $type, $formatID);
        if ($ID > 0) {
            $up = [
                intval($this->PrintShopIncrease->update($ID, 'amount', $amount)),
                intval($this->PrintShopIncrease->update($ID, 'value', $value))
            ];
            if (array_sum($up) == 2) {
                $item = $this->PrintShopIncrease->get('ID', $ID);
                $item['unit'] = $oneType['unit'];
                if (in_array($item['unit'], ['price', 'price_per_unit'])) {
                    $item['value'] = $this->Price->getNumberToView($item['value']);
                }
                return ['response' => true, 'info' => 'update', 'item' => $item];
            } else {
                return ['response' => false, 'info' => 'update'];
            }
        }

        if ($amount && $value && $type) {
            $lastID = $this->PrintShopIncrease->customCreate($amount, $value, $type, $formatID);
            $result = $lastID > 0;
            $data['response'] = $result;

            if ($result) {
                $item = $this->PrintShopIncrease->get('ID', $lastID);
                $item['unit'] = $oneType['unit'];
                if (in_array($item['unit'], ['price', 'price_per_unit'])) {
                    $item['value'] = $this->Price->getNumberToView($item['value']);
                }
                $data['item'] = $item;
            }
            return $data;
        }

        return ['response' => false];
    }

    public function types()
    {
        $data = $this->PrintShopIncrease->getTypes();
        return $data ?: [];
    }
}
