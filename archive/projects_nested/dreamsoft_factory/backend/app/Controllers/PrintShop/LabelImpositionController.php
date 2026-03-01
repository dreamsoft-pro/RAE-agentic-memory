<?php


namespace DreamSoft\Controllers\PrintShop;


use DreamSoft\Controllers\Components\Uploader;
use DreamSoft\Core\Controller;
use DreamSoft\Libs\LabelImposition\DTO\ImpositionPdfParameters;
use DreamSoft\Libs\LabelImposition\Services\HotFolderJobGenerator;
use DreamSoft\Libs\LabelImposition\Services\JobSeiGenerator;
use DreamSoft\Libs\LabelImposition\Services\VariantThird\CreatePdfService;
use DreamSoft\Models\Order\DpOrder;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Models\Order\DpProductLabelImposition;
use DreamSoft\Models\PrintShop\LabelImposition;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionDescription;
use DreamSoft\Models\PrintShopProduct\PrintShopFormat;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Models\PrintShopUser\UserCalcProductAttribute;
use DreamSoft\Models\PrintShopUser\UserCalcProductFile;

class LabelImpositionController extends Controller
{
    private UserCalcProductFile $UserCalcProductFile;
    private DpProductLabelImposition $DpProductLabelImposition;
    private LabelImposition $LabelImposition;
    private DpProduct $DpProduct;
    private DpOrder $DpOrder;
    private UserCalcProductAttribute $UserCalcProductAttribute;
    private UserCalcProduct $UserCalcProduct;
    private PrintShopFormat $Format;
    private UserCalc $UserCalc;
    private PrintShopConfigOptionDescription $PrintShopConfigOptionDescription;

    public function __construct($parameters = array())
    {
        parent::__construct($parameters);
        $this->LabelImposition = LabelImposition::getInstance();
        $this->UserCalcProductFile = UserCalcProductFile::getInstance();
        $this->DpProductLabelImposition = DpProductLabelImposition::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->DpOrder = DpOrder::getInstance();
        $this->UserCalcProductAttribute = UserCalcProductAttribute::getInstance();
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->Format = PrintShopFormat::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->PrintShopConfigOptionDescription = PrintShopConfigOptionDescription::getInstance();
    }

    public function index($typeID)
    {
        $result = $this->LabelImposition->getForType($typeID);
        if (!$result) {
            $result = ['productTypeID' => $typeID, 'enabled' => 1];
        }
        return $result;
    }

    public function put_index($typeID)
    {
        $allData = $this->Data->getAllPost();
        $result = $this->LabelImposition->updateAll($typeID, $allData);
        if ($result) {
            $result = $allData;
        }
        return $result;
    }

    public function post_index()
    {
        $allData = $this->Data->getAllPost();
        $result = $this->LabelImposition->create($allData);
        if ($result) {
            $allData['ID'] = $result;
            $result = $allData;
        }
        return $result;
    }

