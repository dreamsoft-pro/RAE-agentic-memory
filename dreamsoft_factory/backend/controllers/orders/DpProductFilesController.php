<?php

use DreamSoft\Controllers\Components\{
    RealizationTimeComponent, Acl, Uploader
};
use DreamSoft\Libs\Debugger;
use DreamSoft\Controllers\Orders\DpProductsController;
use DreamSoft\Core\Controller;
use DreamSoft\Models\Currency\Currency;
use DreamSoft\Models\Order\{
    DpOrder, DpProduct, DpProductFile, DpProductReportFile
};
use DreamSoft\Models\Other\ModelIconExtension;
use DreamSoft\Models\Price\BasePrice;
use DreamSoft\Models\PrintShopUser\{
    FixFilePrice, UserCalc, UserCalcProduct, UserCalcProductFile
};
use DreamSoft\Models\Setting\Setting;
use DreamSoft\Models\Tax\Tax;
use DreamSoft\Models\Upload\UploadFile;
use DreamSoft\Traits\ImagePathTrait;
use setasign\Fpdi\{
    PdfReader\PageBoundaries, Tcpdf\Fpdi
};
use Twig\Environment as Twig_Environment;
use Twig\Loader\FilesystemLoader;
use Imagick;
use ImagickPixel;
use ImagickException;

class DpProductFilesController extends Controller
{
    use ImagePathTrait;

