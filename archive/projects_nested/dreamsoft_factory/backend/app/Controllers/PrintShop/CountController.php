<?php

namespace DreamSoft\Controllers\PrintShop;

use DreamSoft\Controllers\Components\Price;
use DreamSoft\Core\Controller;
use DreamSoft\Controllers\Components\CalculatorCollect;
use DreamSoft\Models\Price\BasePrice;

/**
 * Class CountController
 * @package DreamSoft\Controllers\PrintShop
 */
class CountController extends Controller
{
    /**
     * @var Price
     */
    protected $Price;

    /**
     * @var BasePrice
     */
    protected $BasePrice;

    /**
     * @var CalculatorCollect
     */
    protected $Calculator;

    /**
     * CountController constructor.
     * @param array $parameters
     */
    public function __construct(array $parameters = [])
    {
        parent::__construct($parameters);
        $this->Price = Price::getInstance();
        $this->BasePrice = BasePrice::getInstance();
        $this->Calculator = new CalculatorCollect();
    }

    /**
     * @return array|null
     */
    public function patch_index()
    {
        return $this->Data->getAllPost();
    }

    /**
     * @return array
     */
    public function patch_cartReCalculate()
    {
        $post = $this->Data->getAllPost();
        $products = $post['products'];

        $aggregatePrices = array_column($products, 'priceID');
        $reCount = $this->Calculator->calculate($products);

        return ['response' => $reCount];
    }

    /**
     * @return array
     */
    public function patch_cartRestorePrices()
    {
        $post = $this->Data->getAllPost();
        $products = $post['products'];

        $restore = $this->Calculator->restorePrices($products);

        return ['response' => $restore];
    }
}
