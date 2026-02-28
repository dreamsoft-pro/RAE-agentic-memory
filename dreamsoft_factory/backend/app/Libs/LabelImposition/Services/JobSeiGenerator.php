<?php

namespace DreamSoft\Libs\LabelImposition\Services;

use DreamSoft\Libs\LabelImposition\Traits\NamingSchemeTrait;
use DreamSoft\Models\Order\DpOrder;
use Exception;
use SimpleXMLElement;

/**
 * Plik lasera
 */
class JobSeiGenerator
{
    use NamingSchemeTrait;
    private string $baseXml='<?xml version="1.0" encoding="utf-8"?>
<JobSEI>
<Meta>
<Description>Empty Script</Description>
<Creation Author="A.B.C." Date="2016-09-27T10:14:21" Version="Preliminary" />
<Thumbnail Format="PNG" Data="ABAgMEBQYHCAoA==" />
</Meta>
<ZoneDivision>AUTO</ZoneDivision>
<ZoneDimension Width="150" />
<LabelMaster>
<ModuleStep>54</ModuleStep>
</LabelMaster>
<Material Name="Generic">
<Library>PAPER</Library>
</Material>
<Object Name="Printela1">
<!-- -->
<File Type="PDF" Unit="MM">C:\JOBS\CUT LASER QRcode-1.PDF</File>
<!-- -->
<Rotate Angle="0" Ref="C"/>
<Optimize>Full</Optimize>
</Object>
</JobSEI>';
    private array $data;

    public function generate($path, $fileNamePrefix, $copyToSpecialFolders)
    {
        $root = new SimpleXMLElement($this->baseXml);

        $creation=$root->xpath('//Creation')[0];
        $creation->attributes()['Date']=$this->data['dpOrder']['modified'];

        $object=$root->xpath('//Object')[0];
        $object->attributes()['Name']=$this->data['cutFileName'];

        $file=$root->xpath('//File')[0];
        $file[0]='C:\\JOBS\\'.$this->data['cutFileName'];

        $zoneDimension=$root->xpath('//ZoneDimension')[0];
        $zoneDimension->attributes()['Width']=$this->data['sheetWidth'];

        $moduleStep=$root->xpath('//ModuleStep')[0];
        $moduleStep[0]=$this->data['moduleStep'];

        $libraryMaterial=$root->xpath('//Library')[0];
        $libraryMaterial[0]=$this->data['material'];

        $rotate=$root->xpath('//Rotate')[0];
        $rotate->attributes()['Angle']=$this->data['rotationAngle'];

        $fileName = $fileNamePrefix . 'die_cut'.LabelFilePreparer::dateName() . '.xml';
        $res = $root->asXML($path . $fileName);
        if (!$res) {
            throw new Exception('Xml file not saved');
        }
        if($copyToSpecialFolders) {
            $this->copyFileToRaw($path . $fileName);
        }
        return $fileName;
    }
    public function setData(array $array)
    {
        $this->data=$array;
    }

}
