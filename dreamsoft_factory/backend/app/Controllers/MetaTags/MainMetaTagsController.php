<?php

/**
 * MainMetaTagsController.php
 *
 * Handles operations related to main meta tags, including CRUD operations
 * and image uploads for meta tags.
 *
 * @package DreamSoft\Controllers\MetaTags
  * @Author          Rafał Leśniak
  * @Date            15.01.2018
  * @editedBy        Krzysztof Bochenek
  * @editDate        25.10.2024
 */

namespace DreamSoft\Controllers\MetaTags;

use DreamSoft\Controllers\Components\Uploader;
use DreamSoft\Core\Controller;
use DreamSoft\Models\MainMetaTag\MainMetaTag;
use DreamSoft\Models\MainMetaTag\MainMetaTagLanguage;
use DreamSoft\Models\Upload\UploadFile;

/**
 * Class MainMetaTagsController
 *
 * Controller for managing main meta tags and their associated languages and images.
 *
 * @package DreamSoft\Controllers\MetaTags
 */
class MainMetaTagsController extends Controller
{
    /**
     * @var MainMetaTag
     */
    private MainMetaTag $MainMetaTag;
    /**
     * @var MainMetaTagLanguage
     */
    private MainMetaTagLanguage $MainMetaTagLanguage;

    /**
     * @param array $parameters
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

    /**
     * MainMetaTagsController constructor.
     *
     * Initializes models and uploader component, and sets the meta images folder path.
     *
     * @param array $parameters Optional.
     * @param string $destinationFolder Default: metaImages
     */
    public function __construct(array $parameters = array(), string $destinationFolder='metaImages')
    {
        parent::__construct($parameters);
        $this->MainMetaTag = MainMetaTag::getInstance();
        $this->MainMetaTagLanguage = MainMetaTagLanguage::getInstance();
        $this->UploadFile = UploadFile::getInstance();
        $this->Uploader = Uploader::getInstance();
        $this->metaImagesFolder = 'uploadedFiles/' . companyID . '/'.$destinationFolder.'/';

    }

    /**
     * @param $ID
     *
     */
    public function setDomainID($ID) : void
    {
        parent::setDomainID($ID);
        $this->MainMetaTag->setDomainID($ID);
    }
    /**
     * @return string
     *
     */
    private function getImageFolder(): string
    {

        return $this->metaImagesFolder;
    }
    /**
     * @param $routeID
     * @return array{
     *     ID: int,
     *     routeID: int,
     *     domainID: int,
     *     languages: array<string, array{
     *         title: string,
     *         description: string,
     *         keywords: string,
     *         og_title: string,
     *         og_url: string|null,
     *         og_site_name: string|null,
     *         og_description: string,
     *         og_locale: string|null,
     *         imageID: int,
     *         og_image_width: int,
     *         og_image_height: int,
     *         og_image_alt: string|null,
     *         twitter_card: string|null,
     *         twitter_site: string|null,
     *         twitter_creator: string|null
     *     }>,
     *     images: array<string, array{
     *         ID: int,
     *         name: string,
     *         path: string,
     *         created: string,
     *         destination: string,
     *         url: string
     *     }>,
     *     response: bool
     */
    public function index($routeID): array
    {
        $mainMetaTag = $this->MainMetaTag->get('routeID', $routeID);

        if( !$mainMetaTag ) {
            return array('response' => false);
        }

        $mainTagLanguages = $this->MainMetaTagLanguage->get('mainMetaTagID', $mainMetaTag['ID'], true);
        $images = array();

        if( $mainTagLanguages ) {

            foreach ($mainTagLanguages as $mainTagLanguage) {
                $mainMetaTag['languages'][$mainTagLanguage['lang']] = array(
                    'title'               => $mainTagLanguage['title'],
                    'description'         => $mainTagLanguage['description'],
                    'keywords'            => $mainTagLanguage['keywords'],
                    'og_title'            => $mainTagLanguage['og_title'],
                    'og_url'              => $mainTagLanguage['og_url'],
                    'og_site_name'        => $mainTagLanguage['og_site_name'],
                    'og_description'      => $mainTagLanguage['og_description'],
                    'og_locale'           => $mainTagLanguage['og_locale'],
                    'imageID'             => $mainTagLanguage['imageID'],
                    'og_image_width'      => $mainTagLanguage['og_image_width'] != Null ? $mainTagLanguage['og_image_width'] : 1200,
                    'og_image_height'     => $mainTagLanguage['og_image_height'] != Null ? $mainTagLanguage['og_image_height'] : 600,
                    'og_image_alt'        => $mainTagLanguage['og_image_alt'],
                    'twitter_card'        => $mainTagLanguage['twitter_card'],
                    'twitter_site'        => $mainTagLanguage['twitter_site'],
                    'twitter_creator'     => $mainTagLanguage['twitter_creator'],
                );
            }

        }
        $mainMetaTag['images'] = $this->fillImages($mainTagLanguages);
        $mainMetaTag['response'] = true;

        return $mainMetaTag;
    }

