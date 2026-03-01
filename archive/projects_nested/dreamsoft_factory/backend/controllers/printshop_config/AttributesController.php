<?php

use DreamSoft\Controllers\Components\OptionsFilter;
use DreamSoft\Controllers\Components\Uploader;
use DreamSoft\Core\Controller;
use DreamSoft\Models\Order\DpProductReportFile;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttribute;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttributeDescriptionLang;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttributeLang;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttributeNature;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttributeRange;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigAttributeType;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigDetailPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigExclusion;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigIncrease;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOption;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionDescription;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigOptionLang;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPaperPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigPrice;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigRealizationTime;
use DreamSoft\Models\PrintShopProduct\PrintShopAttributeName;
use DreamSoft\Models\PrintShopProduct\PrintShopProductAttributeSetting;
use DreamSoft\Models\PrintShopProduct\PrintShopOption;
use DreamSoft\Models\ProductionPath\OperationOption;
use DreamSoft\Models\PrintShopConfig\PrintShopRelativeOptionsFilter;
use DreamSoft\Models\Upload\UploadFile;
use Spipu\Html2Pdf\Exception\Html2PdfException;
use Spipu\Html2Pdf\Html2Pdf;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;
use Twig\Loader\FilesystemLoader;
use Twig\Environment as Twig_Environment;
use DreamSoft\Libs\TwigExtensions\TranslateExtension;
use DreamSoft\Models\Template\TemplateSetting;
use DreamSoft\Models\PrintShop\PrintShopComplex;
use DreamSoft\Models\PrintShopProduct\PrintShopType;

/**
 * Description of AttributesController
 *
 * @class AttributesController
 * @author Rafał
 */
class AttributesController extends Controller
{

    public $useModels = array();

    /**
     * @var PrintShopConfigAttribute
     */
    protected $PrintShopConfigAttribute;
    /**
     * @var PrintShopConfigAttributeLang
     */
    protected $PrintShopConfigAttributeLang;
    /**
     * @var PrintShopConfigAttributeDescriptionLang
     */
    protected $PrintShopConfigAttributeDescriptionLang;
    /**
     * @var PrintShopConfigAttributeRange
     */
    protected $PrintShopConfigAttributeRange;
    /**
     * @var PrintShopConfigOption
     */
    protected $PrintShopConfigOption;
    /**
     * @var PrintShopConfigOptionLang
     */
    protected $PrintShopConfigOptionLang;
    /**
     * @var PrintShopOption
     */
    protected $PrintShopOption;
    /**
     * @var PrintShopConfigAttributeType
     */
    protected $PrintShopConfigAttributeType;
    /**
     * @var PrintShopConfigAttributeNature
     */
    protected $PrintShopConfigAttributeNature;
    /**
     * @var PrintShopConfigRealizationTime
     */
    protected $PrintShopConfigRealizationTime;
    /**
     * @var PrintShopConfigPrice
     */
    protected $PrintShopConfigPrice;
    /**
     * @var PrintShopConfigDetailPrice
     */
    protected $PrintShopConfigDetailPrice;
    /**
     * @var PrintShopConfigExclusion
     */
    protected $PrintShopConfigExclusion;
    /**
     * @var OperationOption
     */
    protected $OperationOption;
    /**
     * @var PrintShopConfigIncrease
     */
    protected $PrintShopConfigIncrease;
    /**
     * @var PrintShopConfigPaperPrice
     */
    protected $PrintShopConfigPaperPrice;
    /**
     * @var PrintShopAttributeName
     */
    protected $PrintShopAttributeName;
    /**
     * @var PrintShopProductAttributeSetting
     */
    protected $PrintShopProductAttributeSetting;
    /**
     * @var PrintShopConfigOptionDescription
     */
    private $PrintShopConfigOptionDescription;
    /**
     * @var UploadFile
     */
    private $UploadFile;
    /**
     * @var Uploader
     */
    private $Uploader;
    /**
     * @var OptionsFilter
     */
    private $OptionsFilter;

