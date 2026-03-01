<?php

namespace DreamSoft\Libs\LabelImposition\Traits;

use DreamSoft\Libs\LabelImposition\Services\LabelFilePreparer;
use DreamSoft\Libs\LabelImposition\Services\Renderers\DieCutRenderer;
use setasign\Fpdi\Tcpdf\Fpdi;

trait BarcodesTrait
{
    protected Fpdi $anotherPdfCreator;

    public function initializeAnother()
    {
        if ($this->parameters->getAnotherSignFile()) {
            $this->anotherPdfCreator = new Fpdi();
            $this->anotherPdfCreator->setPrintHeader(false);
            $this->anotherPdfCreator->setAutoPageBreak(false);
            $this->anotherPdfCreator->setPrintFooter(false);
            $this->anotherPdfCreator->AddPage(
                $this->calculator->getPageOrientationQr(),
                [
                    $this->calculator->getSheetLengthQr(),
                    $this->parameters->getSheetWidth()]
            );
            $this->anotherPdfCreator->startLayer('CUT');

        }
    }

    public function finalizeAnother($path)
    {
        if ($this->parameters->getAnotherSignFile()) {
            $this->anotherPdfCreator->endLayer();
            $fileName = $this->parameters->getFileNamePrefix() . 'markers' . LabelFilePreparer::dateName() . '.pdf';
            $fullPath = MAIN_UPLOAD . companyID . '/' . $path . $fileName;
            $this->anotherPdfCreator->Output($fullPath, 'F');
            if($this->parameters->getCopyToSpecialFolders()===1) {
                $this->copyFileToRaw($fullPath);
            }
            return $fileName;
        }
        return null;
    }

    public function addBarcode(): void
    {

        foreach ($this->parameters->getBarcodes() as $barcode) {

            $barcodeData = $barcode['data'];
            $barcodePositionX = $this->calculateCodePositionX($barcode['positionX'], $barcode['height']);
            $barcodePositionY = $barcode['positionY'];
            $barcodeWidth = $barcode['width'];
            $barcodeHeight = $barcode['height'];

            $this->pdfCreator->StartTransform();
            $this->pdfCreator->Rotate(90);
            $this->pdfCreator->write1DBarcode($barcodeData, 'S25', -$barcodePositionY, $barcodePositionX, $barcodeWidth, $barcodeHeight);
            $this->pdfCreator->StopTransform();
        }
    }

    private function calculateCodePositionX(string $positionX, float $codeHeight): float
    {
        if ($positionX === 'right') {
            return $this->parameters->getSheetWidth() - $codeHeight;
        }

        return 0;
    }

    public function addQr($pdfCreator): void
    {
        foreach ($this->parameters->getQrCodes() as $qrCode) {

            $qrCodeData = str_replace('{die_cut_file_name}', $this->parameters->getDieCutFileName(), $qrCode['data']);
            $qrCodePositionX = $this->calculateCodePositionX($qrCode['positionX'], $qrCode['height']);
            if ($this->parameters->getAnotherSignFile()) {
                $qrCodePositionX += $qrCode['signFilePositionX'];
            }
            $qrCodePositionY = $qrCode['positionY'];
            $qrCodeSize = $qrCode['height'];
            $creator = $this->parameters->getAnotherSignFile() ? $this->anotherPdfCreator : $pdfCreator;
            $creator->StartTransform();
            $creator->Rotate(90);
            $creator->write2DBarcode($qrCodeData, 'QRCODE,H', -$qrCodePositionY, $qrCodePositionX, $qrCodeSize, $qrCodeSize);
            $creator->StopTransform();
        }
    }

    public function addPhotocell($pdfCreator): void
    {
        $creator = $this->parameters->getAnotherSignFile() ? $this->anotherPdfCreator : $pdfCreator;
        foreach ($this->parameters->getPhotoCells() as $photoCell) {
            if ($this->parameters->getAnotherSignFile()) {
                $photocellPositionX = $this->parameters->getPhotocellAnotherSignFilePositionX();
                $photocellPositionY = $this->parameters->getPhotocellAnotherSignFilePositionY();
                $creator->Rect($photocellPositionX, $photocellPositionY, $photoCell['width'], $photoCell['height'], 'F');
            } else {
                $photocellPositionX = $this->calculateCodePositionX($photoCell['positionX'], $photoCell['height']);
                $photocellPositionY = $photoCell['positionY'];
                $creator->StartTransform();
                $creator->Rotate(90);
                $creator->Rect(-$photocellPositionY, $photocellPositionX, $photoCell['width'], $photoCell['height'], 'F');
                $creator->StopTransform();
            }
        }
    }

    public function addLaserTriggers()
    {
        $triggerWidth = $this->parameters->getLaserTriggerWidth();
        $triggerHeight = $this->parameters->getLaserTriggerHeight();
        $triggerPositionX = $this->parameters->getLaserTriggerPositionX() === 'right' ? $this->parameters->getSheetWidth() - $triggerWidth : 0;
        $dieCutsContext = strpos(get_class($this), 'DieCutRenderer') > -1;
        if ($dieCutsContext) {
            $this->pdfCreator->setDrawColor(0, 0, 255);
            $this->pdfCreator->setFillColor(255, 255, 255);
        } else {
            $this->pdfCreator->setDrawColor(0, 0, 0);
            $this->pdfCreator->setFillColor(0, 0, 0);
        }

        for ($i = 0; $i < $this->parameters->getNumberOfRows(); $i++) {
            $pIdx = count($this->dieCutParameters) / $this->parameters->getNumberOfRows() * $i;
            $triggerPositionY = $this->dieCutParameters[$pIdx]['positionY'] + $this->parameters->getSlope();
            if ($this->parameters->getLaserTriggerPositionY() === 'bottom') {
                $triggerPositionY += ($this->dieCutParameters[$pIdx]['height']  - $this->parameters->getSlope()*2 - $triggerHeight);
            }
            $this->pdfCreator->Rect($triggerPositionX, $triggerPositionY, $triggerWidth, $triggerHeight, $dieCutsContext ? '' : 'F');
        }
    }
}
