<?php

namespace DreamSoft\Controllers\Calculate;

use DreamSoft\Controllers\Components\Price;
use DreamSoft\Core\Controller;
use DreamSoft\Models\Delivery\DeliveryName;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttribute;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOption;
use DreamSoft\Models\PrintShopProduct\PrintShopGroup;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeLanguage;
use DreamSoft\Models\Behaviours\ProductManipulation;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeTax;
use DreamSoft\Models\Tax\Tax;
use DreamSoft\Models\Setting\Setting;
use DreamSoft\Models\PrintShop\PrintShopComplex;
use DreamSoft\Controllers\Components\FormatAssistant;
use DreamSoft\Controllers\Components\OptionAssistant;
use DreamSoft\Models\PrintShopProduct\PrintShopPage;
use DreamSoft\Controllers\Components\DescriptionAssistant;
use DreamSoft\Controllers\Components\DeliveryAssistant;
use DreamSoft\Libs\TwigExtensions\TranslateExtension;
use DreamSoft\Controllers\Components\CalculateAssistant;
use DreamSoft\Models\PrintShop\PrintShopRealizationTimeLanguage;
use DreamSoft\Models\PrintShopProduct\PrintShopFormat;
use DreamSoft\Models\PrintShopProduct\PrintShopFormatName;
use DreamSoft\Models\Content\StaticContent;
use DreamSoft\Models\Content\StaticContentLang;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeDescription;
use DreamSoft\Models\PrintShopProduct\PrintShopOption;
use DreamSoft\Models\Template\TemplateSetting;
use Spipu\Html2Pdf\Exception\Html2PdfException;
use Spipu\Html2Pdf\Html2Pdf;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;
use Twig\Loader\FilesystemLoader;
use Twig\Environment as Twig_Environment;

class CalculateController extends Controller
{
    public $useModels = [];
    