    /**
     * @var PrintShopRelativeOptionsFilter
     */
    private $PrintShopRelativeOptionsFilter;
    /**
     * @var TemplateSetting
     */
    private $TemplateSetting;
    /**
     * @var string
     */
    protected $iconFolder;
    /**
     * AttributesController constructor.
     * @param $params
     */
    protected $PrintShopComplex;
    protected $PrintShopType;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->PrintShopConfigAttribute = PrintShopConfigAttribute::getInstance();
        $this->PrintShopConfigAttributeLang = PrintShopConfigAttributeLang::getInstance();
        $this->PrintShopConfigAttributeDescriptionLang = PrintShopConfigAttributeDescriptionLang::getInstance();
        $this->PrintShopConfigAttributeRange = PrintShopConfigAttributeRange::getInstance();
        $this->PrintShopConfigOption = PrintShopConfigOption::getInstance();
        $this->PrintShopConfigOptionLang = PrintShopConfigOptionLang::getInstance();
        $this->PrintShopOption = PrintShopOption::getInstance();
        $this->PrintShopConfigAttributeType = PrintShopConfigAttributeType::getInstance();
        $this->PrintShopConfigAttributeNature = PrintShopConfigAttributeNature::getInstance();
        $this->PrintShopConfigRealizationTime = PrintShopConfigRealizationTime::getInstance();
        $this->PrintShopConfigPrice = PrintShopConfigPrice::getInstance();
        $this->PrintShopConfigDetailPrice = PrintShopConfigDetailPrice::getInstance();
        $this->PrintShopConfigExclusion = PrintShopConfigExclusion::getInstance();
        $this->OperationOption = OperationOption::getInstance();
        $this->PrintShopConfigIncrease = PrintShopConfigIncrease::getInstance();
        $this->PrintShopConfigPaperPrice = PrintShopConfigPaperPrice::getInstance();
        $this->PrintShopAttributeName = PrintShopAttributeName::getInstance();
        $this->PrintShopProductAttributeSetting = PrintShopProductAttributeSetting::getInstance();
        $this->PrintShopConfigOptionDescription = PrintShopConfigOptionDescription::getInstance();
        $this->OptionsFilter = OptionsFilter::getInstance();
        $this->PrintShopRelativeOptionsFilter = PrintShopRelativeOptionsFilter::getInstance();
        $this->TemplateSetting = TemplateSetting::getInstance();
        $this->PrintShopComplex = PrintShopComplex::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->UploadFile = UploadFile::getInstance();
        $this->Uploader = Uploader::getInstance();
        $this->iconFolder = 'uploadedFiles/' . companyID . '/attributesIcons/';

    }

    /**
     * @param null $ID
     * @return array|bool
     */
    public function attribute($ID = NULL)
    {
        if (intval($ID) > 0) {
            $data = $this->PrintShopConfigAttribute->customGet($ID);
        } else {
            $data = $this->PrintShopConfigAttribute->getAll();
            if ($data) {
                $data =  $this->fillImages($data, 'iconID','iconUrl',$this->iconFolder);
            }
        }

        if (empty($data)) {
            $data = array();
        }
        return $data;

    }

    /**
     * @return array|bool
     */
    public function post_attribute()
    {
        $name = $this->Data->getPost('name');
        $iconID = $this->Data->getPost('iconID');
        $type = $this->Data->getPost('type');
        $natureID = $this->Data->getPost('natureID');

        $minPages = $this->Data->getPost('minPages');
        $step = $this->Data->getPost('step');
        $maxPages = $this->Data->getPost('maxPages');

        $adminName = $this->Data->getPost('adminName');

        $names = $this->Data->getPost('names');
        $description = $this->Data->getPost('description');
        $multipleOptionsMax = $this->Data->getPost('multipleOptionsMax') ?? 0;
        $displayImageOnMiniature = $this->Data->getPost('displayImageOnMiniature') ?? 0;
        $specialFunction = $this->Data->getPost('specialFunction') ?? null;

        if (($name || $names) && $type) {
            if ($minPages && $step) {
                $params['step'] = $step;
                $params['maxPages'] = (intval($maxPages) > 0) ? $maxPages : NULL;
                $params['minPages'] = $minPages;
                $params['iconID'] = $iconID;
                $rangeID = $this->PrintShopConfigAttributeRange->create($params);
            } else {
                $rangeID = NULL;
            }
            $lastID = $this->PrintShopConfigAttribute->customCreate($name, $type, $natureID, $rangeID, $adminName,
                $multipleOptionsMax, $displayImageOnMiniature,$specialFunction);

            if (!empty($names)) {
                foreach ($names as $lang => $name) {
                    $res = $this->PrintShopConfigAttributeLang->set($lang, $name, $lastID);
                    if (!$res) {
                        $return = $this->sendFailResponse('09');
                        return $return;
                    }
                }
            }

            foreach ($description as $lang => $desc){
                $this->PrintShopConfigAttributeDescriptionLang->set($lang,$description,$lastID);
            }

            $return = $this->PrintShopConfigAttribute->customGet($lastID);
            if (!$return) {
                $return['response'] = false;
            }
            $languages = $this->PrintShopConfigAttributeLang->get('attributeID', $lastID, true);
            if (!empty($languages)) {
                $return['names'] = array();
                foreach ($languages as $each) {
                    $return['names'][$each['lang']] = $each['name'];
                }
            }
            return $return;
        } else {
            $return = $this->sendFailResponse('01');
            return $return;
        }
    }

    /**
     * @return array
     */
    public function put_attribute()
    {

        $post = $this->Data->getAllPost();

        if (isset($post['ID']) && !empty($post['ID'])) {
            $ID = $post['ID'];
            unset($post['ID']);
        } else {
            $return = $this->sendFailResponse('01');
            return $return;
        }

        $currentAttr = $this->PrintShopConfigAttribute->customGet($ID);

        if (isset($post['minPages']) && $post['minPages'] !== NULL &&
            isset($post['step']) && !empty($post['step'])) {
            if ($currentAttr['rangeID'] == NULL) {
                $params['step'] = $post['step'];
                $params['iconID'] = $post['iconID'];
                $params['maxPages'] = (intval($post['maxPages']) > 0) ? $post['maxPages'] : NULL;
                $params['minPages'] = $post['minPages'];
                $rangeID = $this->PrintShopConfigAttributeRange->create($params);
                $this->PrintShopConfigAttribute->setRangeID($ID, $rangeID);
            } else {
                if (isset($post['step'])) {
                    $this->PrintShopConfigAttributeRange->update($currentAttr['rangeID'], 'step', $post['step']);
                }
                if (isset($post['minPages'])) {
                    $this->PrintShopConfigAttributeRange->update($currentAttr['rangeID'], 'minPages', $post['minPages']);
                }
                if (isset($post['maxPages'])) {
                    $this->PrintShopConfigAttributeRange->update($currentAttr['rangeID'], 'maxPages', $post['maxPages']);
                }
            }
        } else {
            if ($currentAttr['rangeID'] != NULL) {
                $this->PrintShopConfigAttributeRange->delete('ID', $currentAttr['rangeID']);
                $this->PrintShopConfigAttribute->setRangeID($ID, NULL);
            }
        }
        $post['specialFunction']=$post['specialFunction']==''?null:$post['specialFunction'];
        $res = $this->PrintShopConfigAttribute->customUpdate($ID, $post['name'], $post['iconID'], $post['type'], $post['natureID'], $post['adminName'], $post['multipleOptionsMax'], $post['displayImageOnMiniature'], $post['specialFunction']);
        if ($res) {
            $return['response'] = true;
        } else {
            $return['response'] = false;
            return $return;
        }

        if (!empty($post['names'])) {
            foreach ($post['names'] as $lang => $name) {
                $res = $this->PrintShopConfigAttributeLang->set($lang, $name, $ID);
                if (!$res) {
                    $return = $this->sendFailResponse('09');
                    return $return;
                }
            }
        }

        foreach ($post['description'] as $lang => $description){
            $this->PrintShopConfigAttributeDescriptionLang->set($lang,$description,$ID);
        }

        return $return;

    }

    /**
     * @param $ID
     * @return mixed
     */
    public function delete_attribute($ID)
    {
        if (intval($ID) > 0) {
            $attr = $this->PrintShopConfigAttribute->customGet($ID);
            if ($attr['rangeID'] != null) {
                $this->PrintShopConfigAttributeRange->delete('ID', $attr['rangeID']);
            }
            $deleted = $this->PrintShopConfigAttribute->delete('ID', $ID);
            if ($deleted) {
                $data['infoAttr'] = 'Remove Attribute';
                $this->PrintShopConfigOption->setAttrID($ID);
                $allOptions = $this->PrintShopConfigOption->getAll();
                if (!empty($allOptions) && is_array($allOptions)) {
                    $count = count($allOptions);
                    $data['infoOpt'] = 'Count option: ' . $count . '.';
                    $i = 0;
                    $iOpt = 0;
                    $iPrices = 0;
                    $iDetailPrices = 0;
                    $iRealizationTimes = 0;
                    $iExclusions = 0;
                    $iOperations = 0;
                    $iIncreases = 0;
                    $data['attrID'] = $ID;
                    foreach ($allOptions as $ao) {
                        if ($this->PrintShopConfigOption->delete('ID', $ao['ID'])) {
                            $i++;
                            $data['optID'] = $ao['ID'];
                            $allProductOptions = $this->PrintShopOption->getAllInProduct($ID, $ao['ID']);
                            $data['dumpAll'] = $allProductOptions;
                            if (!empty($allProductOptions) && is_array($allProductOptions)) {
                                foreach ($allProductOptions as $apo) {
                                    $data['productOption'] = $apo;
                                    $this->PrintShopOption->setGroupID($apo['groupID']);
                                    $this->PrintShopOption->setTypeID($apo['typeID']);
                                    $deletedFotmats = $this->PrintShopOption->deleteFormats($apo['ID']);
                                    if ($deletedFotmats) {
                                        $data['infoPrdOptFormats'] = 'Remove formats for options in products.';
                                    }
                                    $iOpt += intval($this->PrintShopOption->delete($ID, $ao['ID']));
                                }
                            }

                            $oldRealizationTimes = $this->PrintShopConfigRealizationTime->customGetAll($ao['ID']);
                            foreach ($oldRealizationTimes as $or) {
                                $iRealizationTimes += intval($this->PrintShopConfigRealizationTime->delete('ID', $or['ID']));
                            }

                            $this->PrintShopConfigPrice->setAttrID($ao['attrID']);
                            $this->PrintShopConfigPrice->setOptID($ao['ID']);

                            $controllers = $this->PrintShopConfigPrice->countByController();
                            if (!empty($controllers)) {
                                foreach ($controllers as $co) {
                                    $this->PrintShopConfigPrice->setControllerID($co['controllerID']);

                                    $prices = $this->PrintShopConfigPrice->getAll();
                                    foreach ($prices as $op) {
                                        $iPrices += intval($this->PrintShopConfigPrice->delete('ID', $op['ID']));
                                    }
                                }
                            }

                            $this->PrintShopConfigDetailPrice->setAttrID($ao['attrID']);
                            $this->PrintShopConfigDetailPrice->setOptID($ao['ID']);
                            $details = $this->PrintShopConfigDetailPrice->getAll();
                            if (!empty($details)) {
                                foreach ($details as $d) {
                                    $iDetailPrices += intval($this->PrintShopConfigDetailPrice->delete('ID', $d['ID']));
                                }
                            }

                            $this->PrintShopConfigExclusion->setAttrID($ao['attrID']);
                            $this->PrintShopConfigExclusion->setOptID($ao['ID']);
                            $iExclusions += intval($this->PrintShopConfigExclusion->customDelete());

                            $iOperations += intval($this->OperationOption->delete('optionID', $ao['ID']));

                            $this->PrintShopConfigIncrease->setAttrID($ao['attrID']);
                            $this->PrintShopConfigIncrease->setOptID($ao['ID']);
                            $iIncreases += intval($this->PrintShopConfigIncrease->deleteBy());

                            if (!$this->PrintShopConfigOptionLang->delete('optionID', $ao['ID'])) {
                                $data = $this->sendFailResponse('09');
                                return $data;
                            }

                            $this->PrintShopAttributeName->delete('attrID', $ID);
                        }
                    }
                    $data['infoOpt'] .= ' Remove: ' . $i;
                    $data['infoPrdOpt'] = 'Remove: ' . $iOpt . ' options for products.';
                    $data['inforealizationTimes'] = 'Remove: ' . $iRealizationTimes . ' realizationTimes for options.';
                    $data['infoPrices'] = 'Remove: ' . $iPrices . ' prices for options.';
                    $data['infoDetailPrices'] = 'Remove: ' . $iDetailPrices . ' detail prices for options.';
                    $data['infoExclusions'] = 'Remove: ' . $iExclusions . ' exclusions.';
                    $data['infoOperations'] = 'Remove: ' . $iOperations . ' operations.';
                    $data['infoIncreases'] = 'Remove: ' . $iIncreases . ' increases.';
                }

                if (!$this->PrintShopConfigAttributeLang->delete('attributeID', $ID)) {
                    $data = $this->sendFailResponse('09');
                    return $data;
                }
            }
            $data['response'] = true;
            return $data;
        } else {
            header("HTTP/1.0 403 Forbidden");
            $data['response'] = false;
            return $data;
        }
    }

    /**
     * @return mixed
     */
    public function patch_sortAttr()
    {
        $post = $this->Data->getAllPost();
        $response = $this->PrintShopConfigAttribute->sort($post);
        $return['response'] = $response;
        return $return;
    }

    /**
     * @param null $ID
     * @return array|bool|mixed
     */
    public function attributeType($ID = NULL)
    {
        if (intval($ID) > 0) {
            $data = $this->PrintShopConfigAttributeType->get('ID', $ID);
        } else {
            $data = $this->PrintShopConfigAttributeType->getAll();
        }
        if (empty($data)) {
            $data = array();
        }
        return $data;
    }

    public function attributeNature()
    {
        return $this->PrintShopConfigAttributeNature->getAll();
    }

    /**
     * Copy attribute
     *
     * @param int
     * @return array
     */
    public function copy($attrID)
    {
        if (intval($attrID) < 1) {
            return $this->sendFailResponse('06');
        }

        $attr = $this->PrintShopConfigAttribute->customGet($attrID);

        $attr['name'] = $attr['name'] . ' - ' . 'KOPIA';
        unset($attr['ID']);
        $newAttrID = $this->PrintShopConfigAttribute->customCreate($attr['name'], $attr['type'], $attr['natureID'], $attr['rangeID'], $attr['adminName'], $attr['multipleOptionsMax'], $attr['displayImageOnMiniature'], $attr['specialFunction']);

        $attrsList = $this->PrintShopConfigAttribute->getAll();
        $sortArr = array();
        $i = 0;
        $gapIndex = null;
        foreach ($attrsList as $al) {
            if ($al['ID'] == $attrID) {
                $i++;
                $gapIndex = $i;
            }
            if ($al['ID'] == $newAttrID) {
                $i = $gapIndex;
            }
            $sortArr[$i] = $al['ID'];
            $i++;
        }
        $this->PrintShopConfigAttribute->sort($sortArr);

        $this->PrintShopConfigOption->setAttrID($attrID);
        $allOptions = $this->PrintShopConfigOption->getAll();

        $newOptionIDs = array();
        $oldRealizationTimes = array();
        foreach ($allOptions as $o) {
            $oldOptionID = $o['ID'];
            unset($o['ID']);
            $o['attrID'] = $newAttrID;
            $this->PrintShopConfigOption->setAttrID($newAttrID);
            $newOptionIDs[$oldOptionID] = $this->PrintShopConfigOption->customCreate($o['name'], $o['adminName'], $o['oneSide']);

            $fields = array('adminName', 'minPages', 'maxPages', 'weight', 'sizePage', 'active',
                'sort', 'oneSide', 'special', 'minVolume', 'rollLength', 'printRotated',
                'itemWeight', 'maxFolds', 'minThickness', 'maxThickness');
            foreach ($fields as $f) {
                $this->PrintShopConfigOption->update($newOptionIDs[$oldOptionID], $f, $o[$f]);
            }

            $oldRealizationTimes[$oldOptionID] = $this->PrintShopConfigRealizationTime->customGetAll($oldOptionID);
        }

        $setRealizations = array();
        foreach ($allOptions as $o) {
            foreach ($oldRealizationTimes[$o['ID']] as $or) {
                $optionID = $newOptionIDs[$o['ID']];
                $volume = $or['volume'];
                $days = $or['days'];
                $setRealizations[] = $this->PrintShopConfigRealizationTime->set($optionID, $volume, $days);
            }
        }

        $newPrices = array();
        foreach ($allOptions as $o) {
            $oldOptionID = $o['ID'];
            $this->PrintShopConfigPrice->setAttrID($attrID);
            $this->PrintShopConfigPrice->setOptID($o['ID']);

            $controllers = $this->PrintShopConfigPrice->countByController();
            if (empty($controllers)) {
                continue;
            }
            foreach ($controllers as $co) {
                $this->PrintShopConfigPrice->setControllerID($co['controllerID']);

                $this->PrintShopConfigPrice->setAttrID($attrID);
                $this->PrintShopConfigPrice->setOptID($o['ID']);
                $oldPrices = $this->PrintShopConfigPrice->getAll();

                $this->PrintShopConfigPrice->setAttrID($newAttrID);
                $this->PrintShopConfigPrice->setOptID($newOptionIDs[$o['ID']]);
                foreach ($oldPrices as $op) {
                    $newPrices[$oldOptionID] = $this->PrintShopConfigPrice->customCreate(
                        $op['amount'],
                        $op['value'],
                        $op['priceType'],
                        $op['expense']
                    );
                }
            }
        }

        $newDetailPrices = array();
        foreach ($allOptions as $o) {
            $this->PrintShopConfigDetailPrice->setAttrID($attrID);
            $this->PrintShopConfigDetailPrice->setOptID($o['ID']);
            $details = $this->PrintShopConfigDetailPrice->getAll();
            if (empty($details)) {
                continue;
            }
            foreach ($details as $d) {
                $this->PrintShopConfigDetailPrice->setAttrID($newAttrID);
                $this->PrintShopConfigDetailPrice->setOptID($newOptionIDs[$o['ID']]);
                $this->PrintShopConfigDetailPrice->setControllerID($d['controllerID']);
                $newDetailPrices[$d['ID']] = $this->PrintShopConfigDetailPrice->createAll($d['minPrice'], $d['basePrice'], $d['startUp']);
            }
        }

        $newExclusions = array();

        foreach ($allOptions as $o) {
            $this->PrintShopConfigExclusion->setAttrID($attrID);
            $this->PrintShopConfigExclusion->setOptID($o['ID']);
            $exclusions = $this->PrintShopConfigExclusion->getAll();
            foreach ($exclusions as $ex) {
                $this->PrintShopConfigExclusion->setAttrID($newAttrID);
                $this->PrintShopConfigExclusion->setOptID($newOptionIDs[$o['ID']]);
                $newExclusions[] = $this->PrintShopConfigExclusion->customCreate($ex['excAttrID'], $ex['excOptID']);
            }
        }

        $newIncreases = array();
        foreach ($allOptions as $o) {
            $this->PrintShopConfigIncrease->setAttrID($attrID);
            $this->PrintShopConfigIncrease->setOptID($o['ID']);

            $increaseControllers = $this->PrintShopConfigIncrease->countByController();

            if (!empty($increaseControllers)) {
                foreach ($increaseControllers as $co) {

                    $this->PrintShopConfigIncrease->setControllerID($co['controllerID']);
                    $this->PrintShopConfigIncrease->setAttrID($attrID);
                    $this->PrintShopConfigIncrease->setOptID($o['ID']);
                    $oldIncreases = $this->PrintShopConfigIncrease->getAll();

                    $this->PrintShopConfigIncrease->setAttrID($newAttrID);
                    $this->PrintShopConfigIncrease->setOptID($newOptionIDs[$o['ID']]);
                    foreach ($oldIncreases as $oi) {
                        $newIncreases[] = $this->PrintShopConfigIncrease->customCreate(
                            $oi['amount'],
                            $oi['value'],
                            $oi['increaseType']
                        );
                    }
                }
            }
        }

        /**
         * @TODO this should be in loop - to fix
         */
        $this->PrintShopConfigPaperPrice->setOptID($o['ID']);

        $paperPrices = $this->PrintShopConfigPaperPrice->getAll();
        $this->PrintShopConfigPaperPrice->setOptID($newOptionIDs[$o['ID']]);
        $newPaperPrices = array();

        if (!empty($paperPrices)) {
            foreach ($paperPrices as $pp) {
                $newPaperPrices[] = $this->PrintShopConfigPaperPrice->customCreate($pp['price'], $pp['expense'], $pp['amount']);
            }
        }

        $newOperations = array();
        foreach ($allOptions as $o) {
            $operations = $this->OperationOption->getSelectedOperations($o['ID']);
            foreach ($operations as $op) {
                $params['optionID'] = $newOptionIDs[$o['ID']];
                $params['operationID'] = $op['operationID'];
                $newOperations[] = $this->OperationOption->create($params);
            }
        }

        $names = $this->PrintShopConfigAttributeLang->get('attributeID', $attrID);
        foreach ($names as $name) {
            $this->PrintShopConfigAttributeLang->set($name['lang'], $name['name'], $newAttrID);
        }

        foreach ($allOptions as $o) {
            $names = $this->PrintShopConfigOptionLang->get('optionID', $o['ID']);
            foreach ($names as $name) {
                $this->PrintShopConfigOptionLang->set($name['lang'], $name['name'], $newOptionIDs[$o['ID']]);
            }
        }

        $data['info'] = 'End copy!';
        $data['response'] = true;
        return $data;
    }

    /**
     * @param $typeID
     * @return array|bool
     */
    public function checkCustomNames($typeID)
    {
        $count = $this->PrintShopAttributeName->countByType($typeID);
        if (!$count) {
            $count = array();
        }
        return $count;
    }

    /**
     * @param $typeID
     * @return array
     */
    public function getAttributeSettings($typeID)
    {
        $list = $this->PrintShopProductAttributeSetting->get('typeID', $typeID, true);

        if (!$list) {
            return array();
        }

        $result = array();
        foreach ($list as $row) {
            $result[$row['attrID']] = $row;
        }

        return $result;
    }

    public function attributeFilters($attrID)
    {
        $this->PrintShopConfigOption->setAttrID($attrID);
        $filterConfig = [];
        $filterConfig['categoriesTree'] = [];
        $this->PrintShopConfigOptionDescription->setDomainID($this->domainID);
        $this->PrintShopConfigOptionDescription->setAttrID($attrID);

        function minMax($baseName, &$filterConfig, $value)
        {
            if (!isset($filterConfig[$baseName])) {
                $filterConfig[$baseName] = [];
            }
            if (!isset($filterConfig[$baseName]['minValue'])) {
                $filterConfig[$baseName]['minValue'] = PHP_FLOAT_MAX;
            }
            if (!isset($filterConfig[$baseName]['maxValue'])) {
                $filterConfig[$baseName]['maxValue'] = 0;
            }
            if ($value == null) {
                return;
            }
            $value = floatval($value);
            if ($value < $filterConfig[$baseName]['minValue']) {
                $filterConfig[$baseName]['minValue'] = $value;
            }
            if ($value > $filterConfig[$baseName]['maxValue']) {
                $filterConfig[$baseName]['maxValue'] = $value;
            }
        }

        foreach ($this->PrintShopConfigOption->getAll() as $option) {
            $this->PrintShopConfigOptionDescription->setOptID($option['ID']);
            $descriptionsRaw = $this->PrintShopConfigOptionDescription->getForOption();
            $descriptions = [];
            foreach ($descriptionsRaw as $description) {
                $descriptions[$description['name']] = trim($description['value']);
            }
            $category = $descriptions['category'];
            $group = $descriptions['group'];
            $type = $descriptions['paper_type'];
            if (empty($category) || empty($group) || empty($type)) {
                continue;
            }
            minMax('weight', $filterConfig, $option['weight']);
            minMax('whiteness', $filterConfig, $descriptions['whiteness']);
            minMax('thickness', $filterConfig, $option['sizePage']);
            minMax('opacity', $filterConfig, $descriptions['opacity']);
            minMax('roughness', $filterConfig, $descriptions['roughness']);


            if (empty($filterConfig['categoriesTree'][$category])) {
                $filterConfig['categoriesTree'][$category] = [];
            }
            if (empty($filterConfig['categoriesTree'][$category][$group])) {
                $filterConfig['categoriesTree'][$category][$group] = [];
            }
            if (empty($filterConfig['categoriesTree'][$category][$group][$type])) {
                $filterConfig['categoriesTree'][$category][$group][$type] = [
                    'description' => $descriptions['paper_type_description'],
                    'image' => $descriptions['paper_type_image']
                ];
            }
            $filterConfig['categoriesTree'][$category][$group][$type]['IDS'][] = $option['ID'];
        }

        foreach (['certificates', 'printingTechniques', 'application', 'color_hex', 'category', 'group', 'paper_type'] as $listName) {
            $filterConfig[$listName] = [];
            $filterConfig[$listName]['values'] = array_filter($this->PrintShopConfigOptionDescription->getValuesByTypeName($listName), function ($item) {
                return !empty($item);
            });
            $tmp = [];
            foreach ($filterConfig[$listName]['values'] as $values) {
                $tmp = array_merge($tmp, array_map(function ($item) {
                    return trim($item);
                }, preg_split('/,/', $values)));
            }
            $tmp = array_values(array_unique($tmp));
            $filterConfig[$listName]['values'] = $tmp;
        }


        $return['filterConfig'] = $filterConfig;
        $return['descriptionsMap'] = $this->PrintShopConfigOptionDescription->getTypesData([
            'category', 'group', 'paper_type', 'weight', 'whiteness', 'thickness', 'opacity', 'roughness', 'certificates', 'printingTechniques', 'application', 'color_hex'
        ]);
        return $return;

    }

    public function post_attributeFilters($attrID){
        $this->PrintShopConfigOption->setAttrID($attrID);
        $this->PrintShopConfigOption->setDomainID($this->getDomainID());
        $allOptions = $this->PrintShopConfigOption->getAllActiveWithDescriptions();
        $filter = $this->Data->getAllPost();
        foreach ($filter as $part) {
            $filter[$part['name']] = $part;
        }
        $altOptionsIds = $this->OptionsFilter->matchOptions($allOptions, $filter, lang);
        return array_values($altOptionsIds);
    }

    public function post_getRelativePapers(){
        $post = $this->Data->getAllPost();
        return $this->PrintShopRelativeOptionsFilter->getOptionFilter($post['attrID'], $post['optID']);
    }

    public function attributeOptions($attrID)
    {
        $this->PrintShopConfigOption->setAttrID($attrID);
        $this->PrintShopConfigOption->setDomainID($this->getDomainID());
        $options = $this->PrintShopConfigOption->getAllActiveWithDescriptions();
        return $options;
    }

    public function post_attributeOption()
    {
        $post = $this->Data->getAllPost();
        $this->PrintShopConfigOption->setAttrID($post['attrID']);
        $this->PrintShopConfigOption->setDomainID($this->getDomainID());
        $option = $this->PrintShopConfigOption->getOption($post['optID']);
        return $option;
    }

    public function productsUsingOptions($attrID)
    {
        $this->PrintShopConfigOption->setAttrID($attrID);
        $this->PrintShopConfigOption->setDomainID($this->getDomainID());
        $options = $this->PrintShopConfigOption->getProductsUsingOptions();
        $complexProducts = $this->PrintShopType->get('complex', 1, true);
        foreach($complexProducts as &$singleComplexProduct){
            $this->PrintShopComplex->setTypeID($singleComplexProduct['ID']);
            $complexGroups = $this->PrintShopComplex->getAll();
            $singleComplexProduct['complexProducts'] = [];
            foreach($complexGroups as $singleComplexGroup){
                $singleComplexProduct['complexProducts'] = array_merge($singleComplexProduct['complexProducts'], $singleComplexGroup['products']);
            }
            $addProduct = $this->PrintShopConfigOption->getComplexProductForDisplay($singleComplexProduct['ID'])[0];
            $addProduct['options'] = [];
            foreach($singleComplexProduct['complexProducts'] as $singleType){
                $usingOptions = $this->PrintShopConfigOption->getTypeWithUsingOptions($singleType['typeID']);
                foreach($usingOptions as $singleUsingOption){
                    $addProduct['options'] = array_merge($addProduct['options'], $singleUsingOption['options']);
                }
            }    

            if($addProduct['typeID']){
                $options[] = $addProduct;   
            }
        }

        return $options;
    }

    public function post_attributeOptionPDF($optionID)
    {
        $post = $this->Data->getAllPost();
        $domainID = $this->getDomainID();
        
        $this->PrintShopConfigOption->setAttrID(2);
        $this->PrintShopConfigOption->setDomainID($domainID);
        $printData = $this->PrintShopConfigOption->getOption($optionID);

        $dateCurr = time();

        $options = $this->PrintShopConfigOption->getProductsUsingOptions();
        $products = [];
        foreach($options as $option){
            if(in_array($optionID, $option['options'])){
                $products[] = $option['names'];
            }
        }
        $printData[0]['products'] = $products;
        $printData[0]['altPapers'] = $post['altPapers'];

        try {

            $html2pdf = new Html2Pdf('P', 'A4', 'pl', true, 'UTF-8');
            $html2pdf->setTestTdInOnePage(false);
            $html2pdf->addFont('freesans', 'regular', BASE_DIR.'libs/tcpdf/fonts/freesans.php');
            $html2pdf->setDefaultFont('freesans');

            $content = '';

            $htmlRender = $this->printAttributesHTML($printData[0]);

            $content .= $htmlRender['content'];

            $html2pdf->writeHTML($content);

            $outputFolder = date('Y-m-d');

            if (!is_dir(MAIN_UPLOAD . companyID . '/' . 'productCards/attr_pdf_' . $optionID)) {
                mkdir(MAIN_UPLOAD . companyID . '/' . 'productCards/attr_pdf_' . $optionID, 0777);
            }
            $path = MAIN_UPLOAD . companyID . '/' . 'productCards/attr_pdf_' . $optionID . '/attr_desc_' . $optionID . '-'.$dateCurr.'.pdf';

            $html2pdf->Output($path, 'F');
            $link = STATIC_URL . companyID . '/productCards/attr_pdf_' . $optionID . '/attr_desc_' . $optionID . '-'.$dateCurr.'.pdf';
            $res = array();
            $res['path'] = $path;
            // $res['content'] = $content;
            $res['link'] = $link;
            $res['success'] = true;
            $res['centent'] = $htmlRender;
        } catch (Html2PdfException $e) {
            return array(
                'info' => $e->getMessage(),
                'error' => true,
                'response' => false
            );
        }
        return $res;
    }

    private function printAttributesHTML($data)
    {
        $loader = new FilesystemLoader(STATIC_PATH . 'templates');

        $twig = new Twig_Environment($loader, array(
            'auto_reload' => true
        ));
        $twig->addExtension(new TranslateExtension());

        // $templateID = 131;
        $templateName = 'print-attribute-details';

        $domainID = $this->getDomainID();
        $this->TemplateSetting->setDomainID($domainID);

        $templateSetting = $this->TemplateSetting->getOne(131, 1);

        $templatePath = 'default/131/' . $templateName . '.html';

        if ($templateSetting && $templateSetting['source'] == 1) {
            $templatePath = companyID . '/131/' . $templateName . '.html';
        } elseif ($templateSetting && $templateSetting['source'] == 2) {
            $templatePath = companyID . '/131/' . $this->getDomainID() . '/' . $templateName . '.html';
        }

        $template = $twig->load($templatePath);

        // $logoFile = MAIN_UPLOAD . 'uploadedFiles' . '/' . companyID . '/' . 'logos' . '/' . $this->getDomainID() . '/logo';

        $ceretificatesArray = explode(', ', $data['descriptions']['certificates']);
        $certificates = null;
        if(sizeof($ceretificatesArray) > 0) $certificates = $ceretificatesArray;

        $printingTechniquesArray = explode(', ', $data['descriptions']['printingTechniques']);
        $printingTechniques = null;
        if(sizeof($printingTechniquesArray) > 0) $printingTechniques = $printingTechniquesArray;

        $finishingAndProcessingArray = explode(', ', $data['descriptions']['finishingAndProcessing']);
        $finishingAndProcessing = null;
        if(sizeof($finishingAndProcessingArray) > 0) $finishingAndProcessing = $finishingAndProcessingArray;

        $imageURL = '';
        if($data['descriptions']['paper_type_image'] && $data['descriptions']['paper_type_image'] !== ''){
            $imageURL = $data['descriptions']['paper_type_image'];
            if(strpos($imageURL, STATIC_URL) !== false){
                $imageURL = str_replace(STATIC_URL, MAIN_UPLOAD, $imageURL);
            } 
        }

        $content = $template->render(
            array(
                // 'logoPath' => $logoFile,
                'printDate' => date(DATE_FORMAT),
                'lang' => lang,
                'paper_type' => $data['name'],
                'paper_type_description' => $data['descriptions']['paper_type_description'],
                'category' => $data['descriptions']['category'],
                'group' => $data['descriptions']['group'],
                'supplier' => $data['descriptions']['supplier'],
                'whiteness' => $data['descriptions']['whiteness'],
                'sizePage' => $data['sizePage'],
                'opacity' => $data['descriptions']['opacity'],
                'colorOfThePaper' => $data['descriptions']['colorOfThePaper'],
                'smoothnessRoughness' => $data['descriptions']['smoothnessRoughness'],
                'certificates' => $certificates,
                'printingTechniques' => $printingTechniques,
                'finishingAndProcessing' => $finishingAndProcessing,
                'products' => $data['products'],
                'altPapers' => $data['altPapers'],
                'imageURL' => $imageURL
            )
        );

        return array('content' => $content, 'templatePath' => $templatePath, 'templateSetting' => $templateSetting, 'domainID' => $domainID);
    }

    /**
     * @return mixed
     */
    public function post_uploadIcon()
    {
        $response['response'] = false;
        $attributeID = $this->Data->getPost('typeID');

        $maxID = $this->UploadFile->getMaxID();
        $dirNumber = floor($maxID / 100);
        $filename = $_FILES['file']['name'];
        $destFolder = $this->iconFolder . '/' . $dirNumber . '/';

        $attribute = $this->PrintShopConfigAttribute->get('ID', $attributeID);

        $one = $this->UploadFile->get('ID', $attribute['iconID']);

        $this->Uploader->remove($this->iconFolder, $one['path']);

        $destIconPath = MAIN_UPLOAD . $destFolder;

        if (!is_dir($destIconPath)) {
            mkdir($destIconPath, 0755, true);
            chmod($destIconPath, 0755);
        }

        if (is_file($destIconPath . $filename)) {
            $nameParts = explode('.', $filename);
            for ($i = 1; ; $i++) {
                $newFileName = $nameParts[0] . '_' . $i . '.' . $nameParts[1];
                if (!is_file($destIconPath . $newFileName)) {
                    $filename = $newFileName;
                    break;
                }
            }
        }

        $res = $this->Uploader->upload($_FILES, 'file', $destFolder, $filename);

        if ($res) {
            $lastID = $this->UploadFile->setUpload($filename, 'attributeIcons', $dirNumber . '/' . $filename);

            $this->PrintShopConfigAttribute->update($attribute['ID'], 'iconID', $lastID);

            $icon = $this->UploadFile->get('ID', $lastID);

            if ($icon) {
                $icon['url'] = STATIC_URL . $this->iconFolder . $icon['path'];
                $response['icon'] = $icon;
                $response['item'] = $attribute;
                $response['response'] = true;
            }

        }
        return $response;
    }

    /**
     * @param $categoryID
     * @return mixed
     */
    public function delete_uploadIcon($categoryID)
    {
        $data['response'] = false;
        $category = $this->PrintShopConfigAttribute->get('ID', $categoryID);

        $one = $this->UploadFile->get('ID', $category['iconID']);

        if ($this->Uploader->remove($this->iconFolder, $one['path'])) {
            $data['response'] = $this->UploadFile->delete('ID', $one['ID']);
            $this->PrintShopConfigAttribute->update($category['ID'], 'iconID', NULL);
        }

        return $data;
    }
    public function fillImages(array $items, $findKey='iconID', $insertKey='iconUrl', $folder='icons'): array
    {
        $aggregateImages = array();
        foreach ($items as $key => $item) {
            if ($item[$findKey]) {
                $aggregateImages[] = $item[$findKey];
            }
        }

        $images = $this->UploadFile->getFileByList($aggregateImages);

        if ($images) {

            foreach ($items as $key => $item) {
                if (array_key_exists($item[$findKey], $images)) {
                    $items[$key][$insertKey] = STATIC_URL . $folder . $images[$item[$findKey]]['path'];
                }
            }
        };

        return $items;
    }
}

