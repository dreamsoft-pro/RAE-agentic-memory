<?php

namespace DreamSoft\Controllers\Components;
/**
 * Description of Uploader
 *
 * @author Rafał
 */
use DreamSoft\Core\Component;
use DreamSoft\Models\Other\ModelIconExtension;
use Exception;
use Imagick;
use ImagickException;

class Uploader extends Component
{

    public function __construct()
    {
        parent::__construct();
    }

    /**
     * @param $productID
     * @param $fileID
     * @return string Path with closing slash
     */
    public static function getUploadPath($productID, $fileID)
    {
        return 'productFiles/' . $productID . '/' . $fileID . '/';
    }
    public static function getPrevUrl($product, $files)
    {

        if(count($files)>0){
            $name = preg_replace('/\.pdf$/', '.jpg', $files[0]['name']);
            $prevFile = MAIN_UPLOAD . companyID . '/' . Uploader::getUploadPath($product['calcProducts'][0]['ID'], $files[0]['ID']) . 'prev-' . $name;
            if (is_file($prevFile)) {
                return STATIC_URL . companyID . '/' . Uploader::getUploadPath($product['calcProducts'][0]['ID'], $files[0]['ID']) . 'prev-' . $name;
            }
        }
        return false;
    }
    public static function getMiniatureName($fileName){
        $explodeName = explode('.', $fileName);
        $ext = end($explodeName);

        $minImageName = false;

        $allowedThumbExtension = explode(',', THUMB_IMAGE_ALLOWED_EXTENSION);

        if (strtolower($ext) == THUMB_PDF_ALLOWED_EXTENSION) {
            array_pop($explodeName);
            $minImageName = implode('.', $explodeName) . '.jpg';
        } else if( in_array(strtolower($ext), $allowedThumbExtension) ) {
            $minImageName = $fileName;
        }
        return $minImageName ? THUMB_IMAGE_PREFIX .$minImageName : false;
    }
    /**
     *
     *
     * @param {String} $_file
     * @param {String} $fileName
     * @param {String} $destFolder
     * @param {String} $newName
     * @return boolean
     */
    public function upload($_file, $fileName, $destFolder, $destinationFileName, $generateUniqueFileName=false)
    {

        if (!isset($_file[$fileName]) || !is_uploaded_file($_file[$fileName]['tmp_name'])) {
            return false;
        }
        $dir = MAIN_UPLOAD . $destFolder;

        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
            chmod($dir, 0755);
        }

        if ($generateUniqueFileName && is_file($dir . $destinationFileName)) {
            $nameParts = explode('.', $destinationFileName);
            for ($i = 1; ; $i++) {
                $generatedFileName = $nameParts[0] . '_' . $i . '.' . $nameParts[1];
                if (!is_file($dir . $generatedFileName)) {
                    $destinationFileName = $generatedFileName;
                    break;
                }
            }
        }

        $file = $dir . $destinationFileName;

        if (move_uploaded_file($_file[$fileName]['tmp_name'], $file)) {
            chmod($file, 0777);
            return $destinationFileName;
        }
        return false;

    }

    /**
     * @param $destinationFolder
     * @param $name
     * @return bool
     */
    public function remove($destinationFolder, $name, $withMiniature=false)
    {
        $file = MAIN_UPLOAD . $destinationFolder . $name;

        if (!is_file($file)) {
            return true;
        }
        if ($withMiniature) {
            $miniature = MAIN_UPLOAD . $destinationFolder . self::getMiniatureName($name);
            unlink($miniature);
        }
        if (unlink($file)) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * @param $_file
     * @param $fileName
     * @param $destinationFolder
     * @param $newName
     * @return bool
     */
    public function uploadToCompany($_file, $fileName, $destinationFolder, $newName)
    {

        if (!isset($_file[$fileName]) || !is_uploaded_file($_file[$fileName]['tmp_name'])) {
            return false;
        }

        $dir = MAIN_UPLOAD . companyID . '/' . $destinationFolder;
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
            chmod($dir, 0755);
        }

        $file = $dir . $newName;
        while (is_file($dir . $newName)) {
            $ext = ModelIconExtension::getExtension($newName);
            $newName = preg_replace(".$ext", '', $newName);
            $newName .= '_';
            $newName .= ".$ext";
        }

        if (move_uploaded_file($_file[$fileName]['tmp_name'], $file)) {
            chmod($file, 0755);
            return $newName;
        }

        return false;
    }

    public function uploadTemporary($postFileName, $fileName=null)
    {
        $postFile = $_FILES[$postFileName];
        if(!$fileName){
            $fileName=$postFile['name'];
        }
        ini_set('max_execution_time', 720);
        $dir = STATIC_PATH . companyID . '/tmp/';// TODO STATIC_PATH should be moved to another
        if (!is_dir($dir)) {
            mkdir($dir, 0777, true);
        }
        $path = $dir . $fileName;

        if (move_uploaded_file($postFile['tmp_name'], $path)) {
            return $path;
        } else {
            return false;
        }
    }

    public function removeTemporary($filePath)
    {
        if (unlink($filePath)) {
            return true;
        } else {
            return false;
        }
    }


    public function removeFromCompany($destFolder, $name)
    {

        $file = MAIN_UPLOAD . companyID . '/' . $destFolder . $name;
        $minFile = MAIN_UPLOAD . companyID . '/' . $destFolder . THUMB_IMAGE_PREFIX . $name;
        $ext = ModelIconExtension::getExtension($name);
        $originalFile = MAIN_UPLOAD . companyID . '/' . $destFolder . preg_replace('/-mod\.' . $ext . '/', '.' . $ext, $name);

        $res = true;
        if (is_file($file)) {
            $res = unlink($file);
        }
        if ($res && is_file($minFile)) {
            $res = unlink($minFile);
        }
        if ($res && is_file($originalFile)) {
            $res = unlink($originalFile);
        }
        return $res;

    }

    /**
     * @param $imagePath
     * @param $width
     * @param $height
     * @param $cropZoom
     * @return Imagick
     * @throws ImagickException
     */
    function resizeImage($imagePath, $width, $height, $cropZoom)
    {
        $explodedString = explode('.', $imagePath);
        $ext = end($explodedString);

        if( $ext == 'pdf' ) {
            $imagick = new Imagick();
            $imagick->readImage(realpath($imagePath));
            $imagick->setImageFormat('jpg');
        } else {
            $imagick = new Imagick(realpath($imagePath));
        }

        $imageProps = $imagick->getImageGeometry();
        if ($imageProps['width'] > $width || $imageProps['height'] > $height) {
            $imagick->resizeImage($width, $height, imagick::FILTER_LANCZOS, 0.9, true);
        }



        if ($cropZoom) {

            $cropWidth = $imagick->getImageWidth();
            $cropHeight = $imagick->getImageHeight();

            $newWidth = $cropWidth / 2;
            $newHeight = $cropHeight / 2;

            $imagick->cropimage(
                $newWidth,
                $newHeight,
                ($cropWidth - $newWidth) / 2,
                ($cropHeight - $newHeight) / 2
            );

            $imagick->scaleimage(
                $imagick->getImageWidth() * 4,
                $imagick->getImageHeight() * 4
            );
        }

        return $imagick;
    }

}
