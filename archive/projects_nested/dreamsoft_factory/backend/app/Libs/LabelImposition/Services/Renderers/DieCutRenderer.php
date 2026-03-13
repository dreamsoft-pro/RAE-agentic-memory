<?php

declare(strict_types=1);

namespace DreamSoft\Libs\LabelImposition\Services\Renderers;

use DreamSoft\Libs\LabelImposition\DTO\ImpositionPdfParameters;
use DreamSoft\Libs\LabelImposition\Services\Calculator;
use DreamSoft\Libs\LabelImposition\Traits\BarcodesTrait;
use DreamSoft\Libs\LabelImposition\Traits\NamingSchemeTrait;
use setasign\Fpdi\Tcpdf\Fpdi;

class DieCutRenderer
{
    use BarcodesTrait;
    use NamingSchemeTrait;

    public function __construct(
        private ImpositionPdfParameters $parameters,
        private array                   $pageParameters,
        private array                   $dieCutParameters,
    )
    {
        $this->pdfCreator = new Fpdi();
        $this->pdfCreator->setPrintHeader(false);
        $this->pdfCreator->setAutoPageBreak(false);
        $this->pdfCreator->setPrintFooter(false);
        $this->prepareDiesCutFile();
    }

    public function render($fileName): string
    {
        $this->pdfCreator->AddPage(
            $this->pageParameters['orientation'],
            $this->pageParameters['format'],
        );
        $this->pdfCreator->startLayer('CUT');

        if ($this->parameters->getCuttingDieFile()) {
            $this->pdfCreator->setSourceFile($this->parameters->getCuttingDieFile());
            $templateId = $this->pdfCreator->importPage(1);
        }
        $this->pdfCreator->setDrawColor(255, 0, 0);
        foreach ($this->dieCutParameters as $dieCutParameter) {

            if ($this->parameters->getCuttingDieFile()) {
                $this->pdfCreator->useTemplate($templateId, $dieCutParameter['positionX'], $dieCutParameter['positionY'], $dieCutParameter['width'], $dieCutParameter['height']);
            } else {
                if ($this->parameters->getRounding() > 0) {
                    $w = $dieCutParameter['width'] - 2 * $this->parameters->getSlope();
                    $h = $dieCutParameter['height'] - 2 * $this->parameters->getSlope();
                    $rounding = $this->parameters->getRounding();
                    $rounding = min($rounding, $w / 2, $h / 2);
                    $this->pdfCreator->RoundedRect($dieCutParameter['positionX'] + $this->parameters->getSlope(),
                        $dieCutParameter['positionY'] + $this->parameters->getSlope(),
                        $w,
                        $h,
                        $rounding);
                } else if ($this->parameters->isDrawEllipse()) {
                    $this->pdfCreator->Ellipse(
                        $dieCutParameter['positionX'] + $this->parameters->getSlope() + $dieCutParameter['width'] / 2,
                        $dieCutParameter['positionY'] + $dieCutParameter['height'] / 2,
                        $dieCutParameter['width'] / 2 - $this->parameters->getSlope(),
                        $dieCutParameter['height'] / 2 - $this->parameters->getSlope()
                    );
                } else {
                    $this->pdfCreator->Rect($dieCutParameter['positionX'] + $this->parameters->getSlope(), $dieCutParameter['positionY'] + $this->parameters->getSlope(), $dieCutParameter['width'] - 2 * $this->parameters->getSlope(), $dieCutParameter['height'] - 2 * $this->parameters->getSlope(), $dieCutParameter['height']);
                }
            }

        }
        if ($this->parameters->getShowLaserTriggers()) {
            $this->addLaserTriggers();
        }
        $this->pdfCreator->endLayer();
        $path = MAIN_UPLOAD . companyID . '/' . $this->parameters->getOutputDirCut() . $fileName;
        $this->pdfCreator->Output($path, 'F');
        if ($this->parameters->getCopyToSpecialFolders()) {
            $this->copyFileToRaw($path);
        }
        return $fileName;
    }

    private function prepareDiesCutFile()
    {
        if (!$this->parameters->getCuttingDieFile()) {
            return;
        }
        if ($this->parameters->getLabelRotation() == 0) {
            return $this->parameters->getCuttingDieFile();
        }

        $rotationAngle = $this->parameters->getLabelRotation();
        $pdf = new Fpdi();
        $pdf->setPrintHeader(false);
        $pdf->setAutoPageBreak(false);
        $pdf->setPrintFooter(false);
        $pdf->setSourceFile($this->parameters->getCuttingDieFile());

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
        $inscribedRadius = abs($size['width'] - $size['height']) / 2;

        if ($rotationAngle == 90 || $rotationAngle == 270) {
            $pdf->useTemplate($page, -1 * $inscribedRadius, $inscribedRadius);
        } else {
            $pdf->useTemplate($page);
        }

        $rotatedPdfPath = $this->parameters->getOutputDir() . uniqid('prepared_', true) . '.pdf';
        $pdf->Output($rotatedPdfPath, 'F');

        return $rotatedPdfPath;
    }
}
