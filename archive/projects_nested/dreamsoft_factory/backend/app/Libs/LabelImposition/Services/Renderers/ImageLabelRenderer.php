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

class ImageLabelRenderer implements RendererInterface
{
    use PdfResponseTrait;
    use ParametersValidator;
    use BarcodesTrait;
    use NamingSchemeTrait;

    private const DPI = 300;
    private Fpdi $pdfCreator;
    private int $sumLabelsOnSheet = 0;
    private Calculator $calculator;
    private array $imageSize;
    private string $preparedImage;

    private array $dieCutParameters;

    public function __construct(
        private ImpositionPdfParameters $parameters,
    )
    {
        $this->pdfCreator = new Fpdi();
        $this->pdfCreator->setPrintHeader(false);
        $this->pdfCreator->setAutoPageBreak(false);
        $this->pdfCreator->setPrintFooter(false);

        $this->dieCutParameters = [];
        $this->preparedImage = $this->rotate($this->parameters->getLabelUrl(), $this->parameters->getLabelRotation());
        $this->imageSize = $this->getSize($this->preparedImage);
        $this->calculator = new Calculator($this->parameters, $this->imageSize);
        $this->initializeAnother();
        $this->validateParameters($this->parameters, $this->calculator);
    }

    public function rotate(string $imageUrl, int $rotate = 0): string
    {
        $image = imagecreatefromstring(file_get_contents($imageUrl));

        $rotatedImage = imagerotate($image, $rotate, 0);

        $tempFileName = tempnam(sys_get_temp_dir(), 'rotated_image_') . '.jpg';
        imagejpeg($rotatedImage, $tempFileName, 100);

        imagedestroy($image);
        imagedestroy($rotatedImage);

        return $tempFileName;
    }

    public function getSize(string $filePath): array
    {
        $imageSize = getimagesize($filePath);
        $width = self::pxToMm($imageSize[0]);
        $height = self::pxToMm($imageSize[1]);

        return [
            'width' => $width,
            'height' => $height,
        ];
    }

    private static function pxToMm($pxSize): float
    {
        return ($pxSize / self::DPI) * 25.4;
    }

    public function render(): array
    {
        $dieCutFileName=$this->parameters->getFileNamePrefix().'die_cut' . LabelFilePreparer::dateName()  . '.pdf';
        $this->parameters->setDieCutFileName($dieCutFileName);
        $this->pdfCreator->AddPage(
            $this->calculator->getPageOrientation(),
            [
                $this->calculator->calculateSheetLength(),
                $this->parameters->getSheetWidth()
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
            $this->parameters->getFileNamePrefix()
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

        for ($i = 0; $i < $this->calculator->calculateColumnsNumber(); $i++) {
            $this->pdfCreator->Image(
                $this->preparedImage,
                $positionX,
                $positionY,
                $this->imageSize['width'],
                $this->imageSize['height']
            );
            $this->setDieCutParameters($positionX, $positionY, $this->imageSize['width'], $this->imageSize['height']);
            $this->sumLabelsOnSheet++;
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

    private function prepareDieCut(string $fileName): string
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
}
