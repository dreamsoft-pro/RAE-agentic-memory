<?php
namespace DreamSoft\Traits;
use DreamSoft\Controllers\Components\Uploader;

trait ImagePathTrait{
    public function addUrls(array &$file, $calcProductID): void
    {
        if (empty($file)) {
            return;
        }
        $allowedThumbExtension=explode(',', THUMB_IMAGE_ALLOWED_EXTENSION);
        $explodeName = explode('.', $file['name']);
        $ext = end($explodeName);

        $minImageName = false;

        if ($ext == THUMB_PDF_ALLOWED_EXTENSION) {
            array_pop($explodeName);
            $minImageName = implode('.', $explodeName) . '.jpg';
        } else if (in_array($ext, $allowedThumbExtension)) {
            $minImageName = $file['name'];
        }

        $file['url'] = STATIC_URL . companyID . '/' . Uploader::getUploadPath($calcProductID, $file['ID']) . $file['name'];

        if ($minImageName) {
            $file['minUrl'] = STATIC_URL . companyID . '/' . Uploader::getUploadPath($calcProductID, $file['ID']) . THUMB_IMAGE_PREFIX . $minImageName;
        } else {
            $file['minUrl'] = STATIC_URL . companyID . '/' . 'images' . '/' . THUMB_IMAGE_DEFAULT;
        }
    }
}
