<?php

/**
 * MainMetaTagsController.php
 *
 * Handles operations related to main meta tags, including CRUD operations
 * and image uploads for meta tags.
 *
 * @package DreamSoft\Controllers\MetaTags
 * @Author          Rafał Leśniak
 * @Date            17-01-2018
 * @editedBy        Krzysztof Bochenek
 * @editDate        25.10.2024
 */

namespace DreamSoft\Controllers\MetaTags;

use DreamSoft\Controllers\Components\Uploader;
use DreamSoft\Core\Controller;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeLanguage;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopProduct\PrintShopGroupLanguage;
use DreamSoft\Models\MainMetaTag\MainMetaTag;
use DreamSoft\Models\MainMetaTag\MainMetaTagLanguage;
use DreamSoft\Models\Route\Route;
use DreamSoft\Models\Seo\MetaTag;
use DreamSoft\Models\Product\CategoryLang;
use DreamSoft\Models\Upload\UploadFile;

class MetaTagsController extends Controller
{
    /**
     * @var MetaTag
     */
    private MetaTag $MetaTag;
    /**
     * @var CategoryLang
     */
    private CategoryLang $CategoryLang;
    /**
     * @var PrintShopTypeLanguage
     */
    protected PrintShopTypeLanguage $PrintShopTypeLanguage;
    /**
     * @var PrintShopGroupLanguage
     */
    protected PrintShopGroupLanguage $PrintShopGroupLanguage;
    /**
     * @var PrintShopType
     */
    private PrintShopType $PrintShopType;
    /**
     * @var Route
     */
    private Route $Route;
    /**
     * @var MainMetaTag
     */
    private MainMetaTag $MainMetaTag;
    /**
     * @var MainMetaTagLanguage
     */
    private MainMetaTagLanguage $MainMetaTagLanguage;

    /**
     * @var UploadFile
     */
    private UploadFile $UploadFile;
    /**
     * @var Uploader
     */
    private Uploader $Uploader;
    /**
     * @var string
     */

    protected string $metaImagesFolder;

    public $useModels = array();

    /**
     * MetaTagsController constructor.
     * @param array $parameters
     */
    public function __construct(array $parameters = array())
    {
        parent::__construct($parameters);
        $this->MetaTag = MetaTag::getInstance();
        $this->CategoryLang = CategoryLang::getInstance();
        $this->PrintShopGroupLanguage = PrintShopGroupLanguage::getInstance();
        $this->PrintShopTypeLanguage = PrintShopTypeLanguage::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->Route = Route::getInstance();
        $this->MainMetaTag = MainMetaTag::getInstance();
        $this->MainMetaTagLanguage = MainMetaTagLanguage::getInstance();
        $this->UploadFile = UploadFile::getInstance();
        $this->Uploader = Uploader::getInstance();

        $this->metaImagesFolder = 'uploadedFiles/' . companyID . '/metaImages/';
    }


    /**
     * @param $ID
     */
    public function setDomainID($ID): void
    {
        parent::setDomainID($ID);
        $this->Route->setDomainID($ID);
        $this->MainMetaTag->setDomainID($ID);
    }


    /**
     * @return string
     */
    public function getImageFolder(): string
    {
        return $this->metaImagesFolder;
    }


