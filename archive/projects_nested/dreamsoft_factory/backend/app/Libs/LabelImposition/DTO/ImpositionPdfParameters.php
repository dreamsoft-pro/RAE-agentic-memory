<?php

namespace DreamSoft\Libs\LabelImposition\DTO;

class ImpositionPdfParameters
{
    private string $labelUrl;
    private string $outputDir;
    private ?int $numberOfColumns;
    private ?int $numberOfRows;
    private ?int $minSheetLength;
    private ?int $sheetWidth;
    private ?int $labelDistance;
    private ?int $variant;
    private ?int $labelRotation;
    private ?float $columnsDistance;

    private array $barCodes;
    private array $qrCodes;
    private array $photoCells;
    private int $rounding;
    private ?string $cuttingDieFile;
    private int $anotherSignFile;
    private ?int $slope;
    private ?int $showLaserTriggers;
    private $fileNamePrefix;
    private ?string $laserTriggerPositionX;
    private ?string $laserTriggerPositionY;
    private int $laserTriggerWidth;
    private int $laserTriggerHeight;
    private ?int $qrCodeAnotherSignFilePositionX;
    private ?int $qrCodeAnotherSignFilePositionY;
    private ?int $photocellAnotherSignFilePositionX;
    private ?int $photocellAnotherSignFilePositionY;
    private int $barcodeEnabled;
    private int $qrCodeEnabled;
    private int $photocellEnabled;
    private string $outputDirPrint;
    private string $outputDirCut;
    private string $outputDirPdf;
    private int $copyToSpecialFolders;
    private string $dieCutFileName;
    private bool $drawEllipse;

    public function __construct(array $params)
    {
        $this->labelUrl = $params['labelUrl'];
        $this->outputDir = $params['outputDir'];
        $this->outputDirPrint = $params['outputDirPrint'];
        $this->outputDirCut = $params['outputDirCut'];
        $this->outputDirPdf = $params['outputDirPdf'];
        $this->numberOfColumns = (int)($params['numberOfColumns'] ?? null);
        $this->numberOfRows = $params['numberOfRows'];
        $this->minSheetLength = $params['minSheetLength'];
        $this->sheetWidth = $params['sheetWidth'];
        $this->labelDistance = $params['labelDistance'];
        $this->labelRotation = $params['labelRotation'];
        $this->columnsDistance = (float)($params['columnsDistance'] ?? null);
        $this->barCodes = $params['barcodes'] ?? [];
        $this->qrCodes = $params['qrcodes'] ?? [];
        $this->photoCells = $params['photocells'] ?? [];
        $this->rounding = $params['rounding'] ?? 0;
        $this->cuttingDieFile = $params['cuttingDieFile'];
        $this->anotherSignFile = $params['anotherSignFile'] ?? 0;
        $this->slope = $params['slope'];
        $this->showLaserTriggers = $params['showLaserTriggers'] ?? 0;
        $this->barcodeEnabled = $params['barcodeEnabled'] ?? 0;
        $this->qrCodeEnabled = $params['qrCodeEnabled'] ?? 0;
        $this->photocellEnabled = $params['photocellEnabled'] ?? 0;
        $this->laserTriggerPositionX = $params['laserTriggerPositionX'];
        $this->laserTriggerPositionY = $params['laserTriggerPositionY'];
        $this->laserTriggerWidth = $params['laserTriggerWidth'] ?? 4;
        $this->laserTriggerHeight = $params['laserTriggerHeight'] ?? 8;
        $this->qrCodeAnotherSignFilePositionX = $params['qrCodeAnotherSignFilePositionX'];
        $this->qrCodeAnotherSignFilePositionY = $params['qrCodeAnotherSignFilePositionY'];
        $this->photocellAnotherSignFilePositionX = $params['photocellAnotherSignFilePositionX'];
        $this->photocellAnotherSignFilePositionY = $params['photocellAnotherSignFilePositionY'];
        $this->fileNamePrefix = $params['fileNamePrefix'];
        $this->copyToSpecialFolders = (int)$params['copyToSpecialFolders'];
        $this->drawEllipse = $params['drawEllipse']??false;

    }

    public function getLabelUrl(): string
    {
        return $this->labelUrl;
    }

    public function getOutputDir(): string
    {
        return $this->outputDir;
    }

    public function getNumberOfColumns(): ?int
    {
        return $this->numberOfColumns;
    }

    public function getNumberOfRows(): int
    {
        return $this->numberOfRows;
    }

    public function getMinSheetLength(): int
    {
        return $this->minSheetLength;
    }

    public function getSheetWidth(): int
    {
        return $this->sheetWidth;
    }

    public function getLabelDistance(): int
    {
        return $this->labelDistance;
    }

    public function getVariant(): int
    {
        return $this->variant;
    }

    public function getLabelRotation(): int
    {
        return $this->labelRotation;
    }

    public function getColumnsDistance(): ?float
    {
        return $this->columnsDistance;
    }

    public function getBarcodes(): array
    {
        return $this->barCodes;
    }

    public function getQrCodes(): array
    {
        return $this->qrCodes;
    }

    public function getPhotoCells(): array
    {
        return $this->photoCells;
    }

    public function getRounding(): int
    {
        return $this->rounding;
    }

    public function getCuttingDieFile(): string
    {
        return $this->cuttingDieFile;
    }

    public function getAnotherSignFile(): int
    {
        return $this->anotherSignFile;
    }

    public function getSlope(): ?int
    {
        return $this->slope;
    }

    public function getShowLaserTriggers(): ?int
    {
        return $this->showLaserTriggers;
    }

    public function getFileNamePrefix(): string
    {
        return $this->fileNamePrefix;
    }

    public function getLaserTriggerPositionX(): ?string
    {
        return $this->laserTriggerPositionX;
    }

    public function getLaserTriggerPositionY(): ?string
    {
        return $this->laserTriggerPositionY;
    }

    public function getLaserTriggerWidth(): int
    {
        return $this->laserTriggerWidth;
    }

    public function getLaserTriggerHeight(): int
    {
        return $this->laserTriggerHeight;
    }

    public function getQrCodeAnotherSignFilePositionX(): ?int
    {
        return $this->qrCodeAnotherSignFilePositionX;
    }

    public function getQrCodeAnotherSignFilePositionY(): ?int
    {
        return $this->qrCodeAnotherSignFilePositionY;
    }

    public function getPhotocellAnotherSignFilePositionX(): ?int
    {
        return $this->photocellAnotherSignFilePositionX;
    }

    public function getPhotocellAnotherSignFilePositionY(): ?int
    {
        return $this->photocellAnotherSignFilePositionY;
    }

    public function getBarcodeEnabled(): int
    {
        return $this->barcodeEnabled;
    }

    public function getQrCodeEnabled(): mixed
    {
        return $this->qrCodeEnabled;
    }

    public function getPhotocellEnabled(): mixed
    {
        return $this->photocellEnabled;
    }

    public function getOutputDirPrint(): string
    {
        return $this->outputDirPrint;
    }

    public function getOutputDirCut(): string
    {
        return $this->outputDirCut;
    }

public function getOutputDirPdf(): string
    {
        return $this->outputDirPdf;
    }

    public function getCopyToSpecialFolders(): int
    {
        return $this->copyToSpecialFolders;
    }

    public function setDieCutFileName(string $dieCutFileName)
    {
        $this->dieCutFileName=$dieCutFileName;
    }

    public function getDieCutFileName(): string
    {
        return $this->dieCutFileName;
    }

    public function isDrawEllipse(): bool
    {
        return $this->drawEllipse;
    }


}

