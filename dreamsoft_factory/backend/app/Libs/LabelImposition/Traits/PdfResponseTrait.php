<?php

namespace DreamSoft\Libs\LabelImposition\Traits;

use DreamSoft\Libs\LabelImposition\Services\Calculator;
use DreamSoft\Libs\LabelImposition\Services\LabelFilePreparer;

trait PdfResponseTrait
{
    public function makeResponse(Calculator $calculator, $pdfObject, int $sumLabelsOnSheet, string $dieCutFilename,
                                 string $outputDir, ?string $anotherSignFile, string $fileNamePrefix): array
    {
        $fileName = $fileNamePrefix . 'imposition' . LabelFilePreparer::dateName() . '.pdf';
        $fullPath=MAIN_UPLOAD . companyID . '/' .$outputDir . $fileName;
        $pdfObject->Output($fullPath, 'F');
        if($this->parameters->getCopyToSpecialFolders()) {
            $this->copyFileToRaw($fullPath);
        }
        return [
            'fileName' =>  $fileName,
            'sumLabelsOnSheet' => $sumLabelsOnSheet,
            'sheetLengthInMm' => $calculator->calculateSheetLength(),
            'sheetSurfaceInSquareMm' => $calculator->calculateSheetSurface(),
            'dieCutFileName' => $dieCutFilename,
            'anotherSignFile' => $anotherSignFile,
            'moduleStep' => $calculator->getImageSize()['height']+$calculator->getParameters()->getLabelDistance(),
        ];
    }
}
