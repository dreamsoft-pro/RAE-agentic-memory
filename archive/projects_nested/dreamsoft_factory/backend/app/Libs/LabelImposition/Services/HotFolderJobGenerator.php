<?php

namespace DreamSoft\Libs\LabelImposition\Services;

use DreamSoft\Libs\LabelImposition\Traits\NamingSchemeTrait;
use DreamSoft\Models\Order\DpOrder;
use Exception;
use SimpleXMLElement;

class HotFolderJobGenerator
{
    use NamingSchemeTrait;

    private string $baseXml = '<HotfolderJob>
	
	<ProductionJob name="Numer zamówienia" comment="Nazwa własna jeśli występuje" externalId="EXT123" leadIn="0" leadOut="0" shippingDate="Data realizacji" productionDate="Data realizacji">
				    
		<ImposeTemplate internalName=""/>
		
		<Cutter internalName="">
				<CutterParameterSet internalName=""/>
		</Cutter>
		
		<PrintItem name="" comment="" width="25.0" height="15.0" unit="mm" pages="1" numberOfCopies="1" url="" >				
		</PrintItem>		
	  
	</ProductionJob>

</HotfolderJob>';
    private array $data;

    public function generate($path, $fileNamePrefix, $copyToSpecialFolders)
    {
        $root = new SimpleXMLElement($this->baseXml);
        $this->assignData($root);
        $fileName = $fileNamePrefix . 'HotFolderJob' . LabelFilePreparer::dateName() . '.xml';
        $res = $root->asXML($path . $fileName);
        if (!$res) {
            throw new Exception('Xml file not saved');
        }
        if ($copyToSpecialFolders) {
            $this->copyFileToRaw($path . $fileName);
        }
        return $fileName;
    }

    public function setData(array $array)
    {
        $this->data = $array;
    }

private function assignData(SimpleXMLElement $root)
{
    $productionJob = $root->xpath('//ProductionJob')[0];

    // Wyodrębnij nazwę pliku z URL
    $filePath = $this->data['fileURL'];
    $fileName = basename($filePath);  // Wyodrębnia nazwę pliku z pełnej ścieżki

    // Ustawienie nazwy produkcji na nazwę pliku
    $productionJob->attributes()['name'] = $fileName;
    $productionJob->attributes()['comment'] = $this->data['dpProduct']['name'];
    $productionJob->attributes()['shippingDate'] = $productionJob->attributes()['productionDate'] = $this->data['psUserCalc']['realisationDate'];
    $productionJob->attributes()['externalId'] = $this->data['dpOrder']['orderNumber'];

    $printItem1 = $root->xpath('//PrintItem')[0];
    $printItem1->attributes()['width'] = $this->data['sheetWidth'];
    $printItem1->attributes()['height'] = $this->data['moduleStep'];
    $printItem1->attributes()['url'] = 'file:///C:/colorpress-durst-pdf/'.$filePath;
    $printItem1->attributes()['numberOfCopies'] = $this->data['numberOfCopies'];
}
}
