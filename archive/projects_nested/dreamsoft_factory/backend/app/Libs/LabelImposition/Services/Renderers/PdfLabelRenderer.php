<?php
declare(strict_types=1);

namespace DreamSoft\Libs\LabelImposition\Services\Renderers;

use DreamSoft\Libs\LabelImposition\DTO\ImpositionPdfParameters;
use DreamSoft\Libs\LabelImposition\Services\Calculator;
use DreamSoft\Libs\LabelImposition\Services\LabelFilePreparer;
use DreamSoft\Libs\LabelImposition\Traits\BarcodesTrait;
use DreamSoft\Libs\LabelImposition\Traits\NamingSchemeTrait;
use DreamSoft\Libs\LabelImposition\Traits\ParametersValidator;
use DreamSoft\Libs\LabelImposition\Traits\PdfResponseTrait;
use setasign\Fpdi\Tcpdf\Fpdi;

class PdfLabelRenderer implements RendererInterface
{
    use PdfResponseTrait;
    use ParametersValidator;
    use BarcodesTrait;
    use NamingSchemeTrait;

    private Fpdi $pdfCreator;
    private int $sumLabelsOnSheet = 0;
    private array $imageSize;
    private string $preparedImage;

    private array $dieCutParameters;

    public function __construct(
        private ImpositionPdfParameters $parameters,
        private array                   $fileInfo,
    )
    {
        $this->initializePdfCreator();
        $this->dieCutParameters = [];
        $this->preparedImage = $this->preparePdf();
        $this->pdfCreator->setSourceFile($this->preparedImage);
        $this->imageSize = $this->getSize($this->preparedImage);
        $this->calculator = new Calculator($this->parameters, $this->imageSize);
        $this->initializeAnother();
        $this->validateParameters($this->parameters, $this->calculator);
    }

    private function initializePdfCreator(): void
    {
        $this->pdfCreator = new Fpdi();
        $this->pdfCreator->setPrintHeader(false);
        $this->pdfCreator->setAutoPageBreak(false);
        $this->pdfCreator->setPrintFooter(false);
    }

    private function preparePdf(): string
    {
        if ($this->parameters->getLabelRotation() == 0) {
            return $this->fileInfo['path'];
        }

        $rotationAngle = $this->parameters->getLabelRotation();
        $pdf = new Fpdi();
        $pdf->setPrintHeader(false);
        $pdf->setAutoPageBreak(false);
        $pdf->setPrintFooter(false);
        $pdf->setSourceFile($this->fileInfo['path']);

        $page = $pdf->importPage(1);
        $size = $pdf->getImportedPageSize($page);

        if ($rotationAngle == 90 || $rotationAngle == 270) {
            $size = ['width' => $size['height'], 'height' => $size['width']];
        }

        if ($size['width'] > $size['height']) {
            $pdf->AddPage('L', [$size['width'], $size['height']]);
        } else {
            $pdf->AddPage('P', [$size['width'], $size['height']]);
        }

        $pdf->Rotate($rotationAngle, $size['width'] / 2, $size['height'] / 2);
        $inscribedRadius = $this->calculateInscribedCircleRadius($size['width'], $size['height']);

        if ($rotationAngle == 90 || $rotationAngle == 270) {
            $pdf->useTemplate($page, -1 * $inscribedRadius, $inscribedRadius);
        } else {
            $pdf->useTemplate($page);
        }

        $rotatedPdfPath = $this->parameters->getOutputDir() . '/' . uniqid('prepared_', true) . '.pdf';
        $pdf->Output($rotatedPdfPath, 'F');

        return $rotatedPdfPath;
    }

    public function rotate(string $imageUrl, int $rotate = 0): string
    {
        // @TODO: Implement this method
        return '';
    }

    private function calculateInscribedCircleRadius($side_a, $side_b): float
    {
        $side_difference = abs($side_a - $side_b);
        return $side_difference / 2;
    }

    public function getSize(string $filePath): array
    {
        $templateId = $this->pdfCreator->importPage(1);
        $pageSize = $this->pdfCreator->getTemplateSize($templateId);

        return [
            'width' => $pageSize['width'] - 1, /*@TODO: to remove after rotation add*/
            'height' => $pageSize['height'],
        ];
    }

    public function __destruct()
    {

    }

    private function prepareDieCut(string $fileName):string
    {
        $dieCutRenderer = new DieCutRenderer($this->parameters,
            [
                'orientation' => $this->calculator->getPageOrientation(),
                'format' => [
                    $this->calculator->calculateSheetLength(),
                    $this->parameters->getSheetWidth(),
                ]
            ],
            $this->dieCutParameters);

        return $dieCutRenderer->render($fileName);
    }

    public function render(): array
    {
        $dieCutFileName=$this->parameters->getFileNamePrefix().'die_cut' . LabelFilePreparer::dateName()  . '.pdf';
        $this->parameters->setDieCutFileName($dieCutFileName);
        $this->pdfCreator->AddPage(
            $this->calculator->getPageOrientation(),
            [
                $this->calculator->calculateSheetLength(),
                $this->parameters->getSheetWidth(),
            ]
        );

        if (!empty($this->parameters->getBarcodes())) {
            $this->addBarcode();
        }

        if (!empty($this->parameters->getQrCodes())) {
            $this->addQr($this->pdfCreator);
        }

        if (!empty($this->parameters->getPhotoCells())) {
            $this->addPhotocell($this->pdfCreator);
        }

        $this->addLabelsToPage();

        if ($this->parameters->getShowLaserTriggers()) {
            $this->addLaserTriggers();
        }
        $anotherFile = $this->finalizeAnother($this->parameters->getOutputDirPrint());

        return $this->makeResponse(
            $this->calculator,
            $this->pdfCreator,
            $this->sumLabelsOnSheet,
            $this->prepareDieCut($dieCutFileName),
            $this->parameters->getOutputDirPrint(),
            $anotherFile,
            $this->parameters->getFileNamePrefix(),
        );
    }

    private function addLabelsToPage(): void
    {
        $positionY = $this->calculator->getStartedPositionY();
        for ($row = 0; $row < $this->parameters->getNumberOfRows(); $row++) {
            $this->renderRow($positionY);
            $positionY += $this->parameters->getLabelDistance() + $this->imageSize['height'];
        }
    }

    private function renderRow(float $positionY): void
    {
        $positionX = $this->calculator->calculateStartedMarginX();
        $templateId = $this->pdfCreator->importPage(1);
        for ($i = 0; $i < $this->calculator->calculateColumnsNumber(); $i++) {
            $this->sumLabelsOnSheet++;
            $this->pdfCreator->useTemplate($templateId, $positionX, $positionY, $this->imageSize['width'], $this->imageSize['height']);
            $this->setDieCutParameters($positionX, $positionY, $this->imageSize['width'], $this->imageSize['height']);
            $positionX += $this->calculator->calculateMarginX() + $this->imageSize['width'];
        }
    }

    private function setDieCutParameters(float $positionX, float $positionY, float $width, float $height): void
    {
        $this->dieCutParameters[] = [
            'positionX' => $positionX,
            'positionY' => $positionY,
            'width' => $width,
            'height' => $height,
        ];
    }
}
