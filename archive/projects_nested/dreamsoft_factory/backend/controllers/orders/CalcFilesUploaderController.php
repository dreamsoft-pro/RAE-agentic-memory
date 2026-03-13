<?php

use DreamSoft\Controllers\Components\Acl;
use DreamSoft\Controllers\Components\Uploader;
use DreamSoft\Controllers\Orders\DpProductsController;
use DreamSoft\Core\Controller;
use DreamSoft\Libs\TwigExtensions\TranslateExtension;
use DreamSoft\Models\Order\DpCalcFile;
use DreamSoft\Models\Order\DpCalcFileSet;
use DreamSoft\Models\Order\DpOrder;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Models\Order\DpProductFile;
use DreamSoft\Models\Order\DpProductReportFile;
use DreamSoft\Models\Other\ModelIconExtension;
use DreamSoft\Models\Upload\UploadFile;
use Twig\Environment as Twig_Environment;
use Twig\Loader\FilesystemLoader;

class CalcFilesUploaderController extends Controller
{

    public $useModels = array();

    protected $DpCalcFile;
    protected $DpCalcFileSet;
    protected $DpProductFile;
    protected $DpProductReportFile;
    protected $DpProduct;
    protected $DpOrder;
    protected $Uploader;
    protected $ModelIconExtension;
    private $Acl;
    protected $folder;
    private $UploadFile;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->DpCalcFile = DpCalcFile::getInstance();
        $this->DpCalcFileSet = DpCalcFileSet::getInstance();
        $this->DpProductFile = DpProductFile::getInstance();
        $this->DpProductReportFile = DpProductReportFile::getInstance();
        $this->DpOrder = DpOrder::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->ModelIconExtension = ModelIconExtension::getInstance();
        $this->Acl = new Acl();

