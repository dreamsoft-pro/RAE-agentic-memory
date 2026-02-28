<?php

namespace DreamSoft\Libs\LabelImposition\Services;

use DreamSoft\Libs\LabelImposition\DTO\ImpositionPdfParameters;

class Calculator
{
    public function __construct(
        private readonly ImpositionPdfParameters $parameters,
        private readonly array                   $imageSize
    )
    {
    }

    public function getPageOrientation(): string
    {
        return $this->calculateSheetLength() < $this->parameters->getSheetWidth() ? 'L' : 'P';
    }

    public function getPageOrientationQr(): string
    {
        return $this->getSheetLengthQr() < $this->parameters->getSheetWidth() ? 'L' : 'P';
    }

    public function calculateSheetLength(): float
    {
        return $this->parameters->getLabelDistance() + ($this->parameters->getNumberOfRows() * $this->imageSize['height']) + ($this->parameters->getNumberOfRows() - 1) * $this->parameters->getLabelDistance();
    }

    public function getSheetLengthQr()
    {
        $calc = $this->calculateSheetLength();
        return $calc < 500 ? 500 : $calc;
    }
    public function getStartedPositionY(): float
    {
        return $this->parameters->getLabelDistance() / 2;
    }

    public function calculateStartedMarginX(): float
    {
        return ($this->parameters->getSheetWidth() - ($this->calculateOverallColumnWidth() - $this->calculateMarginX())) / 2;
    }

    public function calculateOverallColumnWidth(): float
    {
        return $this->calculateColumnsNumber() * ($this->imageSize['width'] + ($this->calculateMarginX()));
    }

    public function calculateColumnsNumber(): int
    {
        $columnsDistance = $this->parameters->getColumnsDistance();
        $labelDistance = $this->parameters->getLabelDistance();
        $signsWidth = $this->calculateSignsWidth();
        $sheetWidth = $this->parameters->getSheetWidth();
        $imageWidth = $this->imageSize['width'];

        if ($numberOfColumns = $this->parameters->getNumberOfColumns()) {
            return $numberOfColumns;
        }

        if ($columnsDistance && $columnsDistance > $signsWidth) {
            $labelWidth = $imageWidth + $columnsDistance;
            $sheetWidth -= $columnsDistance;
        } elseif (($columnsDistance && $columnsDistance < $signsWidth) || (!$columnsDistance && $signsWidth > 0)) {
            $labelWidth = $imageWidth + $signsWidth;
            $sheetWidth -= $signsWidth;
        } else {
            $labelWidth = $imageWidth + $labelDistance;
            $sheetWidth -= $labelDistance;
        }

        return (int)floor($sheetWidth / $labelWidth);
    }

    public function calculateSignsWidth(): float
    {
        $codesHeights=[];
        if($this->parameters->getBarcodeEnabled()){
            $codesHeights[]=$this->parameters->getBarcodes()[0]['height'];
        }
        if($this->parameters->getQrCodeEnabled() && !$this->parameters->getAnotherSignFile()){
            $codesHeights[]=$this->parameters->getQrCodes()[0]['height'];
        }
        if($this->parameters->getPhotocellEnabled()){
            $codesHeights[]=$this->parameters->getPhotoCells()[0]['height'];
        }
        if($this->parameters->getShowLaserTriggers()){
            $codesHeights[]=$this->parameters->getLaserTriggerHeight();
        }
        if (empty($codesHeights)) {
            return 0;
        }

        return max($codesHeights);
    }

    public function calculateMarginX(): float
    {
        if ($this->parameters->getColumnsDistance()) {
            return $this->parameters->getColumnsDistance();
        }

        $totalLabelWidth = $this->calculateColumnsNumber() * $this->imageSize['width'];
        $remainingWidth = $this->parameters->getSheetWidth() - $totalLabelWidth;

        return $remainingWidth / ($this->calculateColumnsNumber() + 1);
    }

    public function calculateSheetSurface(): float
    {
        return $this->parameters->getSheetWidth() * $this->calculateSheetLength();
    }

    public function getImageSize(){
        return $this->imageSize;
    }
    public function getParameters(){
        return $this->parameters;
    }
}