    protected $UserCalcProduct;
    protected $UserCalcProductFile;
    protected $DpProductReportFile;
    protected $DpProduct;
    protected $DpOrder;
    protected $Uploader;
    protected $ModelIconExtension;
    private $Acl;
    private $UploadFile;
    private $FixFilePrice;
    private $BasePrice;
    private $Setting;
    private $Currency;
    private $Tax;
    private $UserCalc;
    private $RealizationTimeComponent;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->UserCalcProductFile = UserCalcProductFile::getInstance();
        $this->DpProductReportFile = DpProductReportFile::getInstance();
        $this->DpOrder = DpOrder::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->ModelIconExtension = ModelIconExtension::getInstance();
        $this->Acl = new Acl();
        $this->Uploader = Uploader::getInstance();
        $this->UploadFile = UploadFile::getInstance();
        $this->BasePrice = BasePrice::getInstance();
        $this->FixFilePrice = FixFilePrice::getInstance();
        $this->Setting = Setting::getInstance();
        $this->Currency = Currency::getInstance();
        $this->Tax = Tax::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->RealizationTimeComponent = RealizationTimeComponent::getInstance();
    }

    public function post_files($calcProductID, $userCalcProductAttrOptionID)
    {
        $product = $this->UserCalcProduct->get('ID', $calcProductID);
        $created = date('Y-m-d H:i:s');
        $name = strtolower($_FILES['file']['name']);

        if (!$this->ModelIconExtension->isAllowedFile($name)) {
            return $this->sendFailResponse('11');
        }

        $width = 0;
        $height = 0;
        $colorSpace = 0;
        $modelExtensionID = $this->ModelIconExtension->nameToModelExtensionID($name);
        $additionalData = $this->Data->getAllPost() ?? [];
        $fileID = $additionalData['update'] ? $additionalData['fileID'] : $this->UserCalcProductFile->add([
            'created' => $created,
            'userCalcProductAttrOptionID' => $userCalcProductAttrOptionID,
            'name' => $name,
            'width' => $width,
            'height' => $height,
            'colorSpace' => $colorSpace,
            'modelExtensionID' => $modelExtensionID,
            'backSideTarget' => count($this->UserCalcProductFile->getOptionFiles($calcProductID, $userCalcProductAttrOptionID)) == 1 ? 1 : 0,
            'volume' => getallheaders()['Volume']
        ]);

        if ($additionalData['update']) {
            $this->UserCalcProductFile->updateAll($fileID, ['name' => $name, 'modelExtensionID' => $modelExtensionID]);
        }

        $lastFile = $this->UserCalcProductFile->get('ID', $fileID);
        $res = $this->Uploader->uploadToCompany($_FILES, 'file', Uploader::getUploadPath($calcProductID, $lastFile['ID']), $lastFile['name']);

        if (!$res) {
            return ['response' => false];
        }

        $lastFile['name'] = $res;
        $this->updateFileMetrics($lastFile, $product);
        $this->DpProduct->update($calcProductID, 'acceptCanceled', 0);
        $this->makeMiniature($lastFile, $calcProductID);
        $this->updatePreview($calcProductID);

        return ['response' => true, 'file' => $lastFile];
    }

    public function put_files($calcProductID, $fileID)
    {
        $product = $this->UserCalcProduct->get('ID', $calcProductID);
        $file = $this->UserCalcProductFile->get('ID', $fileID);
        $localPath = MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($calcProductID, $fileID) . $file['name'];
        $ext = $this->ModelIconExtension->getExtension($file['name']);
        $newFileName = preg_replace('/\.' . $ext . '/', '-mod.' . $ext, $file['name']);
        $tempPath = MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($calcProductID, $fileID) . $newFileName;

        if (str_contains(strtolower($file['name']), '.pdf')) {
            list($localPath, $width, $height, $widthNet, $heightNet, $pagesCount, $colorSpace) = self::getFileDimensions($product['ID'], $file);
            $startDim = [$widthNet, $heightNet, $width, $height];

            if ($widthNet != ($product['formatWidth'] - 2 * $product['slope'])) {
                $newW = $product['formatWidth'] - 2 * $product['slope'];
                $scale = $newW / $widthNet;
                $widthNet = $newW;
                $heightNet *= $scale;
            }

            if ($heightNet != ($product['formatHeight'] - 2 * $product['slope'])) {
                if ($heightNet > ($product['formatHeight'] - 2 * $product['slope'])) {
                    $newH = $product['formatHeight'] - 2 * $product['slope'];
                    $scale = $newH / $heightNet;
                    $heightNet = $newH;
                }
            }

            $width = $product['formatWidth'];
            $height = $product['formatHeight'];
            self::resizePDF($localPath, $pagesCount, $tempPath, $widthNet, $heightNet, $width, $height, $startDim);
            unlink(MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($calcProductID, $fileID) . THUMB_IMAGE_PREFIX . $file['name']);
        } else {
            $imagickFile = new Imagick($localPath);
            $toPx = fn($mm) => ceil($mm / 25.4 * 300);
            $newW = $toPx($product['formatWidth']);
            $newH = ceil($file['height'] * $newW / $file['width']);
            $imagickFile->scaleImage($newW, $newH);

            if ($newH > $toPx($product['formatHeight'])) {
                $imagickFile->cropImage($newW, $toPx($product['formatHeight']), 0, ceil(($newH - $toPx($product['formatHeight'])) / 2));
            } else if ($newH < $toPx($product['formatHeight'])) {
                $marginHeight = ceil(($toPx($product['formatHeight']) - $newH) / 2);
                $cloneTop = clone $imagickFile;
                $cloneTop->cropImage($toPx($product['formatWidth']), 1, 0, 0);
                $cloneTop->scaleImage($cloneTop->getImageWidth(), $marginHeight);

                $cloneBottom = clone $imagickFile;
                $cloneBottom->cropImage($toPx($product['formatWidth']), 1, 0, $newH - 1);
                $cloneBottom->scaleImage($cloneBottom->getImageWidth(), $marginHeight);

                $newImage = new Imagick();
                $newImage->newImage($toPx($product['formatWidth']), $toPx($product['formatHeight']), 'red');
                $newImage->compositeImage($cloneTop, Imagick::COMPOSITE_DEFAULT, 0, 0);
                $newImage->compositeImage($imagickFile, Imagick::COMPOSITE_DEFAULT, 0, $marginHeight);
                $newImage->compositeImage($cloneBottom, Imagick::COMPOSITE_DEFAULT, 0, $marginHeight + $newH);
                $imagickFile = $newImage;
            }

            $imagickFile->writeImage($tempPath);
        }

        $file['name'] = $newFileName;
        $this->UserCalcProductFile->updateAll($file['ID'], ['name' => $newFileName, 'fileFixed' => 1]);
        $this->makeMiniature($file, $calcProductID);
        $this->updateFileMetrics($file, $product);
        $this->updatePreview($calcProductID);

        return ['response' => true];
    }

    public function post_saveFileProps($productID, $fileID)
    {
        $posts = $this->Data->getAllPost();
        $result = true;

        foreach ($posts as $key => $value) {
            $result = $result && $this->UserCalcProductFile->update($fileID, $key, $value);
        }

        return $result;
    }

    public function post_saveProductProps($productID)
    {
        $sendToFix = $this->Data->getPost('sendToFix');
        return $this->saveSendToFix($sendToFix, $productID);
    }

    public function files($productID)
    {
        $product = $this->DpProduct->get('ID', $productID);
        $order = $this->DpOrder->get('ID', $product['orderID']);
        $user = $this->Auth->getLoggedUser();

        if ($order['userID'] !== null && ($user['super'] == 0) && ($order['userID'] !== $user['ID']) && !$this->Acl->canSeeUserFiles($user)) {
            return [];
        }

        $productFiles = $this->UserCalcProductFile->getByProduct($productID);

        if (empty($productFiles)) {
            return [];
        }

        foreach ($productFiles as &$productFile) {
            foreach ($productFile['files'] as &$file) {
                $this->addUrls($file, $productFile['calcProductID']);
            }
        }

        return $productFiles;
    }

    public function productListFiles($orderParams)
    {
        $result = ['files' => [], 'reportFiles' => []];
        $orderParams = explode(',', $orderParams);
        $firstOrderID = current($orderParams);
        $order = $this->DpOrder->get('ID', $firstOrderID);
        $user = $this->Auth->getLoggedUser();

        if ($order['userID'] !== null && ($user['super'] == 0) && ($order['userID'] !== $user['ID'])) {
            return $result;
        }

        $filesList = $this->UserCalcProductFile->getByOrderList($orderParams, 0);
        $reportsList = $this->DpProductReportFile->getByOrderList($orderParams);

        if (empty($filesList) && empty($reportsList)) {
            return $result;
        }

        if (!empty($filesList)) {
            foreach ($filesList as $id => &$prodFiles) {
                foreach ($prodFiles as &$prodFile) {
                    foreach ($prodFile['files'] as &$file) {
                        $this->addUrls($file, $prodFile['calcProductID']);
                    }
                }
            }

            $result['files'] = $filesList;
        }

        if (!empty($reportsList)) {
            foreach ($reportsList as $row) {
                $row['url'] = STATIC_URL . 'uploadedFiles/' . companyID . '/' . $row['path'];
                $explodedPath = explode('/', $row['path']);
                $row['minUrl'] = STATIC_URL . 'uploadedFiles/' . companyID . '/' . $explodedPath[0] . '/' . Uploader::getMiniatureName($row['name']);
                $result['reportFiles'][$row['productID']][] = $row;
            }
        }

        return $result;
    }

    protected function _delete_file($fileID, $productID)
    {
        $result = [];
        $one = $this->UserCalcProductFile->get('ID', $fileID);

        if (!$one) {
            return $this->sendFailResponse('04');
        }

        $product = $this->UserCalcProduct->getDpProduct($productID);

        if (count($this->UserCalcProductFile->getFlatFiles($product['calcID'])) === 1 && $product['sendToFix'] === 1) {
            $this->saveSendToFix(0, $product['ID']);
        }

        if ($this->Uploader->removeFromCompany(Uploader::getUploadPath($productID, $fileID), $one['name'])) {
            if ($this->UserCalcProductFile->delete('ID', $one['ID'])) {
                return ['response' => true, 'removed_item' => $one];
            }

            return $this->sendFailResponse('05');
        }

        return $this->sendFailResponse('05');
    }

    public function delete_files($calcProductID, $fileID)
    {
        $result = $this->_delete_file($fileID, $calcProductID);
        $this->updatePreview($calcProductID);
        return $result;
    }

    public function canSeeUserFiles()
    {
        $user = $this->Auth->getLoggedUser();
        return ['response' => $this->Acl->canSeeAllOngoings($user)];
    }

    private function makeMiniature($file, $productID)
    {
        $explodeName = explode('.', $file['name']);
        $ext = end($explodeName);
        $minImageName = false;

        if ($ext == THUMB_PDF_ALLOWED_EXTENSION) {
            array_pop($explodeName);
            $minImageName = implode('.', $explodeName) . '.jpg';
        } elseif (in_array($ext, explode(',', THUMB_IMAGE_ALLOWED_EXTENSION))) {
            $minImageName = $file['name'];
        }

        $minFile = STATIC_PATH . companyID . '/' . Uploader::getUploadPath($productID, $file['ID']) . THUMB_IMAGE_PREFIX . $minImageName;
        $minUrl = STATIC_URL . companyID . '/' . Uploader::getUploadPath($productID, $file['ID']) . THUMB_IMAGE_PREFIX . $minImageName;

        if (!is_file($minFile)) {
            try {
                $minImage = $this->Uploader->resizeImage(MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($productID, $file['ID']) . $file['name'], THUMB_IMAGE_RESIZE_WIDTH, THUMB_IMAGE_RESIZE_HEIGHT, false);
                $minImage->writeImage(MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($productID, $file['ID']) . THUMB_IMAGE_PREFIX . $minImageName);
                return ['response' => true, 'minUrl' => $minUrl, 'created' => true];
            } catch (ImagickException $exception) {
                return ['response' => false, 'info' => $exception->getMessage()];
            }
        }

        return ['response' => true, 'minUrl' => $minUrl, 'created' => false];
    }

    public function patch_reportFiles($productID, $fileID)
    {
        list($loggedUser, $userName) = $this->getFormatedUserData();
        if ($this->DpProductReportFile->setAccepted($fileID, $loggedUser['ID'], $userName)) {
            $dpProductsController = DpProductsController::getInstance();
            $dpProductsController->setDomainID($this->getDomainID());
            $dpProductsController->sendReportAcceptedMail($productID, $fileID);

            if ($this->DpProduct->checkAllReportsAccepted($productID)) {
                $dpProductsController->changeStatusAndSendMail($productID, 1);
            }

            return ['response' => true, 'reportAccepted' => true];
        }

        return ['response' => false];
    }

    public function patch_files($productID, $fileID)
    {
        list($loggedUser, $userName) = $this->getFormatedUserData();
        return ['response' => $this->UserCalcProductFile->setAccepted($fileID, $loggedUser['ID'], $userName)];
    }

    public function delete_reportFiles($productID, $fileID)
    {
        $comment = $this->Data->getPost('comment');
        list($loggedUser, $userName) = $this->getFormatedUserData();
        return ['response' => $this->DpProductReportFile->setRejected($fileID, $comment, $loggedUser['ID'], $userName)];
    }

    private function getFormatedUserData(): array
    {
        $loggedUser = $this->Auth->getLoggedUser();
        $userName = $loggedUser['firstname'] . ' ' . $loggedUser['lastname'];
        if ($loggedUser['super']) {
            $userName .= ' (Admin)';
        }

        return [$loggedUser, $userName];
    }

    private function updateFileMetrics($file, $product): bool
    {
        list($localPath, $width, $height, $widthNet, $heightNet, $pagesCount, $colorSpace) = self::getFileDimensions($product['ID'], $file);

        $this->UserCalcProductFile->update($file['ID'], 'size', filesize($localPath));
        $this->UserCalcProductFile->update($file['ID'], 'width', $width);
        $this->UserCalcProductFile->update($file['ID'], 'height', $height);
        $this->UserCalcProductFile->update($file['ID'], 'widthNet', $widthNet);
        $this->UserCalcProductFile->update($file['ID'], 'heightNet', $heightNet);
        $this->UserCalcProductFile->update($file['ID'], 'pagesDiff', $pagesCount - $product['pages']);
        $this->UserCalcProductFile->update($file['ID'], 'colorSpace', $colorSpace);

        $dimensionsValid = ($width == $product['formatWidth'] && $height == $product['formatHeight']);

        if (str_contains(strtolower($file['name']), '.pdf')) {
            $dimensionsValid = $dimensionsValid && ($widthNet == $product['formatWidth'] - $product['slope'] * 2 && $heightNet == $product['formatHeight'] - $product['slope'] * 2);
        }

        $dimensionsValid = $dimensionsValid ? 1 : 0;
        $this->UserCalcProductFile->update($file['ID'], 'dimensionsValid', $dimensionsValid);

        return (bool) $dimensionsValid;
    }

    public static function getFileDimensions($productID, $file): ?array
    {
        $localPath = MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($productID, $file['ID']) . $file['name'];

        if (str_contains(strtolower($file['name']), '.pdf')) {
            $tcpdf = new Fpdi('', 'pt');
            $pagesCount = $tcpdf->setSourceFile($localPath);
            $templateId = $tcpdf->importPage(1, PageBoundaries::BLEED_BOX);
            $bleedBox = $tcpdf->getTemplateSize($templateId);
            $templateId = $tcpdf->importPage(1, PageBoundaries::TRIM_BOX);
            $trimBox = $tcpdf->getTemplateSize($templateId);

            $Points2Milis = fn($p) => round($p * 25.4 / 72);
            $width = $Points2Milis($bleedBox['width']);
            $height = $Points2Milis($bleedBox['height']);
            $widthNet = $Points2Milis($trimBox['width']);
            $heightNet = $Points2Milis($trimBox['height']);

            exec('"' . GHOSTCRIPT_COMMAND . '" -dNOSAFER -dQUIET -o - -sDEVICE=ink_cov ' . $localPath, $result2, $ret);

            if ($ret != 0) {
                Debugger::getInstance()->debug('Cant run ghostscript', $result2);
                return null;
            }

            $colorSpaceData = preg_split('/ /', trim($result2[0]));

            foreach ($colorSpaceData as $data) {
                if (is_string($data) && !empty($data) && !is_numeric($data)) {
                    $colorSpace = $data;
                    break;
                }
            }
        } else {
            $imagickFile = new Imagick($localPath);
            $toMilis = fn($px) => round($px / 300 * 2.54 * 10);
            $width = $toMilis($imagickFile->getImageWidth());
            $height = $toMilis($imagickFile->getImageHeight());
            $imagickColorSpace = $imagickFile->getImageColorspace();
            $refl = new ReflectionClass(new Imagick);
            $const = $refl->getReflectionConstants();
            $colorSpace = '';

            foreach ($const as $c) {
                if (str_contains($c->getName(), 'COLORSPACE') && $c->getValue() == $imagickColorSpace) {
                    $colorSpace = preg_replace('/COLORSPACE_/', '', $c->getName());
                    break;
                }
            }

            $widthNet = $heightNet = $pagesCount = 0;
        }

        return [$localPath, $width, $height, $widthNet, $heightNet, $pagesCount, $colorSpace];
    }

    private function updatePreview($calcProductID)
    {
        return;
        // This method is currently disabled.
    }

    public static function resizePDF($localPath, $pagesCount, $tempPath, $widthNet, $heightNet, $width, $height, $startDim)
    {
        $toPt = fn($mm) => $mm * 72 / 25.4;
        $slopeX = $toPt(($width - $widthNet) / 2);
        $slopeY = $toPt(($height - $heightNet) / 2);
        $widthNet = $toPt($widthNet);
        $heightNet = $toPt($heightNet);
        $width = $toPt($width);
        $height = $toPt($height);

        $format = [
            'TrimBox' => ['llx' => $slopeX, 'lly' => $slopeY, 'urx' => $widthNet + $slopeX, 'ury' => $heightNet + $slopeY],
            'BleedBox' => ['llx' => 0, 'lly' => 0, 'urx' => $width, 'ury' => $height],
            'CropBox' => ['llx' => 0, 'lly' => 0, 'urx' => $width, 'ury' => $height],
            'MediaBox' => ['llx' => 0, 'lly' => 0, 'urx' => $width, 'ury' => $height]
        ];

        $tcpdf = new Fpdi('', 'pt', $format);
        $tcpdf->setSourceFile($localPath);
        $sc = [$widthNet / $toPt($startDim[0]), $heightNet / $toPt($startDim[1])];
        $offset = [($widthNet - $toPt($startDim[0])) / 2 * $sc[0], ($heightNet - $toPt($startDim[1])) / 2 * $sc[1]];

        for ($i = 0; $i < $pagesCount; $i++) {
            $tcpdf->addPage();
            $pageID = $tcpdf->importPage($i + 1, '/BleedBox');
            $tcpdf->useImportedPage($pageID, -$offset[0], -$offset[1], $width + $offset[0] * 2, $height + $offset[1] * 2);
        }

        $tcpdf->Output($tempPath, 'F');
    }

    private function saveSendToFix($sendToFix, $productID)
    {
        $productPrice = $this->DpProduct->getProductPrice($productID);
        $this->Setting->setDomainID($this->getDomainID());
        $this->Tax->setDomainID($this->getDomainID());
        $this->Currency->setDomainID($this->getDomainID());
        $currency = $this->Currency->get('CODE', $productPrice['currency']);
        $taxID = $this->Setting->getValue('defaultTax', 'general');
        $tax = $this->Tax->get('ID', $taxID);
        $fixFileDays = $this->Setting->getValue('fixFileDays', 'additionalSettings');
        $dpProduct = $this->DpProduct->get('ID', $productID);
        $userCalc = $this->UserCalc->get('ID', $dpProduct['calcID']);
        $return = true;

        if ($sendToFix) {
            $price = $this->Setting->getValue('fixFilePrice', 'additionalSettings');
            $return &= $this->FixFilePrice->create(['price' => $price, 'productID' => $productID]);
            $return &= $this->DpProduct->updateProductPrice($productID, $price, $tax['value'], $currency, true);
            $realisationDate = strtotime($userCalc['realisationDate']) + $fixFileDays * 24 * 60 * 60;
        } else {
            $fixFilePrice = $this->FixFilePrice->get('productID', $productID);
            $price = $fixFilePrice['price'];
            $return &= $this->FixFilePrice->delete('productID', $productID);
            $return &= $this->BasePrice->delete('ID', $fixFilePrice['priceID']);
            $return &= $this->DpProduct->updateProductPrice($productID, $price, $tax['value'], $currency, false);
            $realisationDate = strtotime($userCalc['realisationDate']) - $fixFileDays * 24 * 60 * 60;
        }

        $return &= $this->UserCalc->update($userCalc['ID'], 'realisationDate', date('Y-m-d', $realisationDate));
        $return &= $this->DpProduct->update($productID, 'sendToFix', $sendToFix);

        return $return;
    }
}
