<?php

use DreamSoft\Core\Controller;
use DreamSoft\Models\Other\Country;

/**
 * Created by PhpStorm.
 * User: rafal
 * Date: 31.01.17
 * Time: 20:02
 */
class CountriesController extends Controller
{
    /**
     * @var Country
     */
    private $Country;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Country = Country::getInstance();
    }

    public function index()
    {
        return $this->Country->getCountries();
    }

    public function patch_index()
    {
        $post = $this->Data->getAllPost();
        
        foreach($post as $country){
            if(!$this->Country->updateDisabledAndDefault($country['code'], $country['disabled'], $country['isDefault'])){
                return array('response' => false);
            }
        }

        return array('response' => true);
    }

    public function getAll(){
        return $this->Country->getAll();
    }
}