        $this->folder = 'calcFiles';
        $this->miniaturesFolder = 'miniatures';
        $this->orgFileFolder = 'orgFiles';
        $this->orgCroppedFileFolder = 'orgCroppedFiles';
        $this->miniatureWidth = 300;
        $this->Uploader = Uploader::getInstance();
        $this->UploadFile = UploadFile::getInstance();
    }

    public function post_files($typeID, $calcFilesSetID = null)
    {

        $user = $this->Auth->getLoggedUser();
        $userID = $user['ID'];

        $created = date('Y-m-d H:i:s');
        $calcID = 0;

        $orgFileName = strtolower($_FILES['file']['name']);
        $originalFileName = $orgFileName;
        $name = $this->cleanString(rand().'-'.$orgFileName);

        $explodeName = explode('.', $orgFileName);
        $ext = end($explodeName);
        $name .= '.'.$ext;

        if(!$this->ModelIconExtension->isAllowedFile($name)){
            return $this->sendFailResponse('11');
        }

        if(!$userID){
            if($calcFilesSetID){
                $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFilesSetID);
            }else{
                $userID = 0;
                $calcFileSetID = $this->DpCalcFileSet->create(compact('userID', 'calcID', 'typeID', 'created'));
                $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFileSetID);
            }
        }else{
            $calcFileSet = $this->DpCalcFileSet->getByParams($userID, $typeID, 0);
            
            if($calcFileSet == false){
                $this->debug('ADD NEW');
                $calcFileSetID = $this->DpCalcFileSet->create(compact('userID', 'calcID', 'typeID', 'created'));
                $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFileSetID);
            }
        }

        if(!$userID){
            $userID = 0;
        }       

        $date = date('Y-m-d', strtotime($created));

        $destinationFolder = '/' .$this->folder. '/' . $userID . '/' . $calcFileSet['ID'] . '/';

        $res = $this->Uploader->uploadToCompany($_FILES, 'file', $destinationFolder, $name);
        if($res){
            $destFilePath = MAIN_UPLOAD . companyID . '/' .$destinationFolder;
            $originalFile = $destFilePath . $name;
            $miniatureFile = $destFilePath . $this->miniaturesFolder . '/'. $name;

            $this->createFolderIfDoesNotExists($destFilePath . $this->miniaturesFolder);
            $imagick = new Imagick($originalFile);
            $geo = $imagick->getImageGeometry();
            $width = $geo['width'];
            $height = $geo['height'];
            $imagick->scaleImage($this->miniatureWidth, 0);
            $imagick->writeimage($miniatureFile);

            $calcFilesSetID = $calcFileSet['ID'];
            $calcFilesID = $this->DpCalcFile->create(compact('name', 'calcFilesSetID', 'created', 'originalFileName', 'width', 'height'));
            $lastFile = $this->DpCalcFile->get('ID', $calcFilesID);

            $lastFile = $this->injectFileUrls($lastFile, STATIC_URL . companyID.$destinationFolder, $name);

            $this->createFolderIfDoesNotExists($destFilePath.$this->orgFileFolder);
            $this->createFolderIfDoesNotExists($destFilePath.$this->orgCroppedFileFolder);
        }

        return array('response' => $res, 'file' => $lastFile);

    }

    private function parseAllowedExtensions( $extensionList )
    {
        if( !$extensionList ) {
            return explode(',', THUMB_IMAGE_ALLOWED_EXTENSION);
        }
        $extensions = array();
        foreach ($extensionList as $item) {
            $extensions[] = $item['extension'];
        }

        return $extensions;
    }

    public function filesSet($setID)
    {

        $calcFileSet = $this->DpCalcFileSet->get('ID', $setID);
        $list = array();

        if ($calcFileSet == false) {
            $list = array();
        } else {
            $calcFiles = $this->DpCalcFile->get('calcFilesSetID', $calcFileSet['ID'], true);
            foreach ($calcFiles as $calcFile) {
                if($calcFile['copyOf'] == 0){
                    $copies = $this->getCopies($calcFile);
                    $calcFile['copies'] = sizeof($copies);

                    $calcFile = $this->injectFileUrls($calcFile, STATIC_URL . companyID . '/'.$this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/', $calcFile['name']);

                    $calcFile['isFirstInGroup'] = true;
                    $calcFile['isLastInGroup'] = false;
                    $list[] = $calcFile;
                    foreach($copies as $copy){
                        $copy['isFirstInGroup'] = false;
                        $copy['isLastInGroup'] = false;
                        if($copy['ID'] == $copies[sizeof($copies)-1]['ID']){
                            $copy['isLastInGroup'] = true;
                        }
                        $list[] = $copy;
                    }
                }
            }
        }

        return $list;
    }


    public function files($typeID)
    {

        $user = $this->Auth->getLoggedUser();
        $userID = $user['ID'];

        $calcFileSet = $this->DpCalcFileSet->getByParams($userID, $typeID, 0);
        $list = array();

        if ($calcFileSet == false) {
            $list = array();
        } else {

            $allowedThumbExtension = explode(',', THUMB_IMAGE_ALLOWED_EXTENSION);
            $calcFiles = $this->DpCalcFile->get('calcFilesSetID', $calcFileSet['ID'], true);
            foreach ($calcFiles as $calcFile) {
                if($calcFile['copyOf'] == 0){
                    $copies = $this->getCopies($calcFile);
                    $calcFile['copies'] = sizeof($copies);

                    $calcFile = $this->injectFileUrls($calcFile, STATIC_URL . companyID . '/'.$this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/', $calcFile['name']);

                    $calcFile['isFirstInGroup'] = true;
                    $calcFile['isLastInGroup'] = false;
                    $list[] = $calcFile;
                    foreach($copies as $copy){
                        $copy['isFirstInGroup'] = false;
                        $copy['isLastInGroup'] = false;
                        if($copy['ID'] == $copies[sizeof($copies)-1]['ID']){
                            $copy['isLastInGroup'] = true;
                        }
                        $list[] = $copy;
                    }
                }
            }
        }

        return $list;
    }

    public function delete_files($productID, $fileID)
    {

        $result = array();
        $user = $this->Auth->getLoggedUser();
        $userID = $user['ID'];
        if(!$userID){
            $userID = 0;
        }
        $one = $this->DpCalcFile->get('ID', $fileID);        

        if (!$one) {
            $result = $this->sendFailResponse('04');
        }


        $destFolder = $this->folder . '/' . $userID . '/' . $one['calcFilesSetID'] . '/';

        if ($this->Uploader->removeFromCompany($destFolder, $one['name'])) {
            $this->Uploader->removeFromCompany($destFolder.$this->miniaturesFolder.'/', $one['name']);
            $this->Uploader->removeFromCompany($destFolder.$this->orgFileFolder.'/', $one['name']);
            $this->Uploader->removeFromCompany($destFolder.$this->orgCroppedFileFolder.'/', $one['name']);

            $copies = $this->DpCalcFile->get('copyOf', $fileID, true);
            if(sizeof($copies) > 0){
                $firstCopy = $this->DpCalcFile->get('copyOf', $fileID);
                foreach($copies as $copy){
                    $this->DpCalcFile->update($copy['ID'], 'copyOf', $firstCopy['ID']);
                }
                $this->DpCalcFile->update($firstCopy['ID'], 'copyOf', 0);
            }

            if ($this->DpCalcFile->delete('ID', $one['ID'])) {

                $result = array('response' => true, 'removed_item' => $one);

            } else {

                $result = $this->sendFailResponse('05');

            }

        } else {

            $result = $this->sendFailResponse('05');

        }

        return $result;

    }

    public function createGuestSet($typeID){
        $userID = 0;
        $calcID = 0;
        $typeID = $typeID;
        $created = date('Y-m-d H:i:s');
        $calcFileSetID = $this->DpCalcFileSet->create(compact('userID', 'calcID', 'typeID', 'created'));

        return array('response' => true, 'calcFileSetID' => $calcFileSetID);
    }

    public function post_setCollectionToBW($setID){
        $calcFiles = $this->DpCalcFile->get('calcFilesSetID', $setID, true);
        $calcFilesRes = [];
        foreach($calcFiles as $calcFile){
            if($calcFile['isBW'] == 0){
                $calcFilesRes[] = $this->post_setImageBW($calcFile['ID'])['response'];
            }else{
                $calcFilesRes[] = $calcFile;
            }
        }

        $list = $this->createGroupSetAfterFilter($calcFilesRes, $setID);

        return array('response' => true, 'calcFiles' => $list);
    }

    public function post_setCollectionToSepia($setID){
        $calcFiles = $this->DpCalcFile->get('calcFilesSetID', $setID, true);
        $calcFilesRes = [];
        foreach($calcFiles as $calcFile){
            if($calcFile['isSepia'] == 0){
                $calcFilesRes[] = $this->post_setImageSepia($calcFile['ID'])['response'];
            }else{
                $calcFilesRes[] = $calcFile;
            }
        }

        $list = $this->createGroupSetAfterFilter($calcFilesRes, $setID);

        return array('response' => true, 'calcFiles' => $list);
    }

    public function post_removeCollectionFilters($setID){
        $calcFiles = $this->DpCalcFile->get('calcFilesSetID', $setID, true);
        $calcFilesRes = [];
        foreach($calcFiles as $calcFile){
            if($calcFile['isSepia'] == 1){
                $calcFilesRes[] = $this->post_setImageSepia($calcFile['ID'])['response'];
            }else if($calcFile['isBW'] == 1){
                $calcFilesRes[] = $this->post_setImageBW($calcFile['ID'])['response'];
            }else{
                $calcFilesRes[] = $calcFile;
            }
        }

        $list = $this->createGroupSetAfterFilter($calcFilesRes, $setID);

        return array('response' => true, 'calcFiles' => $list);
    }

    public function post_setImageBW($fileID){
        $calcFile = $this->DpCalcFile->get('ID', $fileID);

        $calcFileRes = $this->setImageProperty($calcFile, 'isBW');

        return array('response' => $calcFileRes);
    }

    public function post_setImageSepia($fileID){
        $calcFile = $this->DpCalcFile->get('ID', $fileID);

        $calcFileRes = $this->setImageProperty($calcFile, 'isSepia');

        return array('response' => $calcFileRes);
    }

    private function setImageProperty($calcFile, $field){
        $explodeName = explode('.', $calcFile['name']);
        $ext = end($explodeName);
        $sliced = array_slice($explodeName, 0, -1);
        $onlyFileName = implode("", $sliced);

        $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFile['calcFilesSetID']);
        $filename = $calcFile['name'];
        $destinationFolder =  $this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/';
        $destFilePath = MAIN_UPLOAD . companyID . '/' .$destinationFolder;
        $originalFile = $destFilePath . 'orgFiles/'.$filename;
        $originalCroppedFile = $destFilePath . $this->orgCroppedFileFolder.'/'.$filename;

        $this->createFolderIfDoesNotExists($destFilePath.$this->orgFileFolder);                        
        if(!file_exists($originalFile)){
            copy($destFilePath.$filename, $originalFile);
        }

        if($calcFile[$field] == 0){
            if($calcFile['isCropped'] == 1){
                $imagick = new Imagick($destFilePath.$this->orgCroppedFileFolder.'/'.$filename);
            }else{
                $imagick = new Imagick($destFilePath.$this->orgFileFolder.'/'.$filename);
            }

            if($field == 'isBW'){
                $imagick->setImageType(2);
            }else if($field == 'isSepia'){
                $imagick->sepiaToneImage(80);
            }

            $imagick->writeimage($destFilePath . $filename);
            $imagick->scaleImage($this->miniatureWidth, 0);
            $imagick->writeimage($destFilePath . $this->miniaturesFolder . '/' . $filename);

            if($field == 'isBW'){
                $this->DpCalcFile->update($calcFile['ID'], 'isBW', 1);
                $calcFile['isBW'] = 1;
                $this->DpCalcFile->update($calcFile['ID'], 'isSepia', 0);
                $calcFile['isSepia'] = 0;
                $newFileName = $onlyFileName.'BW.'.$ext;
            }if($field == 'isSepia'){
                $this->DpCalcFile->update($calcFile['ID'], 'isBW', 0);
                $calcFile['isBW'] = 0;
                $this->DpCalcFile->update($calcFile['ID'], 'isSepia', 1);
                $calcFile['isSepia'] = 1;
                $newFileName = $onlyFileName.'SEP.'.$ext;
            }            
        }else{
            if($calcFile['isCropped'] == 1){
                copy($originalCroppedFile, $destFilePath.$filename);
            }else{
                copy($originalFile, $destFilePath.$filename);
            }
            $imagick = new Imagick($destFilePath.$filename);            
            $imagick->scaleImage($this->miniatureWidth, 0);
            $imagick->writeimage($destFilePath . $this->miniaturesFolder . '/' . $filename);

            $newOnlyFileName = str_replace(array('SEP', 'BW'), '', $onlyFileName.rand(0,100));
            $newFileName = $newOnlyFileName.'.'.$ext;
            
            $this->DpCalcFile->update($calcFile['ID'], 'isBW', 0);
            $this->DpCalcFile->update($calcFile['ID'], 'isSepia', 0);
            $calcFile['isBW'] = 0;
            $calcFile['isSepia'] = 0;
        }   

        rename($originalCroppedFile, $destFilePath . $this->orgCroppedFileFolder . '/'.$newFileName);
        rename($originalFile, $destFilePath . $this->orgFileFolder . '/'.$newFileName);
        rename($destFilePath.$filename, $destFilePath.$newFileName);
        rename($destFilePath.$this->miniaturesFolder .'/'.$filename, $destFilePath.$this->miniaturesFolder .'/'.$newFileName);

        $calcFile = $this->injectFileUrls($calcFile, STATIC_URL . companyID . '/' . $destinationFolder, $newFileName);

        $this->DpCalcFile->update($calcFile['ID'], 'name', $newFileName);
        $calcFile['name'] = $newFileName;

        return $calcFile;
    }

    public function post_cropImage($fileID){
        $post = $this->Data->getAllPost();
        $calcFile = $this->DpCalcFile->get('ID', $fileID);

        $explodeName = explode('.', $calcFile['name']);
        $ext = end($explodeName);
        $sliced = array_slice($explodeName, 0, -1);
        $onlyFileName = implode("", $sliced);
        $newFileName = rand(0, 100).$calcFile['originalFileName'];

        $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFile['calcFilesSetID']);
        $filename = $calcFile['name'];
        $destinationFolder =  $this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/';
        $destFilePath = MAIN_UPLOAD . companyID . '/' .$destinationFolder;
        $originalFile = $destFilePath . $this->orgFileFolder . '/'.$filename;
        $originalCroppedFile = $destFilePath . $this->orgCroppedFileFolder.'/'.$filename;

 
        $this->createFolderIfDoesNotExists($destFilePath.$this->orgFileFolder);
        $this->createFolderIfDoesNotExists($destFilePath.$this->orgCroppedFileFolder);            
        if(!file_exists($originalFile)){
            copy($destFilePath.$filename, $originalFile);
        }

        $imagick = new Imagick($destFilePath.$this->orgFileFolder.'/'.$filename);

        $imagick->cropImage(ceil($post['width']), ceil($post['height']), ceil($post['x']), ceil($post['y']));
        $geo = $imagick->getImageGeometry();
        $width = $geo['width'];
        $height = $geo['height'];
        $this->DpCalcFile->update($calcFile['ID'], 'width', $width);
        $calcFile['width'] = $width;
        $this->DpCalcFile->update($calcFile['ID'], 'height', $height);
        $calcFile['height'] = $height;

        $imagick->writeimage($destFilePath . $filename);
        $imagick->writeimage($destFilePath . $this->orgCroppedFileFolder . '/' . $filename);
        $imagick->scaleImage($this->miniatureWidth, 0);
        $imagick->writeimage($destFilePath . $this->miniaturesFolder . '/' . $filename);

        $this->DpCalcFile->update($calcFile['ID'], 'cropData', $post['json']);
        $calcFile['cropData'] = $post['json'];
        $this->DpCalcFile->update($calcFile['ID'], 'isCropped', 1);
        $calcFile['isCropped'] = 1;
        $this->DpCalcFile->update($calcFile['ID'], 'isBW', 0);
        $this->DpCalcFile->update($calcFile['ID'], 'isSepia', 0);            
        if($calcFile['isBW'] == 1){
            $calcFile['isBW'] = 0;
            $calcFile = $this->setImageProperty($calcFile, 'isBW');
            $filename = $calcFile['name'];
        }
        if($calcFile['isSepia'] == 1){
            $calcFile['isSepia'] = 0;
            $calcFile = $this->setImageProperty($calcFile, 'isSepia');
            $filename = $calcFile['name'];
        }
        $calcFile['isCropped'] = 1;

        $originalFile = $destFilePath . $this->orgFileFolder . '/'.$filename;
        $originalCroppedFile = $destFilePath . $this->orgCroppedFileFolder.'/'.$filename;
        
        rename($originalCroppedFile, $destFilePath . $this->orgCroppedFileFolder . '/'.$newFileName);
        rename($originalFile, $destFilePath . $this->orgFileFolder . '/'.$newFileName);
        rename($destFilePath.$filename, $destFilePath.$newFileName);
        rename($destFilePath.$this->miniaturesFolder .'/'.$filename, $destFilePath.$this->miniaturesFolder .'/'.$newFileName);
        $this->DpCalcFile->update($calcFile['ID'], 'name', $newFileName);
        $calcFile['name'] = $newFileName;

        $calcFile = $this->injectFileUrls($calcFile, STATIC_URL . companyID . '/' . $destinationFolder, $newFileName);

        return array('success' => true, 'response' => $calcFile);
    }

    public function post_restoreImage($fileID){
        $calcFile = $this->DpCalcFile->get('ID', $fileID);

        $explodeName = explode('.', $calcFile['name']);
        $ext = end($explodeName);
        $sliced = array_slice($explodeName, 0, -1);
        $onlyFileName = implode("", $sliced);
        $newFileName = rand(0, 100).$calcFile['originalFileName'];

        $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFile['calcFilesSetID']);
        $filename = $calcFile['name'];
        $destinationFolder =  $this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/';
        $destFilePath = MAIN_UPLOAD . companyID . '/' .$destinationFolder;
        $originalFile = $destFilePath . $this->orgFileFolder . '/'.$filename;
        $originalCroppedFile = $destFilePath . $this->orgCroppedFileFolder.'/'.$filename;
        
        if(file_exists($originalFile)){
            copy($originalFile, $destFilePath.$filename);

            $imagick = new Imagick($destFilePath.$filename);
            $geo = $imagick->getImageGeometry();
            $width = $geo['width'];
            $height = $geo['height'];
            $this->DpCalcFile->update($calcFile['ID'], 'width', $width);
            $calcFile['width'] = $width;
            $this->DpCalcFile->update($calcFile['ID'], 'height', $height);
            $calcFile['height'] = $height;

            $imagick->scaleImage($this->miniatureWidth, 0);
            $imagick->writeimage($destFilePath . $this->miniaturesFolder . '/' . $filename);

            $this->DpCalcFile->update($calcFile['ID'], 'isBW', 0);
            $calcFile['isBW'] = 0;
            $this->DpCalcFile->update($calcFile['ID'], 'isSepia', 0);
            $calcFile['isSepia'] = 0;
            $this->DpCalcFile->update($calcFile['ID'], 'isCropped', 0);
            $calcFile['isCropped'] = 0;
            $this->DpCalcFile->update($calcFile['ID'], 'editData', NULL);
            $calcFile['editData'] = NULL;

            rename($originalCroppedFile, $destFilePath . $this->orgCroppedFileFolder . '/'.$newFileName);
            rename($originalFile, $destFilePath . $this->orgFileFolder . '/'.$newFileName);
            rename($destFilePath.$filename, $destFilePath.$newFileName);
            rename($destFilePath.$this->miniaturesFolder .'/'.$filename, $destFilePath.$this->miniaturesFolder .'/'.$newFileName);
            $this->DpCalcFile->update($calcFile['ID'], 'name', $newFileName);
            $calcFile['name'] = $newFileName;

            $calcFile = $this->injectFileUrls($calcFile, STATIC_URL . companyID . '/' . $destinationFolder, $newFileName);

            return array('success' => true, 'response' => $calcFile);
        }

        return array('success' => false);
    }

    public function post_copyImage($fileID){
        $calcFile = $this->DpCalcFile->get('ID', $fileID);

        $copyPrefix = '_(1)';
        $explodeName = explode('.', $calcFile['name']);
        $ext = end($explodeName);
        $sliced = array_slice($explodeName, 0, -1);
        $onlyFileName = implode("", $sliced);

        $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFile['calcFilesSetID']);
        $filename = $calcFile['name'];
        $destinationFolder =  $this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/';
        $destFilePath = MAIN_UPLOAD . companyID . '/' .$destinationFolder;
        $originalFile = $destFilePath . $this->orgFileFolder . '/'.$filename;
        $newFileName = $onlyFileName . $copyPrefix . '.' . $ext;
        
        $this->createFolderIfDoesNotExists($destFilePath.$this->orgFileFolder);
        if(!file_exists($originalFile)){
            copy($destFilePath.$filename, $originalFile);
        }

        $versionCount = 2;
        while(file_exists($destFilePath.$newFileName)){
            $newFileName = $onlyFileName . '_('. $versionCount . ').' . $ext;
            $versionCount++;
        }

        copy($originalFile, $destFilePath.$newFileName);

        $name = $newFileName;
        $calcFilesSetID = $calcFile['calcFilesSetID'];
        $created = date('Y-m-d H:i:s');
        $originalFileName = $newFileName;
        if($calcFile['copyOf'] == 0){
            $copyOf = $calcFile['ID'];
        }else{
            $copyOf = $calcFile['copyOf'];
        }
        
        $imagick = new Imagick($destFilePath.$newFileName);
        $geo = $imagick->getImageGeometry();
        $width = $geo['width'];
        $height = $geo['height'];

        $imagick->scaleImage($this->miniatureWidth, 0);
        $imagick->writeimage($destFilePath . $this->miniaturesFolder . '/' . $newFileName);

        $newCalcFileID = $this->DpCalcFile->create(compact('name', 'calcFilesSetID', 'created', 'originalFileName', 'copyOf', 'width', 'height'));

        $newCalcFile = $this->DpCalcFile->get('ID', $newCalcFileID);

        $newCalcFile = $this->injectFileUrls($newCalcFile, STATIC_URL . companyID . '/' . $destinationFolder, $newFileName);

        return array('success' => true, 'response' => $newCalcFile);
    }

    public function patch_changeQty($fileID){
        $post = $this->Data->getAllPost();
        $newQty = $post['newQty'];
        $success = $this->DpCalcFile->update($fileID, 'qty', $newQty);
        $newCalcFile = $calcFile = $this->DpCalcFile->get('ID', $fileID);

        return array('success' => $success, 'file' => $newCalcFile);
    }

    public function post_editImage($fileID){
        $calcFile = $this->DpCalcFile->get('ID', $fileID);

        $copyPrefix = 'ee';
        $explodeName = explode('.', $calcFile['name']);
        $ext = end($explodeName);
        $sliced = array_slice($explodeName, 0, -1);
        $onlyFileName = implode("", $sliced);

        $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFile['calcFilesSetID']);
        $filename = $calcFile['name'];
        $destinationFolder =  $this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/';
        $destFilePath = MAIN_UPLOAD . companyID . '/' .$destinationFolder;
        $originalFile = $destFilePath . $this->orgFileFolder . '/'.$filename;
        $originalCroppedFile = $destFilePath . $this->orgCroppedFileFolder.'/'.$filename;
        $newFileName = $onlyFileName . $copyPrefix . '.' . $ext;

        $post = $this->Data->getAllPost();
        $brightness = $post['brightness'];
        $contrast = $post['contrast'];
        $success = true;

        if($calcFile['isCropped'] == 1){
            $imagick = new Imagick($destFilePath.$this->orgCroppedFileFolder.'/'.$filename);
        }else{
            $imagick = new Imagick($destFilePath.$this->orgFileFolder.'/'.$filename);
        }
        $imagick->brightnessContrastImage($brightness - 100, $contrast - 100);
        $imagick->writeimage($destFilePath . $newFileName);
        $imagick->scaleImage($this->miniatureWidth, 0);
        $imagick->writeimage($destFilePath . $this->miniaturesFolder . '/' . $newFileName);

        $editData = array('brightness' => $brightness, 'contrast' => $contrast);
        $jsonEditData = json_encode($editData, JSON_FORCE_OBJECT);
        $this->DpCalcFile->update($fileID, 'editData', $jsonEditData);
        $calcFile['editData'] = $jsonEditData;
        $this->DpCalcFile->update($fileID, 'name', $newFileName);
        $calcFile['name'] = $newFileName;

        rename($originalCroppedFile, $destFilePath . $this->orgCroppedFileFolder . '/'.$newFileName);
        rename($originalFile, $destFilePath . $this->orgFileFolder . '/'.$newFileName);

        $calcFile = $this->injectFileUrls($calcFile, STATIC_URL . companyID . '/' . $destinationFolder, $newFileName);

        return array('success' => $success, 'file' => $calcFile);
    }

    private function cleanString($string) {
        $string = str_replace(' ', '-', $string);
     
        return preg_replace('/[^A-Za-z0-9\-]/', '', $string);
     }

     private function createFolderIfDoesNotExists($dir){
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
            chmod($dir, 0755);
        }
     } 
     
     private function getCopies($calcFile){
        $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFile['calcFilesSetID']);
        $copies = $this->DpCalcFile->get('copyOf', $calcFile['ID'], true);
        foreach ($copies as &$calcFile) {
            $calcFile = $this->injectFileUrls($calcFile, STATIC_URL . companyID . '/'.$this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/', $calcFile['name']);
       }    
       return $copies;
     }

     private function createGroupSetAfterFilter($calcFilesRes, $calcFilesSetID){
        $list = array();
        $calcFileSet = $this->DpCalcFileSet->get('ID', $calcFilesSetID);
        foreach ($calcFilesRes as $calcFile) {
            if($calcFile['copyOf'] == 0){
                $filename = $calcFile['name'];
                $destinationFolder =  $this->folder.'/'.$calcFileSet['userID'].'/'.$calcFileSet['ID'].'/';
                $calcFile = $this->injectFileUrls($calcFile, STATIC_URL . companyID . '/' . $destinationFolder, $filename);
                $copies = $this->getCopies($calcFile);
                $calcFile['copies'] = sizeof($copies);
                $calcFile['isFirstInGroup'] = true;
                $calcFile['isLastInGroup'] = false;
                $list[] = $calcFile;
                foreach($copies as $copy){
                    $copy['isFirstInGroup'] = false;
                    $copy['isLastInGroup'] = false;
                    if($copy['ID'] == $copies[sizeof($copies)-1]['ID']){
                        $copy['isLastInGroup'] = true;
                    }
                    $list[] = $copy;
                }
            }
        }

        return $list;
    }

    private function injectFileUrls($object, $mainPath, $filename) {
            $orgFileURL = $mainPath . $this->orgFileFolder .'/'. $filename;
            $originalCroppedUrl = $mainPath . $this->orgCroppedFileFolder .'/'. $filename;
            $miniatureURL = $mainPath . $this->miniaturesFolder .'/'. $filename;
            $object['url'] = $mainPath . $filename;
            $object['originalUrl'] = $orgFileURL;
            $object['originalCroppedUrl'] = $originalCroppedUrl;
            $object['miniature'] = $miniatureURL;

        return $object;
    }

}
