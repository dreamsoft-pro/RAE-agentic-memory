<?php

namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Models\Address\Address;
use DreamSoft\Models\Address\AddressUser;
use DreamSoft\Models\Order\DpOrder;
use DreamSoft\Models\Order\DpOrderAddress;
use DreamSoft\Models\Order\DpOrderAddressProduct;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Models\ProductionPath\Ongoing;
use DreamSoft\Models\ProductionPath\ExternalProduct;
use DreamSoft\Models\User\User;
use DreamSoft\Libs\Debugger;
use DreamSoft\Models\ProductionPath\ExternalData;
use DreamSoft\Models\ProductionPath\OperationOption;
use DreamSoft\Models\PrintShopUser\UserCalcProductAttribute;

class ExternalApi extends Debugger
{
    /**
     * @var UserCalcProductAttribute
     */
    private $UserCalcProductAttribute;
	/**
     * @var ExternalData
     */
    private $ExternalData;
	/**
     * @var OperationOption
     */
    private $OperationOption;
    /**
     * @var DpOrder
     */
    private $DpOrder;
    /**
     * @var DpOrderAddress
     */
    private $DpOrderAddress;
    /**
     * @var DpOrderAddressProduct
     */
    private $DpOrderAddressProduct;
    /**
     * @var User
     */
    private $User;
    /**
     * @var Address
     */
    private $Address;
    /**
     * @var AddressUser
     */
    private $AddressUser;
    /**
     * @var Ongoing
     */
    private $Ongoing;
    /**
     * @var UserCalc
     */
    private $UserCalc;
    /**
     * @var UserCalcProduct
     */
    private $UserCalcProduct;
    /**
     * @var DpProduct
     */
    private $DpProduct;
    /**
     * @var ExternalProduct
     */
    private $ExternalProduct;
    /**
     * @var DevicesController
     */
    private $devicesController;

    public function __construct(DevicesController $devicesController)
    {   
        parent::__construct();
        $this->devicesController = $devicesController;
        $this->DpOrder = DpOrder::getInstance();
        $this->DpOrderAddress = DpOrderAddress::getInstance();
        $this->DpOrderAddressProduct = DpOrderAddressProduct::getInstance();
        $this->User = User::getInstance();
        $this->Address = Address::getInstance();
        $this->AddressUser = AddressUser::getInstance();
        $this->Ongoing = Ongoing::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->ExternalProduct = ExternalProduct::getInstance();
		$this->ExternalData = ExternalData::getInstance();
        $this->OperationOption = OperationOption::getInstance();
        $this->UserCalcProductAttribute = UserCalcProductAttribute::getInstance();
        $this->setDebugName('unidrukApi');
        $this->readOrders();
    }

