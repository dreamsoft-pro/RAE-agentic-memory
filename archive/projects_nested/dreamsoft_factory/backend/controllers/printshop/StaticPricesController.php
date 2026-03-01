<?php

use DreamSoft\Controllers\Components\Price;
use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigExclusion;
use DreamSoft\Models\PrintShopProduct\PrintShopOption;
use DreamSoft\Models\PrintShopProduct\PrintShopPage;
use DreamSoft\Models\PrintShopProduct\PrintShopStaticPrice;
use DreamSoft\Models\PrintShopProduct\PrintShopVolume;
use DreamSoft\Controllers\Components\Standard;

class StaticPricesController extends Controller
{
    public $useModels = array();

    protected $PrintShopStaticPrice;
    protected $PrintShopConfigExclusion;
    protected $Price;
    protected $PrintShopVolume;
    protected $PrintShopOption;
    protected $PrintShopPage;
    private $Standard;
    protected $ExcelReader;
    protected $ExcelWriter;
    protected $ExcelFile;
    public $sheetIndex = 0;
    protected $filename;
    protected $path;
    private $limit = 15000;
    private $actualIndex = 0;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopStaticPrice = PrintShopStaticPrice::getInstance();
        $this->PrintShopConfigExclusion = PrintShopConfigExclusion::getInstance();
        $this->PrintShopVolume = PrintShopVolume::getInstance();
        $this->PrintShopOption = PrintShopOption::getInstance();
        $this->PrintShopPage = PrintShopPage::getInstance();
        $this->Standard = Standard::getInstance();
        $this->Price = Price::getInstance();
        $this->path = STATIC_PATH . companyID . '/tmp/export/export.xls';
    }

    public function getLimit()
    {
        return $this->limit;
    }

    public function setLimit($limit)
    {
        $this->limit = $limit;
    }

    public function getActualIndex()
    {
        return $this->actualIndex;
    }

    public function setActualIndex($actualIndex)
    {
        $this->actualIndex = $actualIndex;
    }

    public function staticprices($groupID, $typeID, $formatID)
    {
        $this->PrintShopStaticPrice->setGroupID($groupID);
        $this->PrintShopStaticPrice->setTypeID($typeID);
        $this->PrintShopStaticPrice->setFormatID($formatID);

        $data = $this->PrintShopStaticPrice->getAll();

        if (!empty($data)) {
            foreach ($data as $key => $value) {
                $data[$key]['price'] = $this->Price->getNumberToView($value['price']);
                if ($value['expense']) {
                    $data[$key]['expense'] = $this->Price->getNumberToView($value['expense']);
                }
            }
        } else {
            $data = array();
        }

        return $data;
    }

    public function patch_staticprices($groupID, $typeID, $formatID)
    {
        $data['response'] = false;
        $options = $this->Data->getPost('options');
        $price = $this->Data->getPost('price');
        $expense = $this->Data->getPost('expense');

        $this->PrintShopStaticPrice->setGroupID($groupID);
        $this->PrintShopStaticPrice->setTypeID($typeID);
        $this->PrintShopStaticPrice->setFormatID($formatID);

        $options = json_decode($options, true);
        uksort($options, array($this->Standard, 'sortLikeJs'));
        $options = json_encode($options);

        if (!strlen($price) && $expense === null) {
            if ($this->PrintShopStaticPrice->customDelete($options)) {
                $data['response'] = true;
                $data['info'] = 'Deleted';
            }
            return $data;
        }

        if ($price !== null) {
            $price = $this->Price->getPriceToDb($price);
        }
        if ($expense !== null) {
            $expense = $this->Price->getPriceToDb($expense);
        }

        $response = $this->PrintShopStaticPrice->getByOptions($options);
        if ($response) {
            if ($expense !== null) {
                $key = 'expense';
                $value = $expense;
                if ($expense == 0) {
                    $value = null;
                }
            } else {
                $key = 'price';
                $value = $price;
            }
            if ($this->PrintShopStaticPrice->update($options, $key, $value)) {
                $data['response'] = true;
                $data['info'] = 'Updated';
            }
        } else {
            if ($lastID = $this->PrintShopStaticPrice->createPrice($options, $price, $expense)) {
                $data['response'] = true;
                $data['info'] = 'Created';
            }
        }

        return $data;
    }

    public function export($groupID, $typeID, $formatID)
    {
        ini_set('max_execution_time', 300);

        $this->PrintShopStaticPrice->setGroupID($groupID);
        $this->PrintShopStaticPrice->setTypeID($typeID);
        $this->PrintShopStaticPrice->setFormatID($formatID);
        $this->PrintShopOption->setGroupID($groupID);
        $this->PrintShopOption->setTypeID($typeID);

        $options = $this->PrintShopOption->getAll();

        $attributes = array();
        $aggregateOptions = array();
        foreach ($options as $option) {
            $aggregateOptions[$option['optID']] = $option;
            $option['ID'] = $option['optID'];
            $attributes[$option['attrSort']]['name'] = $option['attrName'];
            $attributes[$option['attrSort']]['ID'] = $option['attrID'];
            $attributes[$option['attrSort']]['name'] = $option['attrName'];
            $attributes[$option['attrSort']]['options'][] = $option;
        }

        $this->PrintShopPage->setGroupID($groupID);
        $this->PrintShopPage->setTypeID($typeID);
        $pages = $this->PrintShopPage->getAll();
        if (empty($pages)) {
            $pages = array(array('pages' => 2));
        }
        $pagesAsAttr = array();
        $pagesAsAttr[0] = array('ID' => 'pages', 'name' => 'pages', 'options' => null);
        foreach ($pages as $page) {
            $pagesAsAttr[0]['options'][] = array('ID' => $page['pages'], 'name' => $page['pages']);
        }
        $attributes = array_merge($pagesAsAttr, $attributes);

        $this->PrintShopVolume->setGroupID($groupID);
        $this->PrintShopVolume->setTypeID($typeID);

        $volumes = $this->PrintShopVolume->getAllByFormat($formatID);

        if (empty($volumes)) {
            $volumes[] = array('volume' => '1');
        }

        $volumesAsAttr = array('ID' => 'volumes', 'name' => 'volumes', 'options' => null);
        foreach ($volumes as $each) {
            if (!empty($each['formatID']) && $each['formatID'] != $formatID) {
                continue;
            }
            $volumesAsAttr['options'][] = array('ID' => $each['volume'], 'name' => $each['volume']);
        }
        $attributes[] = $volumesAsAttr;

        $matrix = array();
        reset($attributes);
        $first = current($attributes);
        $matrix[0] = $first['options'];

        $numberOfCombinations = $this->calculateNumberOfCombinations($attributes);

        $parts = ceil($numberOfCombinations / $this->getLimit());

        $prices = $this->PrintShopStaticPrice->getAll();

        $matrix = $this->buildMatrix($attributes, $matrix);

        return $this->generateExportFiles($groupID, $typeID, $formatID, $attributes, $matrix, $prices, $parts);
    }

    private function calculateNumberOfCombinations($attributes)
    {
        return array_reduce($attributes, function($carry, $item) {
            return $carry * count($item['options']);
        }, 1);
    }

    private function buildMatrix($attributes, $matrix)
    {
        foreach ($attributes as $each) {
            if ($each !== reset($attributes)) {
                $matrix = $this->matrix($matrix, $each['options']);
            }
        }
        return $matrix;
    }

    private function generateExportFiles($groupID, $typeID, $formatID, $attributes, $matrix, $prices, $parts)
    {
        $urls = [];
        for ($i = 0; $i < $parts; $i++) {
            $filename = $this->createFilename($groupID, $typeID, $formatID, $i);
            $sheetName = 'Format ' . $formatID;

            try {
                $newFileName = $this->makeFile($filename, $sheetName, $attributes, $matrix, $prices, $i);
            } catch (PHPExcel_Reader_Exception $exception) {
                return array(
                    'response' => false,
                    'info' => $exception->getMessage()
                );
            }

            $urls[] = STATIC_URL . companyID . '/export/' . $newFileName;
        }

        return array('response' => true, 'urls' => $urls);
    }

    private function createFilename($groupID, $typeID, $formatID, $part)
    {
        return $groupID . '_' . $typeID . '_' . $formatID . '-part-' . $part . '.xls';
    }

    private function checkOptionExclusions($extractOptions, $exclusions, $aggregateOptions)
    {
        if (!is_array($exclusions)) {
            return array();
        }

        $excludedOptions = array();
        foreach ($extractOptions as $attrID => $optID) {
            $tmpExclusions = $exclusions;
            $pos = array_search($attrID, array_keys($exclusions));
            if ($pos > 0) {
                array_splice($tmpExclusions, $pos - 1);
            }

            foreach ($tmpExclusions as $tmpExclusion) {
                $explode = explode(',', $tmpExclusion['excList']);
                if (in_array($optID, $explode)) {
                    $option = $aggregateOptions[$optID];
                    $excludedOptions[$option['attrID']] = $optID;
                }
            }
        }

        return $excludedOptions;
    }

    private function import($groupID, $typeID, $formatID, $path = null)
    {
        ini_set('max_execution_time', 720);

        $this->PrintShopStaticPrice->setGroupID($groupID);
        $this->PrintShopStaticPrice->setTypeID($typeID);
        $this->PrintShopStaticPrice->setFormatID($formatID);

        $data['response'] = true;

        if (!$this->openFile($path)) {
            $data['response'] = false;
            return $data;
        }

        $changes = 0;
        $sheetArray = $this->sheetToArray();

        $actualModel = $this->PrintShopStaticPrice->getDb();

        if ($actualModel->getPdo() === NULL) {
            $this->PrintShopStaticPrice = new PrintShopStaticPrice();
            $this->PrintShopStaticPrice->setGroupID($groupID);
            $this->PrintShopStaticPrice->setTypeID($typeID);
            $this->PrintShopStaticPrice->setFormatID($formatID);
        }

        foreach ($sheetArray as $key => $row) {
            if ($key == 1) {
                continue;
            }
            $options = $row['A'];

            if (empty($row['B'])) {
                if (!$this->PrintShopStaticPrice->customDelete($options)) {
                    $data['response'] = false;
                    $data['info'][] = 'Cannot delete price ' . $options;
                }
            } else {
                $response = $this->PrintShopStaticPrice->getByOptions($options);
                $price = $this->Price->getPriceToDb($row['B']);
                $expense = !empty($row['C']) ? $this->Price->getPriceToDb($row['C']) : null;

                if ($response) {
                    if (!$this->PrintShopStaticPrice->update($options, 'price', $price)) {
                        $data['response'] = false;
                        $data['info'][] = 'Cannot edit price ' . $options;
                    } else {
                        $changes++;
                    }

                    if (!$this->PrintShopStaticPrice->update($options, 'expense', $expense)) {
                        $data['response'] = false;
                        $data['info'][] = 'Cannot edit expense ' . $options;
                    } else {
                        $changes++;
                    }
                } else {
                    if (!$this->PrintShopStaticPrice->createPrice($options, $price, $expense)) {
                        $data['response'] = false;
                        $data['info'][] = 'Cannot add new price ' . $options;
                    } else {
                        $changes++;
                    }
                }
            }
        }
        $data['changes'] = $changes;
        return $data;
    }

    public function post_import($groupID, $typeID, $formatID)
    {
        $data['response'] = true;

        if (isset($_FILES)) {
            $data['files'] = $_FILES;
            $file = $_FILES['file'];
            $dir = STATIC_PATH . companyID . '/export/tmp/';
            if (!is_dir($dir)) {
                mkdir($dir, 0777, true);
            }
            $filename = $groupID . '_' . $typeID . '_' . $formatID . '.xls';
            $path = $dir . $filename;
            $data['path'] = $path;
            if (move_uploaded_file($file['tmp_name'], $path)) {
                $data = $this->import($groupID, $typeID, $formatID, $path);
                $data['uploadSuccess'] = true;
            } else {
                $data['response'] = false;
                $data['info'] = 'Upload failed';
            }
        } else {
            $data['response'] = false;
        }

        return $data;
    }

    public function newFile($sheetName = 'format')
    {
        $this->ExcelFile = new PHPExcel();
        $this->ExcelWriter = PHPExcel_IOFactory::createWriter($this->ExcelFile, 'Excel5');
        $this->ExcelFile->getActiveSheet()->setTitle($sheetName);
        return true;
    }

    private function openFile($path = null)
    {
        $src = $path ?: $this->path;
        if (!file_exists($src)) {
            return false;
        }

        $inputFileType = PHPExcel_IOFactory::identify($src);
        $this->ExcelReader = PHPExcel_IOFactory::createReader($inputFileType);
        $this->ExcelFile = $this->ExcelReader->load($src);

        if ($this->sheetIndex !== null) {
            $this->ExcelFile->setActiveSheetIndex($this->sheetIndex);
        }
        return true;
    }

    private function setCellValue($cell, $value)
    {
        $this->ExcelFile->getActiveSheet()->setCellValue(strtoupper($cell), $value);
        return true;
    }

    private function getCellValue($cell)
    {
        return $this->ExcelFile->getActiveSheet()->getCell(strtoupper($cell))->getCalculatedValue();
    }

    private function getCellContent($cell)
    {
        return $this->ExcelFile->getActiveSheet()->getCell(strtoupper($cell))->getValue();
    }

    private function setActiveSheet($index)
    {
        $this->ExcelFile->setActiveSheetIndex($index);
        return true;
    }

    private function sheetToArray()
    {
        return $this->ExcelFile->getActiveSheet()->toArray(null, true, true, true);
    }

    private function saveFile()
    {
        $this->ExcelWriter->save($this->path);
        chmod($this->path, 0777);
        return true;
    }

    private function matrix($matrix, $array)
    {
        $newIndex = count($matrix);
        $countMatrix = count($matrix);

        for ($i = 0; $i < $countMatrix; $i++) {
            $countMatrixI = count($matrix[$i]);
            for ($j = 0; $j < $countMatrixI; $j++) {
                for ($k = 0; $k < count($array); $k++) {
                    if ($k == 0) {
                        $matrix[$newIndex][$j] = $array[$k];
                    } else {
                        $matrix[$newIndex][count($matrix[$i])] = $array[$k];
                        $matrix[$i][] = $matrix[$i][$j];
                    }
                }
            }
        }

        return $matrix;
    }

    private function makeFile($filename, $sheetName, $attributes, $matrix, $prices, $part)
    {
        $dir = STATIC_PATH . companyID . '/export/';
        if (!is_dir($dir)) {
            mkdir($dir, 0777, true);
        }

        $filename = $filename . '-part-' . $part . '.xls';
        $this->path = $dir . $filename;

        $this->newFile($sheetName);

        $header = array_merge(['Klucz', 'Cena', 'Koszt'], array_column($attributes, 'name'));
        $alphas = range('A', 'Z');
        foreach ($header as $i => $each) {
            $this->setCellValue($alphas[$i] . '1', $each);
        }

        $prices = $prices ?: array();
        $startIndex = $part * $this->getLimit();
        $endIndex = (($part + 1) * $this->getLimit()) - 1;

        for ($i = $startIndex; $i < count($matrix[0]); $i++) {
            if ($i < $startIndex || $i > $endIndex) {
                continue;
            }

            $row = $this->createRow($matrix, $attributes, $i, $prices);
            $this->fillSheetRow($row, $i, $startIndex, $alphas);
        }

        $this->saveFile();
        return $filename;
    }

    private function createRow($matrix, $attributes, $i, &$prices)
    {
        $options = array();
        $optNames = array();
        for ($j = 0; $j < count($matrix); $j++) {
            $options[$attributes[$j]['ID']] = intval($matrix[$j][$i]['ID']);
            $optNames[] = $matrix[$j][$i]['name'];
        }

        uksort($options, array($this->Standard, 'sortLikeJs'));
        $row = ['key' => json_encode($options), 'price' => '', 'expense' => ''];
        foreach ($prices as $key => $price) {
            if ($price['options'] == $row['key']) {
                $row['price'] = $this->Price->getNumberToView($price['price']);
                if ($price['expense'] !== null) {
                    $row['expense'] = $this->Price->getNumberToView($price['expense']);
                }
                unset($prices[$key]);
                break;
            }
        }

        return array_merge($row, $optNames);
    }

    private function fillSheetRow($row, $i, $startIndex, $alphas)
    {
        $sheetRow = ($i - $startIndex) + 2;
        foreach ($row as $j => $value) {
            $this->setCellValue($alphas[$j] . $sheetRow, $value === false ? '' : $value);
        }
    }
}