    public function generate($labelImpositionID, $productID, $calcProductID, $calcProductFileIDs, $copyToSpecialFolders)
    {
        $userCalcProduct = $this->UserCalcProduct->get('ID', $calcProductID);
        $format = $this->Format->get('ID', $userCalcProduct['formatID']);
        $dpProduct = $this->DpProduct->get('ID', $productID);
        $dpOrder = $this->DpOrder->getOne($dpProduct['orderID']);
        $psUserCalc = $this->UserCalc->get('ID', $userCalcProduct['calcID']);


        $allData = [];
        foreach (explode(',', $calcProductFileIDs) as $calcProductFileID) {

            if ($previousImposition = $this->DpProductLabelImposition->get('fileID', $calcProductFileID)) {
                $filesFields = ['labelImpositionPath', 'labelImpositionDieCutPath', 'xmlFile', 'anotherSignFile',
                    'hotFolderJobMarker', 'hotFolderJobImposition', 'labelImpositionDiePdfPath'];
                foreach ($filesFields as $field) {
                    $file = $previousImposition[$field];
                    $file = str_replace(STATIC_URL . companyID, '', $file);
                    $file = MAIN_UPLOAD . companyID . $file;
                    if (is_file($file)) {
                        unlink($file);
                    }
                }
            }

            $file = $this->UserCalcProductFile->get('ID', $calcProductFileID);
            $file0Dir = MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($calcProductID, $calcProductFileID);
            $path = $file0Dir . $file['name'];
            $labelImposition = $this->LabelImposition->get('ID', $labelImpositionID);
            $labelImposition['slope'] = $format['slope'];
            $labelImposition['labelUrl'] = $path;
            $labelImposition['outputDir'] = $file0Dir;
            $labelImposition['outputDirPrint'] = $this->getSynchroFolder('print', $dpOrder['orderNumber']);
            $labelImposition['outputDirCut'] = $this->getSynchroFolder('cut', $dpOrder['orderNumber']);
            $labelImposition['outputDirPdf'] = $this->getSynchroFolder('pdf', $dpOrder['orderNumber']);
            $labelImposition['copyToSpecialFolders'] = $copyToSpecialFolders;

            $labelImposition['cuttingDieFile'] = '';
            $attrs = $this->UserCalcProductAttribute->getByCalcProductIds([$calcProductID]);
            foreach ($attrs[array_key_first($attrs)] as $attr) {
                switch ($attr['specialFunction']) {
                    case 'rotation':
                        $labelImposition['labelRotation'] = (int)$attr['optName'];
                        break;
                    case 'rounding':
                        $labelImposition['rounding'] = $attr['attrPages'] ?? $attr['optName'];
                        break;
                    case 'cuttingDie':
                        if ($attr['optName'] === 'ellipse') {
                            $labelImposition['drawEllipse'] = true;
                        } else {
                            $cuttingDieFile = $this->UserCalcProductFile->get('userCalcProductAttrOptionID', $attr['ID']);
                            if ($cuttingDieFile) {
                                $fileDir = MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($calcProductID, $cuttingDieFile['ID']);
                                $labelImposition['cuttingDieFile'] = $fileDir . $cuttingDieFile['name'];
                            }
                        }
                        break;
                    default:
                        continue;

                }
            }
            $labelImposition['barcodes'] = $labelImposition['barcodeEnabled'] ? [[
                'data' => $this->replaceVars($labelImposition['barcodeData'], $productID),
                'positionX' => $labelImposition['barcodePositionX'],
                'positionY' => $labelImposition['barcodePositionY'],
                'width' => $labelImposition['barcodeWidth'],
                'height' => $labelImposition['barcodeHeight']
            ]] : [];
            $labelImposition['qrcodes'] = $labelImposition['qrCodeEnabled'] ? [[
                'data' => $this->replaceVars($labelImposition['qrCodeData'], $productID),
                'positionX' => $labelImposition['qrCodePositionX'],
                'signFilePositionX' => $labelImposition['qrCodeAnotherSignFilePositionX'],
                'positionY' => $labelImposition['qrCodePositionY'],
                'height' => $labelImposition['qrCodeSize']
            ]] : [];

            $labelImposition['photocells'] = $labelImposition['photocellEnabled'] ? [[
                'positionX' => $labelImposition['photocellPositionX'],
                'signFilePositionX' => $labelImposition['photocellAnotherSignFilePositionX'],
                'positionY' => $labelImposition['photocellPositionY'],
                'width' => $labelImposition['photocellWidth'],
                'height' => $labelImposition['photocellHeight']
            ]] : [];
            $labelImposition['fileNamePrefix'] = $dpOrder['orderNumber'] . '_' . $productID . '_' . $calcProductFileID . '_';
            $impositionPdfParameters = new ImpositionPdfParameters($labelImposition);
            try {
                $service = new CreatePdfService($impositionPdfParameters);
            } catch (\Exception $e) {
                $fileErrorData = ['error' => $e->getMessage() . "(" . $file['name'] . ")"];
                $allData[] = $fileErrorData;
                return $allData;
            }

            $pdfData = $service->createPdf();

            $paperAttr = current(array_filter($attrs[array_key_first($attrs)], fn($item) => $item['type'] == 3));
            $this->PrintShopConfigOptionDescription->setAttrID($paperAttr['attrID']);
            $this->PrintShopConfigOptionDescription->setOptID($paperAttr['optID']);
            $this->PrintShopConfigOptionDescription->setDomainID($this->getDomainID());
            $descriptionsAll = $this->PrintShopConfigOptionDescription->getForOption();
            $paperType = current(array_filter($descriptionsAll, fn($item) => $item['name'] == 'paper_type'))['value'];
            $xmlGenerator = new JobSeiGenerator();
            $xmlGenerator->setData(['dpOrder' => $dpOrder,
                'cutFileName' => $pdfData['dieCutFileName'],
                'userCalcProductFile' => $file,
                'sheetWidth' => $labelImposition['sheetWidth'],
                'moduleStep' => sprintf('%01.2f', $pdfData['moduleStep']),
                'material' => $paperType,
                'rotationAngle' => $labelImposition['rotationAngle'],
            ]);
            $xmlFile = $xmlGenerator->generate(MAIN_UPLOAD . companyID . '/' . $impositionPdfParameters->getOutputDirCut(),
                $labelImposition['fileNamePrefix'],
                $labelImposition['copyToSpecialFolders']);

            $hotFolderJobGenerator = new HotFolderJobGenerator();
            $hotFolderJobGenerator->setData(['dpOrder' => $dpOrder,
                'dpProduct' => $dpProduct,
                'psUserCalc' => $psUserCalc,
                'userCalcProductFile' => $file,
                'fileURL' => $pdfData['fileName'],
                'numberOfCopies' => ceil($file['volume'] / $pdfData['sumLabelsOnSheet']),
                'sheetWidth' => $labelImposition['sheetWidth'],
                'moduleStep' => sprintf('%01.2f', $pdfData['moduleStep']),
            ]);
            $xmlFile2 = $hotFolderJobGenerator->generate(MAIN_UPLOAD . companyID . '/' . $impositionPdfParameters->getOutputDirPrint(),
                $labelImposition['fileNamePrefix'] . 'imposition',
                $labelImposition['copyToSpecialFolders']
            );
            $hotFolderJobGenerator->setData(['dpOrder' => $dpOrder,
                'dpProduct' => $dpProduct,
                'psUserCalc' => $psUserCalc,
                'userCalcProductFile' => $file,
                'fileURL' => $pdfData['anotherSignFile'],
                'numberOfCopies' => 1,
                'sheetWidth' => $labelImposition['sheetWidth'],
                'moduleStep' => sprintf('%01.2f', $pdfData['moduleStep']),
            ]);
            $xmlFile3 = $hotFolderJobGenerator->generate(MAIN_UPLOAD . companyID . '/' . $impositionPdfParameters->getOutputDirPrint(),
                $labelImposition['fileNamePrefix'] . 'marker',
                $labelImposition['copyToSpecialFolders']
            );

            $params = [
                'labelImpositionPath' => STATIC_URL . companyID . '/' . $impositionPdfParameters->getOutputDirPrint() . $pdfData['fileName'],
                'labelImpositionDieCutPath' => STATIC_URL . companyID . '/' . $impositionPdfParameters->getOutputDirCut() . $pdfData['dieCutFileName'],
                'labelImpositionDiePdfPath' => STATIC_URL . companyID . '/' . $impositionPdfParameters->getOutputDirPdf() . $pdfData['dieCutFileName'],
                'sheetLengthInMm' => $pdfData['sheetLengthInMm'],
                'sheetSurfaceInSquareMm' => $pdfData['sheetSurfaceInSquareMm'],
                'sumLabelsOnSheet' => $pdfData['sumLabelsOnSheet'],
                'xmlFile' => STATIC_URL . companyID . '/' . $impositionPdfParameters->getOutputDirCut() . $xmlFile,
                'hotFolderJobMarker' => STATIC_URL . companyID . '/' . $impositionPdfParameters->getOutputDirPrint() . $xmlFile3,
                'hotFolderJobImposition' => STATIC_URL . companyID . '/' . $impositionPdfParameters->getOutputDirPrint() . $xmlFile2,
                'anotherSignFile' => STATIC_URL . companyID . '/' . $impositionPdfParameters->getOutputDirPrint() . $pdfData['anotherSignFile'],
            ];
            $pdfData['labelImpositionPath'] = $params['labelImpositionPath'];
            $pdfData['labelImpositionDieCutPath'] = $params['labelImpositionDieCutPath'];
            $pdfData['xmlFile'] = $params['xmlFile'];
            $pdfData['hotFolderJobMarker'] = $params['hotFolderJobMarker'];
            $pdfData['hotFolderJobImposition'] = $params['hotFolderJobImposition'];
            $pdfData['anotherSignFile'] = $params['anotherSignFile'];
            if ($this->DpProductLabelImposition->get('fileID', $calcProductFileID)) {
                $pdfData['success'] = $this->DpProductLabelImposition->updateAll($calcProductFileID, $params, 'fileID');
            } else {
                $params['fileID'] = $calcProductFileID;
                $pdfData['success'] = $this->DpProductLabelImposition->create($params, false, 'fileID') !== false;
            }
            $allData[] = $pdfData;
        }
        return $allData;
    }

    private function replaceVars(string $baseContent, int $productID)
    {
        $dpProduct = $this->DpProduct->get('ID', $productID);
        $dpOrder = $this->DpOrder->getOne($dpProduct['orderID']);
        $vars = [
            'order_number' => $dpOrder['orderNumber'],
            'user_name' => $dpOrder['userName'],
            'user_last_name' => $dpOrder['userLastname'],
            'user_email' => $dpOrder['userMail'],
        ];
        foreach ($vars as $key => $var) {
            $baseContent = str_replace('{' . $key . '}', $var, $baseContent);
        }
        return $baseContent;
    }

    private function getSynchroFolder(string $section, int $orderNumber)
    {
        $folder = 'productFiles/' . $section . '/' . date('Ymd') . '/' . $orderNumber;
        $localPath = MAIN_UPLOAD . companyID . '/' . $folder;
        if (!is_dir($localPath)) {
            mkdir($localPath, 0755, true);
            chmod($localPath, 0755);
        }
        return $folder . '/';
    }
}
