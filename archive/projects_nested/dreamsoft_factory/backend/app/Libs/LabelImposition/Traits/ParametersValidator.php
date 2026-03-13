<?php

namespace DreamSoft\Libs\LabelImposition\Traits;

use DreamSoft\Libs\LabelImposition\DTO\ImpositionPdfParameters;
use DreamSoft\Libs\LabelImposition\Services\Calculator;
use InvalidArgumentException;

trait ParametersValidator
{
    private function validateParameters(
        ImpositionPdfParameters $parameters,
        Calculator              $calculator
    ): void
    {
        if ($calculator->calculateOverallColumnWidth() > $parameters->getSheetWidth()) {
            throw new InvalidArgumentException('The overall elements width(' . $calculator->calculateOverallColumnWidth() . ' mm) of the columns is greater than the sheet width (' . $parameters->getSheetWidth() . ' mm)');
        }

        if ($calculator->calculateSheetLength() < $parameters->getMinSheetLength()) {
            throw new InvalidArgumentException('The sheet length (' . $calculator->calculateSheetLength() . ' mm) is less than the minimum sheet length (' . $parameters->getMinSheetLength() . ' mm)');
        }
    }
}