    /**
     * Handles POST requests to create a new main meta tag.
     *
     * @return array{
     *     response: bool,
     *     savedLanguages: int,
     *     item?: array
     * }
     */
    public function post_index(): array
    {
        $post = $this->Data->getAllPost();
        $languages = $post['languages'];

        $savedLanguages = 0;
        $lastID = false;

        if( intval($post['routeID']) > 0 ) {
            $params = array();
            $params['routeID'] = $post['routeID'];
            $params['domainID'] = $this->getDomainID();
            $lastID = $this->MainMetaTag->create($params);

            if( $lastID ) {

                if( $languages ) {
                    foreach ($languages as $lang => $metaTag) {
                        $params = array();
                        $params['mainMetaTagID']        = $lastID;
                        $params['lang']                 = $lang;
                        $params['title']                = $metaTag['title'];
                        $params['description']          = $metaTag['description'];
                        $params['keywords']             = $metaTag['keywords'];
                        $params['og_title']             = $metaTag['og_title'] || $metaTag['title'];
                        $params['og_url']               = $metaTag['og_url'];
                        $params['og_site_name']         = $metaTag['og_site_name'];
                        $params['og_description']       = $metaTag['og_description'] || $metaTag['description'];
                        $params['og_locale']            = $metaTag['og_locale'];
                        $params['imageID']              = $metaTag['imageID'];
                        $params['og_image_width']       = $metaTag['og_image_width'] != Null ? $metaTag['og_image_width'] : 1200;
                        $params['og_image_height']      = $metaTag['og_image_height'] != Null ? $metaTag['og_image_height'] : 600;
                        $params['og_image_alt']         = $metaTag['og_image_alt'];
                        $params['twitter_card']         = $metaTag['twitter_card'];
                        $params['twitter_site']         = $metaTag['twitter_site'];
                        $params['twitter_creator']      = $metaTag['twitter_creator'];
                        error_log(serialize($params));

                        $lastSavedLanguageID = $this->MainMetaTagLanguage->create($params);

                        if( $lastSavedLanguageID > 0 ) {
                            $savedLanguages++;
                        }
                    }
                }

            }
        }

        if( $lastID ) {
            return array(
                'response' => true,
                'savedLanguages' => $savedLanguages,
                'item' => $this->index($post['routeID'])
            );
        }

        return $this->sendFailResponse('03');
    }