    /**
     * @param array $params
     * @return array
     */
    public function index(array $params = array()): array
    {
        $type = $params['type'];
        $itemUrl = $params['itemUrl'];
        $categoryUrl = NULL;
        if( array_key_exists('categoryUrl', $params) ) {
            $categoryUrl = $params['categoryUrl'];
        }
        $metaTags = array();
        switch ($type) {
            case 'group':
                $groupLangEntity = $this->PrintShopGroupLanguage->getByUrl($itemUrl);
                $allMetaTags = $this->MetaTag->getByGroup($groupLangEntity['groupID']);
                $groupLangEntities = $this->PrintShopGroupLanguage->get('groupID', $groupLangEntity['groupID'], true);
                $categoryID = $this->CategoryLang->getByUrl($categoryUrl, lang);
                $categoryLangEntities = $this->CategoryLang->get('categoryID', $categoryID, true);
                if( $categoryLangEntities ) {
                    foreach ($categoryLangEntities as $categoryLangEntity) {
                        $metaTags['urlParams']['category'][$categoryLangEntity['lang']] = $categoryLangEntity['slug'];
                    }
                }

                $metaTags['metaTags'] = array();
                foreach ($allMetaTags as $oneMetaTag) {
                    $metaTags['metaTags'][$oneMetaTag['lang']] = array(
                        'title'               => $oneMetaTag['title'],
                        'description'         => $oneMetaTag['description'],
                        'keywords'            => $oneMetaTag['keywords'],
                        'og_title'            => $oneMetaTag['og_title'],
                        'og_url'              => $oneMetaTag['og_url'],
                        'og_site_name'        => $oneMetaTag['og_site_name'],
                        'og_description'      => $oneMetaTag['og_description'],
                        'og_locale'           => $oneMetaTag['og_locale'],
                        'imageID'             => $oneMetaTag['imageID'],
                        'og_image_width'      => $oneMetaTag['og_image_width'] != Null ? $oneMetaTag['og_image_width'] : 1200,
                        'og_image_height'     => $oneMetaTag['og_image_height'] != Null ? $oneMetaTag['og_image_height'] : 600,                        'og_image_alt'        => $oneMetaTag['og_image_alt'],
                        'twitter_card'        => $oneMetaTag['twitter_card'],
                        'twitter_site'        => $oneMetaTag['twitter_site'],
                        'twitter_creator'     => $oneMetaTag['twitter_creator'],

                    );
                }

                if( empty($metaTags['metaTags']) ) {
                    $routeEntity = $this->Route->getByState($type, $this->getDomainID());
                    $mainMetaTagEntity = $this->MainMetaTag->getOne($routeEntity['ID'], $this->getDomainID());
                    $mainMetaLanguageEntity = $this->MainMetaTagLanguage->getOne($mainMetaTagEntity['ID'], lang);
                    $metaTags['metaTags'][lang] = array(
                        'title'               => $mainMetaLanguageEntity['title'],
                        'description'         => $mainMetaLanguageEntity['description'],
                        'keywords'            => $mainMetaLanguageEntity['keywords'],
                        'og_title'            => $mainMetaLanguageEntity['og_title'],
                        'og_url'              => $mainMetaLanguageEntity['og_url'],
                        'og_site_name'        => $mainMetaLanguageEntity['og_site_name'],
                        'og_description'      => $mainMetaLanguageEntity['og_description'],
                        'og_locale'           => $mainMetaLanguageEntity['og_locale'],
                        'imageID'             => $mainMetaLanguageEntity['imageID'],
                        'og_image_width'      => $mainMetaLanguageEntity['og_image_width'] != Null ? $mainMetaLanguageEntity['og_image_width'] : 1200,
                        'og_image_height'     => $mainMetaLanguageEntity['og_image_height'] != Null ? $mainMetaLanguageEntity['og_image_height'] : 600,                        'og_image_alt'        => $mainMetaLanguageEntity['og_image_alt'],
                        'twitter_card'        => $mainMetaLanguageEntity['twitter_card'],
                        'twitter_site'        => $mainMetaLanguageEntity['twitter_site'],
                        'twitter_creator'     => $mainMetaLanguageEntity['twitter_creator'],
                    );
                }

                if( $groupLangEntities ) {
                    foreach ($groupLangEntities as $groupLangEntity) {
                        $metaTags['urlParams']['group'][$groupLangEntity['lang']] = $groupLangEntity['slug'];
                    }
                }
                break;
            case 'type':
                $typeLangEntity = $this->PrintShopTypeLanguage->getByUrl($itemUrl);
                $typeEntity = $this->PrintShopType->get('ID', $typeLangEntity['typeID']);
                $groupLangEntities = $this->PrintShopGroupLanguage->get('groupID', $typeEntity['groupID'], true);
                $typeLangEntities = $this->PrintShopTypeLanguage->get('typeID', $typeLangEntity['typeID'], true);
                $allMetaTags = $this->MetaTag->getByType($typeLangEntity['typeID']);
                $categoryID = $this->CategoryLang->getByUrl($categoryUrl, lang);
                $categoryLangEntities = $this->CategoryLang->get('categoryID', $categoryID, true);

                $metaTags['metaTags'] = array();
                foreach ($allMetaTags as $oneMetaTag) {
                    $metaTags['metaTags'][$oneMetaTag['lang']] = array(
                        'title'               => $oneMetaTag['title'],
                        'description'         => $oneMetaTag['description'],
                        'keywords'            => $oneMetaTag['keywords'],
                        'og_title'            => $oneMetaTag['og_title'],
                        'og_url'              => $oneMetaTag['og_url'],
                        'og_site_name'        => $oneMetaTag['og_site_name'],
                        'og_description'      => $oneMetaTag['og_description'],
                        'og_locale'           => $oneMetaTag['og_locale'],
                        'imageID'             => $oneMetaTag['imageID'],
                        'og_image_width'      => $oneMetaTag['og_image_width'] != Null ? $oneMetaTag['og_image_width'] : 1200,
                        'og_image_height'     => $oneMetaTag['og_image_height'] != Null ? $oneMetaTag['og_image_height'] : 600,                        'og_image_alt'        => $oneMetaTag['og_image_alt'],
                        'twitter_card'        => $oneMetaTag['twitter_card'],
                        'twitter_site'        => $oneMetaTag['twitter_site'],
                        'twitter_creator'     => $oneMetaTag['twitter_creator'],
                    );
                }

                if( empty($metaTags['metaTags']) ) {
                    $routeEntity = $this->Route->getByState('calculate', $this->getDomainID());
                    $mainMetaTagEntity = $this->MainMetaTag->getOne($routeEntity['ID'], $this->getDomainID());
                    $mainMetaLanguageEntity = $this->MainMetaTagLanguage->getOne($mainMetaTagEntity['ID'], lang);
                    $metaTags['metaTags'][lang] = array(
                        'title'               => $mainMetaLanguageEntity['title'],
                        'description'         => $mainMetaLanguageEntity['description'],
                        'keywords'            => $mainMetaLanguageEntity['keywords'],
                        'og_title'            => $mainMetaLanguageEntity['og_title'],
                        'og_url'              => $mainMetaLanguageEntity['og_url'],
                        'og_site_name'        => $mainMetaLanguageEntity['og_site_name'],
                        'og_description'      => $mainMetaLanguageEntity['og_description'],
                        'og_locale'           => $mainMetaLanguageEntity['og_locale'],
                        'imageID'             => $mainMetaLanguageEntity['imageID'],
                        'og_image_width'      => $mainMetaLanguageEntity['og_image_width'] != Null ? $mainMetaLanguageEntity['og_image_width'] : 1200,
                        'og_image_height'     => $mainMetaLanguageEntity['og_image_height'] != Null ? $mainMetaLanguageEntity['og_image_height'] : 600,                        'og_image_alt'        => $mainMetaLanguageEntity['og_image_alt'],
                        'twitter_card'        => $mainMetaLanguageEntity['twitter_card'],
                        'twitter_site'        => $mainMetaLanguageEntity['twitter_site'],
                        'twitter_creator'     => $mainMetaLanguageEntity['twitter_creator'],
                    );
                }

                if( $groupLangEntities ) {
                    foreach ($groupLangEntities as $groupLangEntity) {
                        $metaTags['urlParams']['group'][$groupLangEntity['lang']] = $groupLangEntity['slug'];
                    }
                }
                if( $typeLangEntities ) {
                    foreach ($typeLangEntities as $typeLangEntity) {
                        $metaTags['urlParams']['type'][$typeLangEntity['lang']] = $typeLangEntity['slug'];
                    }
                }
                if( $categoryLangEntities ) {
                    foreach ($categoryLangEntities as $categoryLangEntity) {
                        $metaTags['urlParams']['category'][$categoryLangEntity['lang']] = $categoryLangEntity['slug'];
                    }
                }

                break;
            case 'category':
                $categoryID = $this->CategoryLang->getByUrl($itemUrl, lang);
                $allMetaTags = $this->MetaTag->getByCategory($categoryID);
                $categoryLangEntities = $this->CategoryLang->get('categoryID', $categoryID, true);
                $metaTags['metaTags'] = array();
                foreach ($allMetaTags as $oneMetaTag) {
                    $metaTags['metaTags'][$oneMetaTag['lang']] = array(
                        'title'               => $oneMetaTag['title'],
                        'description'         => $oneMetaTag['description'],
                        'keywords'            => $oneMetaTag['keywords'],
                        'og_title'            => $oneMetaTag['og_title'],
                        'og_url'              => $oneMetaTag['og_url'],
                        'og_site_name'        => $oneMetaTag['og_site_name'],
                        'og_description'      => $oneMetaTag['og_description'],
                        'og_locale'           => $oneMetaTag['og_locale'],
                        'imageID'             => $oneMetaTag['imageID'],
                        'og_image_width'      => $oneMetaTag['og_image_width'] != Null ? $oneMetaTag['og_image_width'] : 1200,
                        'og_image_height'     => $oneMetaTag['og_image_height'] != Null ? $oneMetaTag['og_image_height'] : 600,                        'og_image_alt'        => $oneMetaTag['og_image_alt'],
                        'twitter_card'        => $oneMetaTag['twitter_card'],
                        'twitter_site'        => $oneMetaTag['twitter_site'],
                        'twitter_creator'     => $oneMetaTag['twitter_creator'],
                    );
                }

                if( empty($metaTags['metaTags']) ) {
                    $routeEntity = $this->Route->getByState('category', $this->getDomainID());
                    $mainMetaTagEntity = $this->MainMetaTag->getOne($routeEntity['ID'], $this->getDomainID());
                    $mainMetaLanguageEntity = $this->MainMetaTagLanguage->getOne($mainMetaTagEntity['ID'], lang);
                    $metaTags['metaTags'][lang] = array(
                        'title'               => $mainMetaLanguageEntity['title'],
                        'description'         => $mainMetaLanguageEntity['description'],
                        'keywords'            => $mainMetaLanguageEntity['keywords'],
                        'og_title'            => $mainMetaLanguageEntity['og_title'],
                        'og_url'              => $mainMetaLanguageEntity['og_url'],
                        'og_site_name'        => $mainMetaLanguageEntity['og_site_name'],
                        'og_description'      => $mainMetaLanguageEntity['og_description'],
                        'og_locale'           => $mainMetaLanguageEntity['og_locale'],
                        'imageID'             => $mainMetaLanguageEntity['imageID'],
                        'og_image_width'      => $mainMetaLanguageEntity['og_image_width'] != Null ? $mainMetaLanguageEntity['og_image_width'] : 1200,
                        'og_image_height'     => $mainMetaLanguageEntity['og_image_height'] != Null ? $mainMetaLanguageEntity['og_image_height'] : 600,
                        'og_image_alt'        => $mainMetaLanguageEntity['og_image_alt'],
                        'twitter_card'        => $mainMetaLanguageEntity['twitter_card'],
                        'twitter_site'        => $mainMetaLanguageEntity['twitter_site'],
                        'twitter_creator'     => $mainMetaLanguageEntity['twitter_creator'],
                    );
                }

                if( $categoryLangEntities ) {
                    foreach ($categoryLangEntities as $categoryLangEntity) {
                        $metaTags['urlParams']['category'][$categoryLangEntity['lang']] = $categoryLangEntity['slug'];
                    }
                }
                break;
            default:
                break;
        }

        if( !empty($metaTags) ) {
            $metaTags['response'] = true;
        } else {
            $metaTags['response'] = false;
            $metaTags['metaTags'] = NULL;
        }

        return $metaTags;
    }
    /**
     * @return mixed
     */