    private $PrintShopGroup;
    private $PrintShopType;
    private $PrintShopTypeLanguage;
    private $ProductManipulation;
    private $PrintShopTypeTax;
    private $Tax;
    private $Setting;
    private $PrintShopComplex;
    private $FormatAssistant;
    private $PrintShopPage;
    private $OptionAssistant;
    private $DescriptionAssistant;
    private $DeliveryAssistant;
    private $TemplateSetting;
    private $CalculateAssistant;
    private $DeliveryName;
    private $Price;
    private $PrintShopConfigAttribute;
    private $PrintShopConfigOption;
    private $PrintShopRealizationTimeLanguage;
    private $PrintShopFormat;
    private $PrintShopFormatName;
    private $StaticContent;
    private $StaticContentLang;
    private $PrintShopTypeDescription;
    private $PrintShopOption;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopGroup = PrintShopGroup::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->PrintShopTypeLanguage = PrintShopTypeLanguage::getInstance();
        $this->ProductManipulation = ProductManipulation::getInstance();
        $this->PrintShopTypeTax = PrintShopTypeTax::getInstance();
        $this->Tax = Tax::getInstance();
        $this->Setting = Setting::getInstance();
        $this->PrintShopComplex = PrintShopComplex::getInstance();
        $this->FormatAssistant = FormatAssistant::getInstance();
        $this->PrintShopPage = PrintShopPage::getInstance();
        $this->OptionAssistant = OptionAssistant::getInstance();
        $this->DescriptionAssistant = DescriptionAssistant::getInstance();
        $this->DeliveryAssistant = DeliveryAssistant::getInstance();
        $this->TemplateSetting = TemplateSetting::getInstance();
        $this->CalculateAssistant = CalculateAssistant::getInstance();
        $this->DeliveryName = DeliveryName::getInstance();
        $this->Price = Price::getInstance();
        $this->PrintShopConfigAttribute = PrintShopConfigAttribute::getInstance();
        $this->PrintShopConfigOption = PrintShopConfigOption::getInstance();
        $this->PrintShopRealizationTimeLanguage = PrintShopRealizationTimeLanguage::getInstance();
        $this->PrintShopFormat = PrintShopFormat::getInstance();
        $this->PrintShopFormatName = PrintShopFormatName::getInstance();
        $this->StaticContent = StaticContent::getInstance();
        $this->StaticContentLang = StaticContentLang::getInstance();
        $this->PrintShopTypeDescription = PrintShopTypeDescription::getInstance();
        $this->PrintShopOption = PrintShopOption::getInstance();
    }

    public function setDomainID($domainID)
    {
        parent::setDomainID($domainID);
        $this->OptionAssistant->setDomainID($domainID);
        $this->TemplateSetting->setDomainID($domainID);
        $this->CalculateAssistant->setDomainID($domainID);
        $this->Setting->setDomainID($domainID);
        $this->StaticContent->setDomainID($domainID);
        $this->PrintShopTypeTax->setDomainID($domainID);
        $this->ProductManipulation->setDomainID($domainID);
    }

    public function index($typeID)
    {
        $typeEntity = $this->PrintShopType->get('ID', $typeID);
        if (!$typeEntity) {
            return $this->sendFailResponse('06');
        }
        
        $group = $this->PrintShopGroup->customGet($typeEntity['groupID']);
        $type = $this->prepareType($typeEntity);

        $taxes = $this->getTaxesForProduct($group['ID'], $type['ID']);
        $typeDescriptions = $this->getTypeDescriptions($group['ID'], $type['ID']);
        $complex = $type['complex'] ? $this->getComplex($type['ID']) : $this->prepareComplex($type);

        $formats = [];
        $pages = [];
        $selectOptions = [];
        
        foreach ($complex as $row) {
            if ($row['products']) {
                foreach ($row['products'] as $product) {
                    $formats[$product['typeID']] = $this->getFormats($product['groupID'], $product['typeID'], $type['ID']);
                    $pages[$product['typeID']] = $this->getPages($product['groupID'], $product['typeID']);
                    $selectOptions[$product['typeID']] = $this->getSelectOptions($product['typeID']);
                }
            }
        }

        $params = [];
        $currency = DEFAULT_CURRENCY;
        $deliveries = $this->DeliveryAssistant->getDeliveries($params, $currency);

        return compact(
            'group',
            'type',
            'taxes',
            'complex',
            'formats',
            'pages',
            'selectOptions',
            'typeDescriptions',
            'deliveries'
        );
    }

    private function prepareType($typeEntity)
    {
        if (!$typeEntity) {
            return $this->sendFailResponse('06');
        }

        $ID = $typeEntity['ID'];
        $this->PrintShopType->setGroupID($typeEntity['groupID']);
        $data = $this->PrintShopType->get('ID', $ID);
        if (!$data) {
            return $this->sendFailResponse('06');
        }
        
        $languages = $this->PrintShopTypeLanguage->get('typeID', $ID, true);
        $category = $this->ProductManipulation->selectCategory($typeEntity['groupID'], $ID);
        $group = $this->PrintShopGroup->customGet($typeEntity['groupID']);

        foreach ($languages as $value) {
            $data['names'][$value['lang']] = $value['name'];
            $data['icons'][$value['lang']] = $value['icon'];
            $data['slugs'][$value['lang']] = $value['slug'];
        }
        $data['category'] = $category;
        $data['group']['slugs'] = $group['slugs'];
        
        return $data;
    }

    private function getTaxesForProduct($groupID, $typeID)
    {
        if (!$typeID) {
            return [];
        }

        $selected = $this->PrintShopTypeTax->getByType($typeID) ?: $this->PrintShopTypeTax->getByGroup($groupID);
        $data = [];
        
        foreach ($selected as $taxID) {
            $tax = $this->Tax->customGet($taxID, 1);
            if ($this->Setting->getValue('defaultTax') == $taxID) {
                $tax['default'] = 1;
            }
            $data[] = $tax;
        }

        return $data;
    }

    private function getComplex($typeID)
    {
        $this->PrintShopComplex->setTypeID($typeID);
        return $this->PrintShopComplex->getAll() ?: [];
    }

    private function prepareComplex($type)
    {
        $type['typeID'] = $type['ID'];
        return [
            [
                'ID' => $type['ID'],
                'name' => $type['name'],
                'products' => [$type]
            ]
        ];
    }

    private function getFormats($groupID, $typeID, $complexID)
    {
        try {
            return $this->FormatAssistant->formats($groupID, $typeID, $complexID, NULL, 1) ?: [];
        } catch (\Exception $exception) {
            $this->debug($exception->getMessage());
            return [];
        }
    }

    private function getPages($groupID, $typeID)
    {
        $this->PrintShopPage->setGroupID($groupID);
        $this->PrintShopPage->setTypeID($typeID);
        return $this->PrintShopPage->getAll() ?: [];
    }

    private function getSelectOptions($typeID)
    {
        return $this->OptionAssistant->getSelectOptions($typeID) ?: [];
    }

    private function getTypeDescriptions($groupID, $typeID)
    {
        return $this->DescriptionAssistant->getTypeDescriptions($groupID, $typeID) ?: [];
    }

    private function printOfferData($params)
    {
        $params['limitedVolumes'] = 1;

        $data = $this->CalculateAssistant->prepareRealizationTimes($params);

        $deliveriesAggregate = [];
        $sumDeliveryPrice = 0;
        $sumDeliveryPriceGross = 0;
        
        foreach ($params['productAddresses'] as $productAddress) {
            $deliveriesAggregate[] = $productAddress['deliveryID'];
            $sumDeliveryPrice += floatval(str_replace(',', '.', $productAddress['price']));
            $sumDeliveryPriceGross += floatval(str_replace(',', '.', $productAddress['priceGross']));
        }

        $selectedDeliveries = [];
        $dNames = $this->DeliveryName->getNames($deliveriesAggregate);
        
        foreach ($deliveriesAggregate as $ID) {
            $selectedDeliveries[] = $dNames[$ID];
        }
        
        $data['selectedDeliveries'] = $selectedDeliveries;
        $data['sumDeliveryPrice'] = $this->Price->getPriceToView($sumDeliveryPrice);
        $data['sumDeliveryPriceGross'] = $this->Price->getPriceToView($sumDeliveryPrice);

        $price = $priceGross = 0;
        
        foreach ($data['volumes'] as $key => $volume) {
            if ($volume['calculation']['volume'] == $params['activeVolume']) {
                $price = floatval(str_replace(',', '.', $volume['calculation']['price']));
                $priceGross = floatval(str_replace(',', '.', $volume['calculation']['priceBrutto']));
            }
            $unitPrice = floatval(str_replace(',', '.', $volume['calculation']['price'])) / $volume['calculation']['volume'];
            $unitPriceGross = floatval(str_replace(',', '.', $volume['calculation']['priceBrutto'])) / $volume['calculation']['volume'];
            $data['volumes'][$key]['calculation']['unitPrice'] = $this->Price->getPriceToView($unitPrice * 100);
            $data['volumes'][$key]['calculation']['unitPriceGross'] = $this->Price->getPriceToView($unitPriceGross * 100);
        }

        $data['totalPrice'] = $this->Price->getPriceToView(($price + $sumDeliveryPrice) * 100);
        $data['totalPriceGross'] = $this->Price->getPriceToView(($priceGross + $sumDeliveryPriceGross) * 100);
        $data['activeVolume'] = $params['activeVolume'];
        $data['amount'] = $params['amount'];

        $types = $this->PrintShopType->customGetByList([$params['typeID']]);
        $data['type'] = current($types);

        $aggregateAttributes = [];
        $aggregateOptions = [];
        $aggregateTypes = [];
        
        foreach ($params['products'] as $product) {
            $aggregateTypes[] = $product['typeID'];
            foreach ($product['options'] as $row) {
                $aggregateAttributes[] = $row['attrID'];
                $aggregateOptions[] = $row['optID'];
            }
        }

        $attributes = $this->prepareAttributeNames($aggregateAttributes);
        $options = $this->prepareOptionNames($aggregateOptions);

        $productOptions = $this->PrintShopOption->getSelectedOptionSorted($params['typeID'], $aggregateOptions);

        foreach ($productOptions as $productOptionKey => $productOption) {
            $options[$productOptionKey]['invisible'] = $productOption['invisible'];
        }

        $typeLanguages = $this->prepareTypeLanguages($aggregateTypes);

        foreach ($params['products'] as $productKey => $product) {
            foreach ($product['options'] as $optionKey => $row) {
                $params['products'][$productKey]['options'][$optionKey]['attribute'] = $attributes[$row['attrID']] ?? null;
                $params['products'][$productKey]['options'][$optionKey]['option'] = $options[$row['optID']] ?? null;
            }
        }

        $selectedRealisationTime = array_filter($data['realisationTimes'], function ($realisationTime) use ($params) {
            return $realisationTime['ID'] == $params['realizationTimeID'];
        });

        $data['realisationTimeDate'] = $selectedRealisationTime['date'] ?? null;

        foreach ($selectedRealisationTime['volumes'] as $volume) {
            if ($volume['volume'] == $params['activeVolume'] && $volume['date']) {
                $data['realisationTimeDate'] = $volume['date'];
            }
        }

        $types = $this->PrintShopType->getByList($aggregateTypes);

        foreach ($params['products'] as $productKey => $product) {
            $params['products'][$productKey]['format'] = $this->PrintShopFormat->customGet($product['formatID']);
            $customNames = $this->PrintShopFormatName->getByType($product['typeID']);
            $params['products'][$productKey]['typeLanguage'] = $typeLanguages[$product['typeID']] ?? [];
            $params['products'][$productKey]['type'] = $types[$product['typeID']] ?? [];
            if ($customNames) {
                $sortedCustomNames = array_column($customNames, 'name', 'lang');
                $params['products'][$productKey]['format']['customNames'] = $sortedCustomNames;
            }
        }

        $data['products'] = $params['products'];
        $data['staticText'] = $this->prepareStaticText('static.print_offer');

        $imagesFromGallery = $this->prepareImagesFromGallery($params['typeID']);
        $data['imageFromGallery'] = is_array($imagesFromGallery) ? current($imagesFromGallery) : [];

        return $data;
    }

    private function printOfferHTML($data)
    {
        $loader = new FilesystemLoader(STATIC_PATH . 'templates');
        $twig = new Twig_Environment($loader, ['auto_reload' => true]);
        $twig->addExtension(new TranslateExtension());

        $templateID = 119;
        $templateName = 'print-offer';
        $templateSetting = $this->TemplateSetting->getOne($templateID, 1);

        $templatePath = 'default/' . $templateID . '/' . $templateName . '.html';
        if ($templateSetting && $templateSetting['source'] == 1) {
            $templatePath = companyID . '/' . $templateID . '/' . $templateName . '.html';
        } elseif ($templateSetting && $templateSetting['source'] == 2) {
            $templatePath = companyID . '/' . $templateID . '/' . $this->getDomainID() . '/' . $templateName . '.html';
        }

        $template = $twig->load($templatePath);
        $logoFile = MAIN_UPLOAD . 'uploadedFiles/' . companyID . '/logos/' . $this->getDomainID() . '/logo';

        return $template->render([
            'logoPath' => $logoFile,
            'offerDate' => date(DATE_FORMAT),
            'print_offer_text' => 'test',
            'lang' => lang,
            'selectedDeliveries' => $data['selectedDeliveries'],
            'currency' => $data['currency'],
            'totalPrice' => $data['totalPrice'],
            'totalPriceGross' => $data['totalPriceGross'],
            'activeVolume' => $data['activeVolume'],
            'volumes' => $data['volumes'],
            'type' => $data['type'],
            'complexProducts' => $data['products'],
            'amount' => $data['amount'],
            'realisationTimeDate' => $data['realisationTimeDate'],
            'tax' => $data['tax'],
            'staticText' => $data['staticText'],
            'imageFromGallery' => $data['imageFromGallery']
        ]);
    }

    private function generate($params)
    {
        try {
            $html2pdf = new Html2Pdf('P', 'A4', 'pl', true, 'UTF-8');
            $html2pdf->setTestTdInOnePage(false);
            $html2pdf->addFont('freesans', 'regular', BASE_DIR . 'libs/tcpdf/fonts/freesans.php');
            $html2pdf->setDefaultFont('freesans');

            $printOfferData = $this->printOfferData($params);
            $content = $this->printOfferHTML($printOfferData);

            $html2pdf->writeHTML($content);
            $outputFolder = date('Y-m-d');
            $path = MAIN_UPLOAD . 'tmp/' . $outputFolder . '/print_offer.pdf';
            
            if (!is_dir(MAIN_UPLOAD . 'tmp/' . $outputFolder)) {
                mkdir(MAIN_UPLOAD . 'tmp/' . $outputFolder, 0777, true);
            }

            $html2pdf->Output($path, 'F');
            $link = STATIC_URL . 'tmp/' . $outputFolder . '/print_offer.pdf';
            return ['path' => $path, 'invoiceData' => $printOfferData, 'link' => $link, 'success' => true];
        } catch (Html2PdfException $e) {
            return ['info' => $e->getMessage(), 'error' => true, 'response' => false];
        }
    }

    public function patch_printOffer()
    {
        $post = $this->Data->getAllPost();
        $generated = $this->generate($post);
        return $generated['success'] ? $generated : $this->sendFailResponse('13');
    }

    private function prepareAttributeNames($aggregateAttributes)
    {
        return $this->PrintShopConfigAttribute->customGetByList($aggregateAttributes) ?: [];
    }

    private function prepareOptionNames($aggregateOptions)
    {
        return $this->PrintShopConfigOption->customGetByList($aggregateOptions) ?: [];
    }

    private function prepareTypeLanguages($aggregateTypes)
    {
        $languages = $this->PrintShopTypeLanguage->getByList($aggregateTypes) ?: [];
        $result = [];
        foreach ($languages as $language) {
            $result[$language['typeID']][$language['lang']] = $language['name'];
        }
        return $result;
    }

    private function prepareStaticText($key)
    {
        $printOfferContent = $this->StaticContent->get('key', $key);
        $languages = $this->StaticContentLang->get('staticContentID', $printOfferContent['ID'], true) ?: [];
        foreach ($languages as $language) {
            $printOfferContent['content'][$language['lang']] = $language['content'];
        }
        return $printOfferContent;
    }

    private function prepareImagesFromGallery($typeID, $descType = 5)
    {
        $data = $this->PrintShopTypeDescription->customGetAll($typeID) ?: [];
        $firstGalleryDescription = current(array_filter($data, function ($description) use ($descType) {
            return $description['descType'] == $descType;
        }));

        $fileFolder = UPLOADED_FILES_DIR . '/';
        $thumbFolder = UPLOADED_FILES_DIR . '/' . companyID . '/thumbs/';

        $files = [];
        if (isset($firstGalleryDescription['descID'])) {
            $files = $this->PrintShopTypeDescription->getFilesByList([$firstGalleryDescription['descID']]);
        }

        foreach ($files as $descID => $fls) {
            foreach ($fls as $kf => $f) {
                $files[$descID][$kf]['path'] = MAIN_UPLOAD . $fileFolder . companyID . '/' . $f['path'];
                $files[$descID][$kf]['pathThumb'] = MAIN_UPLOAD . $thumbFolder . $f['path'];
            }
        }

        return current($files);
    }
}
