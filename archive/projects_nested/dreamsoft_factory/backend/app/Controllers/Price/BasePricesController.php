<?php

namespace DreamSoft\Controllers\Price;

use DreamSoft\Core\Controller;
use DreamSoft\Models\Price\BasePrice;

/**
 * Class BasePricesController
 * @package DreamSoft\Controllers\Price
 */
class BasePricesController extends Controller
{
    /**
     * @var BasePrice
     */
    protected $BasePrice;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->BasePrice = BasePrice::getInstance();
    }

    /**
     * @return array
     */
    public function post_index()
    {
        $price = $this->Data->getPost('price');
        $grossPrice = $this->Data->getPost('grossPrice');
        $currency = $this->Data->getPost('currency');
        $baseCurrency = $this->Data->getPost('baseCurrency');
        $exchangeRate = $this->Data->getPost('exchangeRate');
        $taxID = $this->Data->getPost('taxID');
        $date = time();

        $required = compact('price', 'grossPrice', 'currency', 'baseCurrency', 'exchangeRate', 'taxID', 'date');

        if (in_array(null, $required, true)) {
            return $this->sendFailResponse('01');
        }

        $lastID = $this->BasePrice->create($required);
        $return = $this->BasePrice->get('ID', $lastID);
        if (!$return) {
            return $this->sendFailResponse('03');
        }
        return $return;
    }

    /**
     * @return array
     */
    public function put_index()
    {
        $post = $this->Data->getAllPost();
        $goodKeys = ['price', 'grossPrice', 'currency', 'baseCurrency', 'exchangeRate', 'taxID'];
        $return = ['response' => false];

        if (!empty($post['ID'])) {
            $ID = $post['ID'];
            unset($post['ID']);
            foreach ($post as $key => $value) {
                if (in_array($key, $goodKeys)) {
                    $this->BasePrice->update($ID, $key, $value);
                }
            }
            $return['response'] = true;
        }
        return $return;
    }

    /**
     * @param int $ID
     * @return array
     */
    public function delete_index($ID)
    {
        $data = ['response' => false, 'ID' => $ID];
        if (intval($ID) > 0) {
            if ($this->BasePrice->delete('ID', $ID)) {
                $data['response'] = true;
            } else {
                return $this->sendFailResponse('05');
            }
        } else {
            return $this->sendFailResponse('04');
        }
        return $data;
    }
}
