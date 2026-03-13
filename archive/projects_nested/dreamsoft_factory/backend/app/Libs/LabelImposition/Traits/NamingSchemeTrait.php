<?php

namespace DreamSoft\Libs\LabelImposition\Traits;


trait NamingSchemeTrait
{
    public function copyFileToRaw($path)
    {
        $parts = explode('/', $path);
        $type = $parts[count($parts) - 4];
        if(str_contains($path,'.pdf') && $type === 'print'){
            $newDirName='DURST-pdf';
        }else if($type === 'print'){
            $newDirName= 'DURST';
        }else{
            $newDirName =  'SEILASER';
        }

        $newDir = join('/', array_splice($parts, 0, -4));
        $newDir .= '/' . $newDirName;
        if (!is_dir($newDir)) {
            mkdir($newDir, 0755);
            chmod($newDir, 0755);
        }
        $res = copy($path, $newDir.'/'.$parts[count($parts)-1]);
        if (!$res) {
            throw new \Exception('File no copied');
        }
    }
}