    /**
     * Handles POST requests to upload an image for a meta tag.
     *
     * @return array{
     *     response: bool,
     *     image?: array{
     *         ID: int,
     *         name: string,
     *         path: string,
     *         created: string,
     *         destination: string,
     *         url: string
     *     },
     *     item?: array,
     *     lang?: string
     * }
     */
    public function post_uploadImage()
    {
        $response['response'] = false;

        $metatagID = $this->Data->getPost('metatagID');
        $lang = $this->Data->getPost('language');
        $response['lang'] = $lang   ;

        $maxID = $this->UploadFile->getMaxID();


        $dirNumber = floor($maxID / 100);
        $filename = $_FILES['file']['name'];

        $destinationFolder = $this->metaImagesFolder . '/' . $dirNumber . '/';
        $destinationImagePath = MAIN_UPLOAD . $destinationFolder;


        $metatag = $this->MetaTag->get('ID', $metatagID);


        if (!is_dir($destinationImagePath)) {
            mkdir($destinationImagePath, 0755, true);
            chmod($destinationImagePath, 0755);
        }


        if (is_file($destinationImagePath . $filename)) {
            $nameParts = explode('.', $filename);
            for ($i = 1; ; $i++) {
                $newFileName = $nameParts[0] . '_' . $i . '.' . $nameParts[1];

                if (!is_file($destinationImagePath . $newFileName)) {
                    $filename = $newFileName;
                    break;
                }
            }
        }


        ## remove existing image

        if($metatagID && $metatag && $metatag['itemID'] != NULL){
            $this->delete_uploadImage($lang,$metatagID);
        }



        #upload image
        $res = $this->Uploader->upload($_FILES, 'file', $destinationFolder, $filename);

        if ($res) {
            $lastID = $this->UploadFile->setUpload($filename, 'MetaImages', $dirNumber . '/' . $filename);


            $image = $this->UploadFile->get('ID', $lastID);

            if ($image) {
                $image['url'] = STATIC_URL . $this->metaImagesFolder . $image['path'];
                $response['image'] = $image;
                $response['item'] = $metatag;
                $response['response'] = true;
            }

            # upload metetag if exist

            if ($metatagID){
                $this->MainMetaTagLanguage->update($metatagID,'imageID',$image['ID']);
            }

        }
        return $response;
    }

