<?php

namespace DreamSoft\Libs;
class DataUtils
{
    /**
     * @param $rows array Ascending sorted, fields: volume, value
     * @param $volume
     * @return int|mixed
     */
    public static function linearApproximation($rows, $volume)
    {
        if (!is_array($rows) || count($rows) == 0 || !is_numeric($volume) || $volume == 0) {
            return 0;
        } else if (count($rows) == 1) {
            return $rows[0]['value'];
        } else if (count($rows) == 2) {
            if ($volume <= $rows[0]['volume']) {
                return DataUtils::linearApproximation([$rows[0]], $volume);
            } else if ($volume >= $rows[1]['volume']) {
                return DataUtils::linearApproximation([$rows[1]], $volume);
            }
            $slope = ($rows[1]['value'] - $rows[0]['value']) / ($rows[1]['volume'] - $rows[0]['volume']);
            return $rows[0]['value'] + ($volume - $rows[0]['volume']) * $slope;
        } else {
            for ($i = 0; $i < count($rows); $i += 2) {
                if ($i < count($rows) - 1) {
                    if ($rows[$i]['volume'] <= $volume && $rows[$i + 1]['volume'] >= $volume) {
                        return DataUtils::linearApproximation([$rows[$i], $rows[$i + 1]], $volume);
                    } else if ($volume < $rows[$i]['volume']) {
                        return DataUtils::linearApproximation([$rows[$i]], $volume);
                    }
                } else {
                    return DataUtils::linearApproximation([$rows[$i]], $volume);
                }
            }
        }
    }

    /**
     * @param $array
     * @param $compareOnFields string|array
     * @return array
     */
    public static function uniqueRecords($array, $compareOnFields)
    {
        $uniqueValues = [];
        if (!is_array($compareOnFields)) {
            $compareOnFields = [$compareOnFields];
        }
        return array_filter($array, function ($item) use (&$uniqueValues, $compareOnFields) {
            $itemFieldValue = '';
            foreach ($compareOnFields as $fieldName) {
                $itemFieldValue .= $item[$fieldName];
            }
            $exists = in_array($itemFieldValue, $uniqueValues);
            if (!$exists) {
                $uniqueValues[] = $itemFieldValue;
                return true;
            }
            return false;
        });
    }

    public static function langVersions(&$item)
    {
        $list = preg_split("/\|\|/", $item['langs']);
        $langs = [];
        foreach ($list as $langLabel) {
            $parts = preg_split("/::/", $langLabel);
            $langs[$parts[0]] = ['name' => $parts[1]];
        }
        $item['langs'] = $langs;
    }
    public static function groupConcatToTree($text)
    {
        $all=[];
        $list = preg_split("/\|\|/", $text);
        foreach ($list as $item) {
            $parts = preg_split("/::/", $item);
            $all[$parts[0]] = $parts[1];
        }
       return $all;
    }

    public static function includeLanguageTables($items, $langFields){
        $result = [];
        foreach ($items as $row) {

            $key = $row['ID'];
            if (!isset($result[$key])) {
                $result[$key] = array();
            }
            $result[$key] = array_merge($result[$key], $row);
            foreach($langFields as $langField){
                $lLang = $lName = null;
                if (!empty($row[$langField[0]])) {
                    $lLang = $row[$langField[0]];
                    $lName = $row[$langField[1]];
                }
                unset($row[$langField[0]]);
                unset($row[$langField[1]]);

                if (!empty($lLang)) {
                    if (!isset($result[$key][$langField[2]])) {
                        $result[$key][$langField[2]] = array();
                    }
                    $result[$key][$langField[2]][$lLang] = $lName;
                }
            }

        }
        return $result;
    }

}
