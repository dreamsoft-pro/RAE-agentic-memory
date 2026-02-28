<?php

namespace DreamSoft\Controllers\Components;

use DreamSoft\Core\Component;


class OptionsFilter extends Component
{
    public function __construct()
    {
        parent::__construct();
    }

    public function matchOptions($allOptions, $filterParts, $currentLang, $prepareFilter = false)
    {
        $matchPart = ['name'];
        $matchExact = ['category', 'group', 'paper_type'];
        $matchRangeSlider = ['weight', 'whiteness', 'thickness', 'opacity', 'roughness'];
        $matchArrays = ['certificates', 'printingTechniques', 'color_hex', 'application'];

        if ($prepareFilter) {
            $filterConsolidated = [];
            foreach ($filterParts as $part) {
                if (!$filterConsolidated[$part['name']]) {
                    $filterConsolidated[$part['name']] = ['name' => $part['name']];
                }
                if (array_search($part['name'], $matchArrays) !== false) {
                    if (!$filterConsolidated[$part['name']]['selectedValues']) {
                        $filterConsolidated[$part['name']]['selectedValues'] = [];
                    }
                    $filterConsolidated[$part['name']]['selectedValues'][] = $part['value'];
                } else if ($part['valueType'] == 'exact') {
                    $filterConsolidated[$part['name']]['value'] = $part['value'];
                } else if ($part['valueType'] == 'min') {
                    $filterConsolidated[$part['name']]['minValue'] = $part['value'];
                } else if ($part['valueType'] == 'max') {
                    $filterConsolidated[$part['name']]['maxValue'] = $part['value'];
                }
            }
            $filterParts = $filterConsolidated;
        }
        foreach ($allOptions as &$option) {
            foreach ($option['descriptions'] as $key => &$description) {
                if (array_search($key, $matchArrays) !== false || array_search($key, $matchExact) !== false) {
                    $description = array_map(function ($item) {
                        return trim($item);
                    }, preg_split('/,/', $description));
                }
            }
            $option['descriptions']['thickness']=$option['sizePage'];
            $option['descriptions']['weight']=$option['weight'];
        }

        $filteredOptions = array_filter($allOptions,
            function ($item) use ($filterParts, $matchPart, $currentLang, $matchRangeSlider, $matchArrays, $matchExact) {
                $pass = true;
                foreach ($filterParts as $part) {
                    $partName = $part['name'];
                    $filterValue = $filterParts[$partName]['value'];
                    if (array_search($partName, $matchPart) !== false && $filterValue) {
                        $pass = $item['names'][$currentLang] && strstr(strtolower($item['names'][$currentLang]), strtolower($filterValue)) !== false;
                    } else if (array_search($partName, $matchRangeSlider) !== false
                        && $item['descriptions'][$partName]) {
                        $description = $item['descriptions'][$partName];
                        $pass = $description >= $filterParts[$partName]['minValue']
                            && $description <= $filterParts[$partName]['maxValue'];
                    } else if (array_search($partName, $matchArrays) !== false && $item['descriptions'][$partName]) {
                        foreach ($filterParts[$partName]['selectedValues'] as $val) {
                            $pass = $pass && array_search($val, $item['descriptions'][$partName]) !== false;
                        }
                    } else if (array_search($partName, $matchExact) !== false && $item['descriptions'][$partName] && $filterValue) {
                        $pass = array_search($filterValue, $item['descriptions'][$partName]) !== false;
                    }
                    if (!$pass) {
                        break;
                    }
                }
                return $pass;
            });
        return $filteredOptions;
    }
}