    private function readOrders()
    {
        $opts = array(
            'http' => array(
                'method' => "GET",
                'header' => "x-api-key: p2lbgWkFrykA4QyUmpHihzmc5BNzIABq\r\n"
            )
        );

        $context = stream_context_create($opts);
        $json = file_get_contents('https://api.unidruk.com.pl/orders?status=production', false, $context);
        if ($json === false) {
            $this->debug('Wrong response from unidruk orders');
            return;
        }
        $json = json_decode($json);
        //$json->data = [$this->getOrder( 78275  ), $this->getOrder( 78276  ), $this->getOrder( 78277  )];//TODO temp
        //{"id":78087,"status":1,"transport":"PERSONAL","status_print":0,"date_receipt":"0000-00-00","date_add":"2021-08-23 07:52:04","date_production":"0000-00-00","customer_description":"","company_description":"","production_description":"","storehouse_description":"","graphic_description":"","other_description":"","products":[{"id":89094,"production":{"CECHY":[{"options-ID":"9","attribute-ID":"7","options-name":"KREDA B\u0141YSK","attribute-name":"rodzaj papieru"},{"options-ID":"57","attribute-ID":"5","options-name":"130","attribute-name":"gramatura"},{"options-ID":"267","attribute-ID":"13","options-name":"Ci\u0119cie przed drukiem","attribute-name":"ci\u0119cie"},{"options-ID":"149","attribute-ID":"3","options-name":"4+0","attribute-name":"druk"},{"options-ID":"271","attribute-ID":"13","options-name":"Ci\u0119cie po druku","attribute-name":"ci\u0119cie"},{"options-ID":"177","attribute-ID":"15","options-name":"r\u0119czne","attribute-name":"pakowanie"}],"OPERACJE":[{"time-id":"0.159444444444444","device-id":"63","format-id":"22","time-name":"time","device name":"Krajarka perfekta 1","format-name":"A2+","quantity-id":"71.95188","operation-id":"143","quantity-name":"quantity","operation name":"Ci\u0119cie przed drukiem"},{"device-id":"15","device name":"KBA Rapida 74","operation-id":"143","operation name":"Ci\u0119cie przed drukiem"},{"device-id":"63","device name":"Krajarka perfekta 1","operation-id":"143","operation name":"Ci\u0119cie przed drukiem"},{"device-id":"123","device name":"pakowanie w papier","operation-id":"143","operation name":"Ci\u0119cie przed drukiem"}],"OPIS PRACY":[{"Workspaces":"A1+","Workspaces-ID":"18"}],"MASZYNY \/ STANOWISKA":[{"machine-ID":"63","machine-name":"Krajarka perfekta 1","average-time-id":"451","average-time-name":"\u015brednia\/h","number-of-people-ID":"1","number-of-people-name":"ile os\u00f3b "},{"machine-ID":"15","machine-name":"KBA Rapida 74","average-time-id":"2318","average-time-name":"\u015brednia\/h","number-of-people-ID":"1","number-of-people-name":"ile os\u00f3b"},{"machine-ID":"63","machine-name":"Krajarka perfekta 1"},{"machine-ID":"123","machine-name":"pakowanie w papier"}]},"print":[{"name":"CI\u0118TE","value":""},{"name":"Szeroko\u015b\u0107 mm","value":"148"},{"name":"Wysoko\u015b\u0107 mm","value":"210"},{"name":"PARAMETRY PRACY","value":""},{"name":"Ilo\u015b\u0107 stron druku","value":"1"},{"name":"Ilo\u015b\u0107 kolor\u00f3w","value":"4"},{"name":"Rodzaj Papieru","value":"KREDA B\u0141YSK"},{"name":"Gramatura papieru","value":"130"},{"name":"Pakowanie ile sztuk w paczce","value":"1000"},{"name":"Termin realizacji ","value":"4 dni"}],"other_data":null,"date_packing_room":null,"date_production":null,"date_create":null,"product_name":"ULOTKI testowe","weight":"404.04","price":"0.00"}],"delivery_address":{"id":80181,"name":"Krzysztof","surname":"Majda","company":"","postalCode":"30-121","address":null,"city":"krak\u00f3w","mobile":"783090000"},"customer":{"id":26617,"margin":null,"discount":null,"transport_free":null,"type":"STANDARD","name":"Krzysztof","surname":"Majda","company":""}}
        foreach ($json->data as $order) {
            if (!$order->products || count($order->products) < 1 || !$order->products[0]->production) {
                continue;
            }
            if (!$this->DpOrder->getOne($order->id)) {//TODO temp !$this->DpOrder->getOne($order->id)
//                $order=$this->getOrder($order->id);
//                $order->products[0]->production=json_decode('[  {"Opispracy":"1"},  {"Cechy":"2"}, {"attribute-ID":"1","attribute-name":"Druk","options-ID":"2","options-name":"Druk4+4"}, {"attribute-ID":"2","attribute-name":"Papier","options-ID":"3","options-name":"Kredabłysk"}, {"attribute-ID":"3","attribute-name":"Foliowanie","options-ID":"2","options-name":"Foliabłysk"}, {"attribute-ID":"4","attribute-name":"Pakowanie","options-ID":"3","options-name":"Paczkipo500szt."}, {"attribute-ID":"5","attribute-name":"Innacecha1","options-ID":"2","options-name":"Brak"}, {"attribute-ID":"6","attribute-name":"Innacecha2","options-ID":"3","options-name":"Brak"},  {"Maszyny/stanowiska":"3"}, {"Device-ID":"15","Device-name":"KBARapida74"}, {"Device-ID":"59","Device-name":"Deltaautomat"}, {"Device-ID":"63","Device-name":"KrajarkaPerfekta1"}, {"Device-ID":"1117","Device-name":"Pakowanie"},  {"Operacje":"4"}, {"Operation-ID":"43","Operation-name":"Cięcieprzeddrukiem","Device-ID":"267","Device-name":"KrajarkaPerfekta1"}, {"Operation-ID":"11","Operation-name":"Drukowanie","Device-ID":"15","Device-name":"KBARapida74"}, {"Operation-ID":"41","Operation-name":"Foliowanie","Device-ID":"59","Device-name":"Deltaautomat"}, {"Operation-ID":"43","Operation-name":"Cięcie","Device-ID":"63","Device-name":"KrajarkaPerfekta1"}, {"Operation-ID":"117","Operation-name":"Pakowanie","Device-ID":"127","Device-name":"Pakowanienawysyłkę"}  ]');

                $user = $this->User->get('externalID', $order->customer->id);
                if (!$user) {
                    $userID = $this->User->create([
                        'externalID' => $order->customer->id,
                        'login' => '',
                        'name' => $order->customer->name,
                        'lastname' => $order->customer->surname,
                        'companyName' => $order->customer->company
                    ]);
                } else {
                    $userID = $user['ID'];
                }
                $address = $this->Address->get('externalID', $order->delivery_address->id);
                if (!$address) {
                    $addressID = $this->Address->create(['externalID' => $order->delivery_address->id,
                        'name' => $order->delivery_address->name,
                        'lastname' => $order->delivery_address->surname,
                        'companyName' => $order->delivery_address->company,
                        'zipcode' => $order->delivery_address->postalCode,
                        'city' => $order->delivery_address->city,
                        'street' => '',
                        'house' => ''
                    ]);
                } else {
                    $addressID = $address['ID'];
                }
                $addressUser = $this->AddressUser->getOne($userID);
                if (!$addressUser) {
                    $this->AddressUser->create(['userID' => $userID, 'addressID' => $addressID, 'type' => 1]);
                }
                $this->Address->setDefault($addressID, $userID);
                $orderID = $order->id;
                $this->DpOrder->create(['ID' => $orderID, 'userID' => $userID, 'production' => 1, 'ready' => 1]);
                $orderAddressID = $this->DpOrderAddress->create([
                    'orderID' => $orderID,
                    'addressID' => $addressID
                ]);
                foreach ($order->products as $product) {
                    //$externalProduct=$this->ExternalProduct->get('externalID',$product->id);
                    $workspaceDescription = $this->extractArray($product, 'OPIS PRACY');
                    if (!$workspaceDescription) {
                        break;
                    }
                    $externalProduct = null;$formatID=null;
                    $customFormatSize = NULL;
                    foreach ($workspaceDescription as $wd) {
                        if ($wd->{'type-id'} && $wd->{'group-ID'}) {
                            $externalProduct = ['groupID' => $wd->{'group-ID'}, 'typeID' => $wd->{'type-id'}];
                        }else if($wd->{'products-format-ID'}){
                            $formatID=$wd->{'products-format-ID'};
                            if($formatID == 13){//TODO: If is custom format
                                $customFormatSize = $wd->{'comments'};
                            }
                        }
                    }
                    if (!$externalProduct) {
                        $this->debug('missing product id',[ 'orderID'=>$orderID, 'product' => $product]);
                        break;
                    }
                    $workspaceID = $workspaceDescription[0]->{'Workspaces-ID'};
                    $userCalcID = $this->UserCalc->create([
                        'baseID' => 0,
                        'ver' => 0,
                        'groupID' => $externalProduct['groupID'],
                        'typeID' => $externalProduct['typeID'],
                        'volume' => 0,
                        'amount' => 0,
                        'calcPriceID' => 0,
                        'priceID' => 0,
                    ]);

                    $customFormatWidth = NULL;
                    $customFormatHeight = NULL;
                    if($customFormatSize != NULL){
                        $formatSize = explode("x", $customFormatSize);
                        if(sizeof($formatSize) > 1){
                            $customFormatWidth = $this->parseIntField($formatSize[0]);
                            $customFormatHeight = $this->parseIntField($formatSize[1]);
                        }
                    }
                    $userCalcProductID = $this->UserCalcProduct->create([
                        'calcID' => $userCalcID,
                        'groupID' => $externalProduct['groupID'],
                        'typeID' => $externalProduct['typeID'],
                        'formatID' => $formatID,
                        'formatWidth' => $customFormatWidth,
                        'formatHeight' => $customFormatHeight,
                        'pages' => 0,
                        'printTypeID' => 0,
                        'workspaceID' => $workspaceID,
                        'numberOfSquareMeters' => 0,
                    ]);
                    if(!$userCalcProductID){
                        $this->debug('missing $userCalcProductID',['orderID'=>$orderID,'productID' => $product->id ]);
                    }
					$options = $this->extractArray($product, 'CECHY');
                    $productID = $this->DpProduct->create(['calcID' => $userCalcID, 'orderID' => $orderID]);
                    $this->DpOrderAddressProduct->create(['orderAddressID' => $orderAddressID, 'productID' => $productID]);
                    $operations = $this->extractArray($product, 'OPERACJE');
                    $order = 1;
                    $inProgressFirst = 1;
                    foreach ($operations as $operation) {
                        $deviceId=$this->parseIntField($operation->{'device-id'});
                        $operationID=$this->parseIntField($operation->{'operation-id'});
                        $estimatedTime=$this->parseIntField($operation->{'time'});
						$unit=$operation->{'unit'};
                        $quantity=$this->parseIntField($operation->{'quantity'});
                        if (!$deviceId || !$operationID) {
                            $this->debug('missing fields in operation',['orderID'=>$orderID,'productID' => $product->id, 'operation' => $operation ]);
                        } else {
							$deviceOrder = $this->Ongoing->getMaxDeviceOrder($deviceId);
                            $deviceOrder++;
                            $this->Ongoing->create(['state' => 0,
                                'itemID' => $userCalcProductID,
                                'operatorID' => null,
                                'operationID' => $operationID,
                                'deviceID' => $deviceId,
                                'order' => $order++,
								'orderOnDevice' => $deviceOrder,
                                'finished' => 0,
                                'processID' => 0,
                                'sheetNumber' => 0,
                                'processSideType' => 0,
                                'inProgress' => $inProgressFirst,
                                'appVersion' => 1,
                                'estimatedTime' => $estimatedTime]);
							$optionID = false;
                            $attributeID = false;    
                            foreach ($options as $option) {
                                $optionsID = $this->parseIntField($option->{'options-ID'});
                                if($this->OperationOption->exist($optionsID, $operationID)){
                                    $optionID = $this->parseIntField($option->{'options-ID'});
                                    $attributeID = $this->parseIntField($option->{'attribute-ID'});
                                }
                            }
                            
                            if($optionID && $optionID > 0 && $attributeID && $attributeID > 0){
								$this->ExternalData->create([
									'orderID' => $this->parseIntField($orderID),
									'deviceID' => $deviceId,
									'unit' => $unit,
									'quantity' => $quantity,
									'optionID' => $optionID,
									'attributeID' => $attributeID
								]);
                            }
							
                            if ($inProgressFirst) {
                                $inProgressFirst = 0;
                            }
                        }
                    }
                    //
                    foreach ($options as $option) {
                        $optionID = $this->parseIntField($option->{'options-ID'});
                        $attributeID = $this->parseIntField($option->{'attribute-ID'});
                        if($optionID && $optionID > 0 && $attributeID && $attributeID > 0){
                            $this->UserCalcProductAttribute->create([
                                'calcProductID' => $userCalcProductID,
                                'attrID' => $attributeID,
                                'optID' => $optionID,
                                //'attrPages' => $userCalcProductID,
                                'controllerID' => 0
                            ]);
                        }
                    }
                    //
                    $devices = $this->extractArray($product, 'MASZYNY / STANOWISKA');
                    foreach ($devices as $device) {

                    }
                }


            }
        }
    }

    private function getOrder($id)
    {
        $opts = array(
            'http' => array(
                'method' => "GET",
                'header' => "x-api-key: p2lbgWkFrykA4QyUmpHihzmc5BNzIABq\r\n"
            )
        );

        $context = stream_context_create($opts);
        $json = file_get_contents('https://api.unidruk.com.pl/orders/' . $id, false, $context);
        if ($json === false) {
            $this->debug('Wrong response from unidruk::order');
            return null;
        }
        $json = json_decode($json);
        return $json;
    }

    private function extractArray($product, string $name)
    {
        if ($product->production && $product->production->$name) {
            return $product->production->$name;
        }
        return [];
    }

    private function parseIntField($likeInt)
    {
        $likeInt=trim($likeInt);
        return $likeInt?intval($likeInt):null;
    }
}
