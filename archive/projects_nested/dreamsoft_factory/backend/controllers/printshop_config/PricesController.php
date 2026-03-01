<?php

use DreamSoft\Controllers\Components\Price;
use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigDiscountPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOption;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionLang;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPaperPrice;
use DreamSoft\Controllers\Components\ExportImport;
use DreamSoft\Controllers\Components\Uploader;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionDescription;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttribute;

/**
 * Description of PricesController
 *
 * @author Rafał
 */

class PricesController extends Controller
{

    public $useModels = array();

	/**
     * @var PrintShopConfigOptionDescription
     */
    private $PrintShopConfigOptionDescription;
    /**
     * @var PrintShopConfigAttribute
     */
    private $PrintShopConfigAttribute;
	/**
     * @var Uploader
     */
    protected $Uploader;
    /**
     * @var ExportImport
     */
    protected $ExportImport;
    /**
     * @var PrintShopConfigPaperPrice
     */
    protected $PrintShopConfigPaperPrice;
    /**
     * @var PrintShopConfigOption
     */
    protected $PrintShopConfigOption;
    /**
     * @var PrintShopConfigOptionLang
     */
    protected $PrintShopConfigOptionLang;
    /**
     * @var PrintShopConfigPrice
     */
    protected $PrintShopConfigPrice;
    /**
     * @var PrintShopConfigDiscountPrice
     */
    protected $PrintShopConfigDiscountPrice;
    /**
     * @var Price
     */
    protected $Price;
    /**
     * @var Spreadsheet_Excel_Writer
     */
    protected $Workbook;
    /**
     * @var string
     */
    protected $filename;

