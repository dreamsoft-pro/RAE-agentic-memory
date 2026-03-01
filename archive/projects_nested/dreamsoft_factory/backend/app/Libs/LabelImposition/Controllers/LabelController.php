<?php

namespace DreamSoft\Libs\LabelImposition\Controllers;

use DreamSoft\Libs\LabelImposition\DTO\ImpositionPdfParameters;
use DreamSoft\Libs\LabelImposition\Requests\RequestInterface;
use DreamSoft\Libs\LabelImposition\Services\VariantThird\CreatePdfService as VariantThirdService;
use InvalidArgumentException;

class LabelController
{

    public function __construct(private readonly RequestInterface $request)
    {
    }

    public function __invoke(): void
    {
        try {
            $impositionPdfParameters = new ImpositionPdfParameters($this->request->getParams());
            $pdfService = new VariantThirdService($impositionPdfParameters);

            $pdfData = $pdfService->createPdf();

            echo json_encode($pdfData, JSON_THROW_ON_ERROR);
        } catch (InvalidArgumentException $e) {
            echo json_encode(
                [
                    'success' => false,
                    'error' => $e->getMessage()
                ], JSON_THROW_ON_ERROR);
        }
    }
}
