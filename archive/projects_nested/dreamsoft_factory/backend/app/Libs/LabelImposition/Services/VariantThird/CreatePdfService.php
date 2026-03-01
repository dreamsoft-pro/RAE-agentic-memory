<?php

namespace DreamSoft\Libs\LabelImposition\Services\VariantThird;

use DreamSoft\Libs\LabelImposition\DTO\ImpositionPdfParameters;
use DreamSoft\Libs\LabelImposition\Services\CreatePdfServiceInterface;
use DreamSoft\Libs\LabelImposition\Services\LabelFilePreparer;
use DreamSoft\Libs\LabelImposition\Services\Renderers\ImageLabelRenderer;
use DreamSoft\Libs\LabelImposition\Services\Renderers\PdfLabelRenderer;
use InvalidArgumentException;

class CreatePdfService implements CreatePdfServiceInterface
{
    private ImageLabelRenderer|PdfLabelRenderer $labelRenderer;
    private array $fileInfo;


    public function __construct(
        protected readonly ImpositionPdfParameters $parameters,
    )
    {
        $labelItemPreparer = new LabelFilePreparer();
        $this->fileInfo = [
            'path' => $this->parameters->getLabelUrl(),
            'type' => $labelItemPreparer->checkMimeType($this->parameters->getLabelUrl())
        ];

        try {
            $this->checkMimeType();
        } catch (InvalidArgumentException $e) {
            echo $e->getMessage();
            exit;
        }

    }

    private function checkMimeType(): void
    {
        if ($this->fileInfo['type'] === 'image') {
            $this->labelRenderer = new ImageLabelRenderer($this->parameters);
        } elseif ($this->fileInfo['type'] === 'pdf') {
            $this->labelRenderer = new PdfLabelRenderer($this->parameters, $this->fileInfo);
        } else {
            throw new InvalidArgumentException('Unsupported file type');
        }
    }

    public function createPdf(): array
    {
        return $this->labelRenderer->render();
    }

    public function __destruct()
    {
    }
}