    /**
     * PricesController constructor.
     * @param array $params
     */
    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopConfigPrice = PrintShopConfigPrice::getInstance();
        $this->PrintShopConfigDiscountPrice = PrintShopConfigDiscountPrice::getInstance();
        $this->Price = Price::getInstance();
        $this->filename = BASE_DIR . '/logs/export.xls';
        $this->Workbook = new Spreadsheet_Excel_Writer($this->filename);
		$this->Uploader = Uploader::getInstance();
		$this->PrintShopConfigOption = PrintShopConfigOption::getInstance();
		$this->PrintShopConfigOptionLang = PrintShopConfigOptionLang::getInstance();
		$this->PrintShopConfigPaperPrice = PrintShopConfigPaperPrice::getInstance();
		$this->ExportImport = ExportImport::getInstance();
		$this->PrintShopConfigOptionDescription = PrintShopConfigOptionDescription::getInstance();
        $this->PrintShopConfigAttribute = PrintShopConfigAttribute::getInstance();
    }

    /**
     * @param $attrID
     * @param $optID
     * @param $controllerID
     * @return array|bool
     */
    public function prices($attrID, $optID, $controllerID)
    {

        $this->PrintShopConfigPrice->setAttrID($attrID);
        $this->PrintShopConfigPrice->setOptID($optID);
        $this->PrintShopConfigPrice->setControllerID($controllerID);

        $result = $this->PrintShopConfigPrice->getAll();
        if (!$result) {
            $result = array();
        } else {
            $res = array();
            if (!empty($result)) {
                foreach ($result as $r) {
                    $actExpense = $r['expense'] ? $this->Price->getNumberToView($r['expense']) : NULL;
                    $res[$r['priceType']][] = array(
                        'priceType' => $r['priceType'],
                        'amount' => $r['amount'],
                        'value' => $this->Price->getNumberToView($r['value']),
                        'expense' => $actExpense,
                        'ID' => $r['ID']
                    );
                }
            }
            sort($res);
            $result = $res;
        }
        return $result;
    }

    /**
     * @param $attrID
     * @param $optID
     * @param $controllerID
     * @param $discountGroupID
     * @return array|bool
     */
    public function discountPrices($attrID, $optID, $controllerID, $discountGroupID)
    {
        $this->PrintShopConfigDiscountPrice->setAttrID($attrID);
        $this->PrintShopConfigDiscountPrice->setOptID($optID);
        $this->PrintShopConfigDiscountPrice->setControllerID($controllerID);
        $this->PrintShopConfigDiscountPrice->setDiscountGroupID($discountGroupID);

        $result = $this->PrintShopConfigDiscountPrice->getAll();
        if (!$result) {
            $result = array();
        } else {
            $res = array();
            if (!empty($result)) {
                foreach ($result as $r) {
                    $actExpense = $r['expense'] ? $this->Price->getNumberToView($r['expense']) : NULL;
                    $res[$r['priceType']][] = array(
                        'priceType' => $r['priceType'],
                        'amount' => $r['amount'],
                        'value' => $this->Price->getNumberToView($r['value']),
                        'expense' => $actExpense,
                        'ID' => $r['ID']
                    );
                }
            }
            sort($res);
            $result = $res;
        }
        return $result;
    }

    /**
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @return array
     */
    public function patch_prices($attributeID, $optionID, $controllerID)
    {

        $this->PrintShopConfigPrice->setControllerID($controllerID);
        $this->PrintShopConfigPrice->setAttrID($attributeID);
        $this->PrintShopConfigPrice->setOptID($optionID);

        $this->PrintShopConfigDiscountPrice->setControllerID($controllerID);
        $this->PrintShopConfigDiscountPrice->setAttrID($attributeID);
        $this->PrintShopConfigDiscountPrice->setOptID($optionID);

        $remove = $this->Data->getPost('remove');
        $discountGroupID = $this->Data->getPost('discountGroupID');

        if ($discountGroupID > 0) {
            $this->PrintShopConfigDiscountPrice->setDiscountGroupID($discountGroupID);
        }

        $post = $this->Data->getAllPost();

        if ($remove) {
            if ($discountGroupID > 0) {
                $res = $this->PrintShopConfigDiscountPrice->delete('ID', $remove);
            } else {
                $res = $this->PrintShopConfigPrice->delete('ID', $remove);
            }
            return array('response' => $res, 'info' => 'remove');
        }
        if ($post['amount'] !== NULL && $post['value'] !== NULL && $post['priceType']) {

            if( $post['amount'] > 0 ) {
                $post['amount'] = str_replace(',', '.', $post['amount']);
            }

            if ($discountGroupID > 0) {
                $data = $this->updateDiscountPrice($post);
            } else {
                $data = $this->updatePrice($post);
            }

        } else {
            $data['response'] = false;
        }
        return $data;
    }

    /**
     * @param $post
     * @return array
     */
    private function updatePrice($post)
    {
        $value = $post['value'];
        $expense = NULL;
        if( array_key_exists('expense', $post) ) {
            $expense = $post['expense'];
        }
        $amount = $post['amount'];
        $priceType = $post['priceType'];

        $value = $this->Price->getPriceToDb($value);

        $data['response'] = false;

        if ($expense !== NULL && strlen($expense) > 0) {
            $expense = $this->Price->getPriceToDb($expense);
        }

        $ID = $this->PrintShopConfigPrice->exist($amount, $priceType);
        if (intval($ID) > 0) {
            $data['response'] = $this->PrintShopConfigPrice->update($ID, $value, $expense);
            $data['info'] = 'update';
            $data['item'] = $this->PrintShopConfigPrice->getOne($ID);
            $data['item'] = $this->prepareValueToView($data['item']);
            $data['item'] = $this->prepareExpenseToView($data['item']);
            return $data;
        } else {
            $ID = $this->PrintShopConfigPrice->customCreate(
                $amount,
                $value,
                $priceType,
                $expense
            );
        }

        if ($ID > 0) {
            $data = $this->PrintShopConfigPrice->customGet($priceType, $amount);
            if (isset($data['value'])) {
                $data['value'] = $this->Price->getNumberToView($data['value']);
            }
            if (isset($data['expense'])) {
                $data['expense'] = ($data['expense'] !== NULL) ? $this->Price->getNumberToView($data['expense']) : NULL;
            }
        } else {
            $data['response'] = false;
        }

        return $data;
    }

    /**
     * @param $post
     * @return bool
     */
    private function updateDiscountPrice($post)
    {
        $value = $post['value'];
        $expense = $post['expense'];
        $amount = $post['amount'];
        $priceType = $post['priceType'];

        $value = $this->Price->getPriceToDb($value);

        $data['response'] = false;

        if ($expense !== NULL && strlen($expense) > 0) {
            $expense = $this->Price->getPriceToDb($expense);
        }

        $ID = $this->PrintShopConfigDiscountPrice->exist($amount, $priceType);
        if (intval($ID) > 0) {
            $data['response'] = $this->PrintShopConfigDiscountPrice->update($ID, $value, $expense);
            $data['info'] = 'update';
            $data['item'] = $this->PrintShopConfigDiscountPrice->getOne($ID);
            $data['item'] = $this->prepareValueToView($data['item']);
            $data['item'] = $this->prepareExpenseToView($data['item']);
            return $data;
        } else {
            $ID = $this->PrintShopConfigDiscountPrice->customCreate($amount, $value, $priceType, $expense);
        }

        if ($ID > 0) {
            $data = $this->PrintShopConfigDiscountPrice->getOne($ID);
            if (isset($data['value'])) {
                $data['value'] = $this->Price->getNumberToView($data['value']);
            }
            if (isset($data['expense'])) {
                $data['expense'] = ($data['expense'] !== NULL) ? $this->Price->getNumberToView($data['expense']) : NULL;
            }
        } else {
            $data['response'] = false;
        }

        return $data;
    }

    public function priceTypes($ID = NULL)
    {

        if (intval($ID) > 0) {
            $data = $this->PrintShopConfigPrice->getPriceType($ID);
        } else {
            $data = $this->PrintShopConfigPrice->getPriceTypes();
        }
        if (empty($data)) {
            $data = array();
        }
        return $data;

    }
	
	//@TODO: optimize
	public function post_price_exporter()
	{
        $allPost = $this->Data->getAllPost();
        $attributeID = $this->Data->getPost('attributeID');
        $exportType = $this->Data->getPost('exportType');
        $domainID = $this->Data->getPost('domainID');

        $attribute = $this->PrintShopConfigAttribute->customGet($attributeID);
        $this->PrintShopConfigOptionDescription->setAttrID($attributeID);

        if ($attributeID > 0) {
            $this->PrintShopConfigOption->setAttrID($attributeID);
        }else{
            return array('response' => false, 'data' => 'Incorrect attributeID');
        }

        $data = $this->PrintShopConfigOption->getAll();
        if(sizeof($data) <= 0)
            return array('response' => false, 'data' => 'Incorrect attributeID');

        //getting prices for each product
        $newData = [];
        foreach($data as $singleOption){
            $optID = $singleOption['ID'];
            $this->PrintShopConfigPaperPrice->setOptID($optID);
            $pricesData = $this->PrintShopConfigPaperPrice->getAll();
            if (empty($pricesData)) {
                $pricesData = array();
            } else {
                foreach ($pricesData as $key => &$value) {
                    $value['price'] = $this->Price->getNumberToView($value['price']);
                    if ($value['expense']) {
                        $value['expense'] = $this->Price->getNumberToView($value['expense']);
                    }else{
                        $value['expense'] = "";
                    }
                }
            }
            $tmp = $singleOption;
            $tmp['kilosPrice'] = $pricesData;
            $newData[] = $tmp;
        }
        $data = $newData;

        //get kilos range
        $kilosRange = array();
        foreach($data as $singleOption){
            foreach($singleOption['kilosPrice'] as $singleKiloData){
                array_push($kilosRange, $singleKiloData['amount']);
            }
        }
        $kilosRange = array_unique($kilosRange);
        array_multisort($kilosRange);

        // prepare header
        $exportSingleHead['attrID'] = 'attrID';
        $exportSingleHead['ID'] = 'optID';
        $exportSingleHead['name'] = 'name';
        $exportSingleHead['thickness'] = 'thickness';
        //// descriptions
        $this->PrintShopConfigOptionDescription->setOptID($data[0]['ID']);
        $descriptionArray = $this->PrintShopConfigOptionDescription->customGetAll($attribute['function'], $domainID);
        foreach($descriptionArray as $singleDescriptionArray){
            $exportSingleHead[$singleDescriptionArray['name']] = $singleDescriptionArray['name'].'(ID:'.$singleDescriptionArray['ID'].')';
        }
        ////range kilos
        foreach($kilosRange as $singleKiloRange){
            $exportSingleHead['range'.$singleKiloRange] = $singleKiloRange." kg";
        }
        foreach($kilosRange as $singleKiloRange){
            $exportSingleHead['expense'.$singleKiloRange] = $singleKiloRange." kg koszt";
        }

        // export
        $exportData = array(); 
        array_push($exportData, $exportSingleHead);
        foreach($data as $singleOption){
            $exportSingle['attrID'] = $singleOption['attrID'];
            $exportSingle['ID'] = $singleOption['ID'];
            $exportSingle['name'] = $singleOption['name'];
            $exportSingle['thickness'] = $singleOption['sizePage'];
            //desriptions
            $this->PrintShopConfigOptionDescription->setOptID($singleOption['ID']);
            $descriptionArray = $this->PrintShopConfigOptionDescription->customGetAll($attribute['function'], $domainID);
            foreach($descriptionArray as $singleDescriptionArray){
                if(array_key_exists('value', $singleDescriptionArray) && $singleDescriptionArray['value'] != null){
                    $exportSingle[$singleDescriptionArray['name']] = $singleDescriptionArray['value'];
                }else{
                    $exportSingle[$singleDescriptionArray['name']] = "";
                }
            }
            //range kilos prices
            foreach($kilosRange as $singleKiloRange){
                $exportSingle['range'.$singleKiloRange] = "";
            }
            foreach($singleOption['kilosPrice'] as $singleKiloData){
                $exportSingle['range'.$singleKiloData['amount']] = $singleKiloData['price'];
            }
            foreach($kilosRange as $singleKiloRange){
                $exportSingle['expense'.$singleKiloRange] = "";
            }
            foreach($singleOption['kilosPrice'] as $singleKiloData){
                $exportSingle['expense'.$singleKiloData['amount']] = $singleKiloData['expense'];
            }
            
            array_push($exportData, $exportSingle);
        }

        // exporting $exportData to file and downloadable element
        $dir = companyID . '/download/';
        if (!is_dir(STATIC_PATH . $dir)) {
            mkdir(STATIC_PATH . $dir, 0777, true);
        }
        $path = $dir . 'price__' . date('Y-m-d_G-i') . '.xls';
        $this->getExportImport()->newSheet('Prices');
        $this->getExportImport()->setFromArray($exportData);
        $this->getExportImport()->path = STATIC_PATH . $path;
        $this->getExportImport()->saveFile();
		
        return array('response' => true, 'url' => STATIC_URL . $path);
    }
	
    public function post_price_importer(){
        
        $path = $this->Uploader->uploadTemporary('file');
        if ($path) {
            $data = $this->importPrices($path);
        } else {
            $data['response'] = false;
        }
        $this->Uploader->removeTemporary($path);
        return $data;
    }
	
	//@TODO: optimize
    private function importPrices(string $path)
    {
        if (!$this->getExportImport()->openFile($path, 0)) {
            return array('response' => false, 'data' => 'Error reading file');
        }

        $dataArray = $this->getExportImport()->sheetToArray();
        $importType = $this->Data->getPost('importType');
        $domainID = $this->Data->getPost('domainID');
        if ($importType != "kilos") {
            return array('response' => false, 'data' => 'Not supported import type');
        }
        if (sizeof($dataArray) <= 1) {
            return array('response' => false, 'data' => 'Nothing to import');
        }

        $createCount = 0;
        $attributeID = intval($dataArray[2]['A']);

        $headerRow = $dataArray[1];
        $descriptionRowIDs = [];
        $descriptionCount = 0;
        foreach($headerRow as $head){
            if (str_contains($head, '(ID:')) { 
                $descriptionCount++;
                $descriptionRowIDs[] = intval(explode(')', explode('(ID:', $head)[1])[0]);
            }
        }

        // rangeArray
        $rangeArray = array_slice($headerRow, (4+$descriptionCount));
        $rangeArray = array_slice($rangeArray, 0, (sizeof($rangeArray)/2));
        $newArrayRange = array();
        foreach($rangeArray as $singleRangeArray){
            $tmp = str_replace(" kg", "", $singleRangeArray);
            array_push($newArrayRange, $tmp);
        }
        $rangeArray = $newArrayRange;

        $importData = array_slice($dataArray, 1, sizeof($dataArray) - 1, true);
        foreach ($importData as $dataRow) {
            $isUpdated = false;
            $optionID = intval($dataRow['B']);
            $this->PrintShopConfigOption->updateAll($optionID,['sizePage' => $dataRow['D']]);
            $descriptionRow = array_values(array_slice($dataRow, 4, $descriptionCount));
            $insert = [];
            $index = 0;
            //descriptions
            foreach ($descriptionRow as $description) {
                $tmp = [];
                $tmp['optionDescriptionTypeID'] = $descriptionRowIDs[$index];
                $tmp['value'] = $description;
                $tmp['attributeID'] = $attributeID;
                $tmp['optionID'] = $optionID;
                $tmp['domainID'] = $domainID;
                $insert[] = $tmp;
                $index++;
            }
            $this->PrintShopConfigOptionDescription->removeAllDescriptionsForOption($attributeID, $domainID, $optionID);
            if($this->PrintShopConfigOptionDescription->batchInsert($insert)){
                $isUpdated = true;
            }

            //prices
            $this->PrintShopConfigPaperPrice->setOptID($optionID);
            $pricesData = $this->PrintShopConfigPaperPrice->getAll();
            ///delete
            foreach($pricesData as $singlePriceData){
                $this->PrintShopConfigPaperPrice->delete('ID', $singlePriceData['ID']);
            }
            ////add new
            $element = 0;
            foreach($rangeArray as $singleRangeArray){
                $amount = $singleRangeArray;
                $price = $this->Price->getPriceToDb(array_values($dataRow)[(4+$descriptionCount+$element)]);
                $expense = $this->Price->getPriceToDb(array_values($dataRow)[(4+$descriptionCount+$element+(sizeof($rangeArray)))]);
                if($price != "" && $price != null && $price != 0){
                    $this->PrintShopConfigPaperPrice->customCreate($price, $expense, $amount);
                }
                $element++;
            }
            if($isUpdated == true){
                $createCount++;
            }
        }

        if (sizeof($importData) != $createCount) {
            return array('response' => false, 'data' => (sizeof($dataArray) - 1 - $createCount).' rows not updated');
        }

        return array('response' => true, 'updated' => $createCount);
    }
	
    protected function getExportImport()
    {
        return $this->ExportImport;
    }

    /**
     * @TODO remove if not in use
     * @deprecated since 11.08.2017
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @param null $docType
     * @return array
     */
    public function export($attributeID, $optionID, $controllerID, $docType = NULL)
    {

        $this->PrintShopConfigPrice->setAttrID($attributeID);
        $this->PrintShopConfigPrice->setOptID($optionID);
        $this->PrintShopConfigPrice->setControllerID($controllerID);

        $result = $this->PrintShopConfigPrice->getAll();
        if (!$result) {
            $result = array();
        } else {
            $res = array();
            if (!empty($result)) {
                $res[] = array('Ilość (przedział)', 'Cena jednostkowa', 'Koszt jednostkowy');
                foreach ($result as $r) {
                    $res[] = array(
                        //'priceType' => $r['priceType'],
                        'amount' => $r['amount'],
                        'value' => $this->Price->getNumberToView($r['value']),
                        'expense' => $this->Price->getNumberToView($r['expense']),
                        //'ID' => $r['ID'] 
                    );
                }
            }
            sort($res);
            $result = $res;
        }

        if ($docType == 'csv') {
            // csv
            $fp = fopen(BASE_DIR . 'logs/export.csv', 'w');
            foreach ($res as $r) {
                fputcsv($fp, $r);
            }
            fclose($fp);
        } elseif ($docType == 'xls') {
            // xls
            $worksheet =& $this->Workbook->addWorksheet('arkusz1');
            $worksheet->setInputEncoding('utf-8');

            $i = 0;
            foreach ($res as $row) {
                if ($i == 0) {
                    $worksheet->write($i, 0, $row[0]);
                    $worksheet->write($i, 1, $row[1]);
                    $worksheet->write($i, 2, $row[2]);
                    $i++;
                    continue;
                }
                $worksheet->write($i, 0, $row['amount']);
                $worksheet->write($i, 1, $row['value']);
                $worksheet->write($i, 2, $row['expense']);
                $i++;
            }

            $this->Workbook->close();
            //$this->Workbook->send();

            //$this->Workbook->send($this->filename);

//            $handle = fopen($this->filename, "r+");
//            $data = fread($handle, filesize($this->filename));
//            fclose($handle);

            //$data = file_get_contents($this->filename);
            $finfo = finfo_open(FILEINFO_MIME_TYPE); // return mime type ala mimetype extension
            $fileInfo = finfo_file($finfo, $this->filename);
            finfo_close($finfo);
        }

        $data = null;
        $mime = null;

        return array('response' => true, 'data' => $data, 'mime' => $mime);
    }

    /**
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @return array
     */
    public function post_importPriceList($attributeID, $optionID, $controllerID)
    {
        $priceType = $this->Data->getPost('priceType');
        $discountGroupID = $this->Data->getPost('discountGroupID');

        if ($discountGroupID > 0) {
            $items = $this->discountImport($attributeID, $optionID, $controllerID, $priceType, $discountGroupID);
        } else {
            $items = $this->import($attributeID, $optionID, $controllerID, $priceType);
        }

        $response = false;
        if ($items) {
            $response = true;
        }

        return array('response' => $response, 'items' => $items);
    }

    /**
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @param $priceType
     * @return array|bool
     */
    private function import($attributeID, $optionID, $controllerID, $priceType)
    {
        $this->PrintShopConfigPrice->setControllerID($controllerID);
        $this->PrintShopConfigPrice->setAttrID($attributeID);
        $this->PrintShopConfigPrice->setOptID($optionID);

        if (intval($priceType) == 0) {
            return array('response' => false);
        }

        $this->PrintShopConfigPrice->removeAll($priceType);

        $file = current($_FILES);

        $items = array();

        $row = 0;
        if (($handle = fopen($file['tmp_name'], "r")) !== FALSE) {
            while (($data = fgetcsv($handle, 0, ";")) !== FALSE) {

                $num = count($data);
                $row++;
                for ($c = 0; $c < $num; $c++) {
                    $this->debug($data[$c]);
                    $expense = NULL;
                    if ($c == 0) {
                        $amount = $data[$c];
                        $ID = $this->PrintShopConfigPrice->exist($amount, $priceType);
                    }
                    if ($c == 1) {
                        $value = $this->Price->getPriceToDb($data[$c]);
                    }
                    if ($c == 2 && $data[$c] !== NULL) {
                        $expense = $this->Price->getPriceToDb($data[$c]);
                    }
                }
                if (isset($ID) && intval($ID) > 0) {
                    $this->PrintShopConfigPrice->update($ID, $value, $expense);
                    $action = 'update';
                } else {
                    $ID = $this->PrintShopConfigPrice->customCreate(
                        $amount,
                        $value,
                        $priceType,
                        $expense
                    );
                    $action = 'save';
                }
                $one['item'] = $this->PrintShopConfigPrice->getOne($ID);
                $one['info'] = $action;
                $items[] = $one;
            }
        }
        fclose($handle);

        if (!empty($items)) {
            return $items;
        }

        return false;
    }

    /**
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @param $priceType
     * @param $discountGroupID
     * @return array|bool
     */
    private function discountImport($attributeID, $optionID, $controllerID, $priceType, $discountGroupID)
    {
        $this->PrintShopConfigDiscountPrice->setControllerID($controllerID);
        $this->PrintShopConfigDiscountPrice->setAttrID($attributeID);
        $this->PrintShopConfigDiscountPrice->setOptID($optionID);
        $this->PrintShopConfigDiscountPrice->setDiscountGroupID($discountGroupID);

        if (intval($priceType) == 0) {
            return array('response' => false);
        }

        $this->PrintShopConfigDiscountPrice->removeAll($priceType);

        $file = current($_FILES);

        $items = array();

        $row = 0;
        if (($handle = fopen($file['tmp_name'], "r")) !== FALSE) {
            while (($data = fgetcsv($handle, 0, ";")) !== FALSE) {
                $num = count($data);
                $row++;
                for ($c = 0; $c < $num; $c++) {
                    $expense = NULL;
                    if ($c == 0) {
                        $amount = $data[$c];
                        $ID = $this->PrintShopConfigDiscountPrice->exist($amount, $priceType);
                    }
                    if ($c == 1) {
                        $value = $this->Price->getPriceToDb($data[$c]);
                    }
                    if ($c == 2 && $data[$c] !== NULL) {
                        $expense = $this->Price->getPriceToDb($data[$c]);
                    }
                }
                if (intval($ID) > 0) {
                    $this->PrintShopConfigDiscountPrice->update($ID, $value, $expense);
                    $action = 'update';
                } else {
                    $ID = $this->PrintShopConfigDiscountPrice->customCreate($amount, $value, $priceType, $expense);
                    $action = 'save';
                }
                $one['item'] = $this->PrintShopConfigDiscountPrice->getOne($ID);
                $one['info'] = $action;
                $items[] = $one;
            }
        }
        fclose($handle);

        if (!empty($items)) {
            return $items;
        }

        return false;
    }

    /**
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @param $priceType
     * @return array
     */
    public function delete_removeAll($attributeID, $optionID, $controllerID, $priceType)
    {
        return $this->removeAll($attributeID, $optionID, $controllerID, $priceType);
    }

    /**
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @param $priceType
     * @param $discountGroupID
     * @return array
     */
    public function delete_allDiscount($attributeID, $optionID, $controllerID, $priceType, $discountGroupID)
    {
        return $this->removeAllDiscount($attributeID, $optionID, $controllerID, $priceType, $discountGroupID);
    }

    /**
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @param $priceType
     * @return array
     */
    private function removeAll($attributeID, $optionID, $controllerID, $priceType)
    {
        $data['response'] = false;

        $this->PrintShopConfigPrice->setControllerID($controllerID);
        $this->PrintShopConfigPrice->setAttrID($attributeID);
        $this->PrintShopConfigPrice->setOptID($optionID);


        if (intval($priceType) == 0) {
            return array('response' => false);
        }

        $response = $this->PrintShopConfigPrice->removeAll($priceType);

        return array('response' => $response);
    }

    /**
     * @param $attributeID
     * @param $optionID
     * @param $controllerID
     * @param $priceType
     * @param $discountGroupID
     * @return array
     */
    private function removeAllDiscount($attributeID, $optionID, $controllerID, $priceType, $discountGroupID)
    {
        $data['response'] = false;

        $this->PrintShopConfigDiscountPrice->setControllerID($controllerID);
        $this->PrintShopConfigDiscountPrice->setAttrID($attributeID);
        $this->PrintShopConfigDiscountPrice->setOptID($optionID);
        $this->PrintShopConfigDiscountPrice->setDiscountGroupID($discountGroupID);


        if (intval($priceType) == 0) {
            return array('response' => false);
        }

        $response = $this->PrintShopConfigDiscountPrice->removeAll($priceType);

        return array('response' => $response);
    }

    /**
     * @param $item
     * @return array
     */
    private function prepareValueToView($item)
    {
        if ( array_key_exists('value', $item) ) {
            $item['value'] = $this->Price->getNumberToView($item['value']);
        }

        return $item;
    }

    /**
     * @param $item
     * @return array
     */
    private function prepareExpenseToView($item)
    {
        if ( array_key_exists('expense', $item) ) {
            $item['expense'] = ($item['expense'] !== NULL) ? $this->Price->getNumberToView($item['expense']) : NULL;
        }

        return $item;
    }
}