    /**
     * Handles PUT requests to update an existing main meta tag.
     *
     * @param int|null $ID The ID of the meta tag to update.
     * @return array{
     *     response: bool,
     *     savedLanguages?: int,
     *     updatedLanguages?: int,
     *     item?: array
     * }
     */
    public function put_index($ID)
    {
        $post = $this->Data->getAllPost();
        $languages = $post['languages'];

        if (!$ID) {
            $ID = $this->Data->getPost('ID');
        }

        if (!$ID) {
            return $this->sendFailResponse('04');
        }

        $savedLanguages = 0;
        $updatedLanguages = 0;

        if($languages) {
            foreach ($languages as $lang => $metaTag) {
                $existID = $this->MainMetaTagLanguage->exist($ID, $lang);

                if( $existID ) {
                    $metaTags = [
                        'title'             =>       'title',
                        'description'       =>       'description',
                        'keywords'          =>       'keywords',
                        'og_title'          =>        $metaTag['og_title']       != NULL ? 'og_title' : 'title',
                        'og_url'            =>       'og_url',
                        'og_site_name'      =>       'og_site_name',
                        'og_description'    =>        $metaTag['og_description'] != NULL ? 'og_description' : 'description',
                        'og_locale'         =>       'og_locale',
                        'imageID'           =>       'imageID',
                        'og_image_width'    =>       'og_image_width',
                        'og_image_height'   =>       'og_image_height',
                        'og_image_alt'      =>       'og_image_alt',
                        'twitter_card'      =>       'twitter_card',
                        'twitter_site'      =>       'twitter_site',
                        'twitter_creator'   =>       'twitter_creator'
                    ];

                    $updatedLanguages = 0;

                    foreach ($metaTags as $key => $value) {
                        if (is_string($value)) {
                            $value = $metaTag[$value];
                        }

                        if (intval($this->MainMetaTagLanguage->update($existID, $key, $value)) > 0) {
                            $updatedLanguages++;
                        }
                    }
                } else {
                    $params = array();
                    $params['mainMetaTagID']        = $ID;
                    $params['lang']                 = $lang;
                    $params['title']                = $metaTag['title'];
                    $params['description']          = $metaTag['description'];
                    $params['keywords']             = $metaTag['keywords'];
                    $params['og_title']             = $metaTag['og_title'] || $metaTag['title'];
                    $params['og_url']               = $metaTag['og_url'];
                    $params['og_site_name']         = $metaTag['og_site_name'];
                    $params['og_description']       = $metaTag['og_description'] || $metaTag['description'];
                    $params['og_locale']            = $metaTag['og_locale'];
                    $params['imageID']              = $metaTag['imageID'];
                    $params['og_image_width']       = $metaTag['og_image_width'] != Null ? $metaTag['og_image_width'] : 1200;
                    $params['og_image_height']      = $metaTag['og_image_height'] != Null ? $metaTag['og_image_height'] : 600;
                    $params['og_image_alt']         = $metaTag['og_image_alt'];
                    $params['twitter_card']         = $metaTag['twitter_card'];
                    $params['twitter_site']         = $metaTag['twitter_site'];
                    $params['twitter_creator']      = $metaTag['twitter_creator'];
                    $lastSavedLanguageID = $this->MainMetaTagLanguage->create($params);

                    if( $lastSavedLanguageID > 0 ) {
                        $savedLanguages++;
                    }
                }
            }
        }

        if( $savedLanguages > 0 || $updatedLanguages > 0 ) {

            $mainTag = $this->MainMetaTag->get('ID', $ID);

            return array(
                'response' => true,
                'savedLanguages' => $savedLanguages,
                'updatedLanguages' => $updatedLanguages,
                'item' => $this->index($mainTag['routeID'])
            );
        }

        return $this->sendFailResponse('03');

    }

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
        $lang =  $this->Data->getPost('language');

        $maxID = $this->UploadFile->getMaxID();


        $dirNumber = floor($maxID / 100);
        $filename = $_FILES['file']['name'];

        $destinationFolder = $this->metaImagesFolder . '/' . $dirNumber . '/';
        $destinationImagePath = MAIN_UPLOAD . $destinationFolder;



        ## remove existing image
        $one = $this->MainMetaTagLanguage->getOne($metatagID,$lang);

        if($one && $one['imageID'] != NULL){
            $this->delete_uploadImage($lang,$metatagID);
        }


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


        $metatag = $this->MainMetaTag->get('ID', $metatagID);

       #upload image
        $res = $this->Uploader->upload($_FILES, 'file', $destinationFolder, $filename);

        if ($res) {
            $lastID = $this->UploadFile->setUpload($filename, 'mainMetaImages', $dirNumber . '/' . $filename);


            $image = $this->UploadFile->get('ID', $lastID);

            if ($image) {
                $image['url'] = STATIC_URL . $this->metaImagesFolder . $image['path'];
                $response['image'] = $image;
                $response['item'] = $metatag;
                $response['lang'] = $lang;
                $response['response'] = true;
            }

            # upload metetag if exist
            if ($one){
                $this->MainMetaTagLanguage->update($one['ID'],'imageID',$image['ID']);
            }
        }

        return $response;
    }

    /**
     * Handles DELETE requests to remove an uploaded image.
     *
     * @param int $imageID The ID of the image to delete.
     * @param string $lang lang name.
     * @return array{
     *     response: bool,
     *     get?: array,
     *     update?: bool
     * }
     */
    public function delete_uploadImage(string $lang, int $mainMetaTagID ): array
    {
        $data['response'] = false;
        $metatag = array();

        $langs = $this->MainMetaTagLanguage->get("mainMetaTagID", $mainMetaTagID,true);
        foreach ($langs as $mt) {
            if ($lang == $mt['lang']) {
                $metatag = $mt;
                break;
            }
        }

        $imageID = $metatag['imageID'];
        $one = $this->UploadFile->get('ID', $imageID);

        if ($this->Uploader->remove($this->metaImagesFolder, $one['path'])) {

            $data['response'] = $this->UploadFile->delete('ID', $one['ID']);

            $this->MainMetaTagLanguage->get("imageID", $imageID,true);
            $data['update'] = $this->MainMetaTagLanguage->update($metatag['ID'], 'imageID', NULL);
        }

        return $data;
    }


    /**
     * @param array $metatags
     * @return mixed
     */
    public function fillImages(array $metatags): array
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

            return $images;
        };

        return [];
    }

}