    /**
     * Handles DELETE requests to remove an uploaded image.
     *
     * @param int $MetaTagID
     * @return array{
     *     response: bool,
     *     update: bool
     * }
     */
    public function delete_uploadImage(string $lang, int $imageID): array
    {
        $data['response'] = false;
        $data['lang'] = $lang;



        $one = $this->UploadFile->get('ID', $imageID);

        if ($this->Uploader->remove($this->metaImagesFolder, $one['path'])) {

            $this->UploadFile->delete('ID', $one['ID']);

            $data['response'] = $this->UploadFile->delete('ID', $one['ID']);
            $data['update'] = $this->MetaTag->update($imageID, 'imageID', NULL);
        }

        return $data;
    }

    /**
     * @param array $metatags
     * @return mixed
     */
    public function getImages(array $metatags): array
    {
        $aggregateImages = array();
        foreach ($metatags as $key => $metatag) {
            if ($metatag['imageID']) {
                $aggregateImages[] = $metatag['imageID'];
            }
        }

        $images = $this->UploadFile->getFileByList($aggregateImages);

        if ($images) {
            foreach ($images as $key => $image) {
                $images[$key]['url'] = STATIC_URL . $this->getImageFolder() . $image['path'];
            }
        }

        foreach ($metatags as $key => $metatag) {
            if ($metatag['imageID']) {
                $metatags[$key]['icon'] = $images[$metatag['imageID']];
            }
        }

        return $metatags;
    }


}