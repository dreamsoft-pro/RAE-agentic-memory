<?php
declare(strict_types=1);

namespace DreamSoft\Libs\LabelImposition\Services;

use RuntimeException;

class LabelFilePreparer
{
    public function __construct()
    {

    }

    public function savelFileLocally(string $url): array
    {
        $path = basePath() . '/public/temporaryFiles/';
        if (!is_dir($path)) {
            if (!mkdir($path, 0777, true) && !is_dir($path)) {
                throw new RuntimeException(sprintf('Directory "%s" was not created', $path));
            }
        }

        $filePath = $path . md5($url);

        if (!file_exists($filePath)) {
            file_put_contents($filePath, file_get_contents($url));
        }

        return [
            'path' => $filePath,
            'type' => $this->checkMimeType($filePath)
        ];
    }

    public function checkMimeType(string $filePath): string
    {
        $finfo = finfo_open(FILEINFO_MIME_TYPE);
        $mime = finfo_file($finfo, $filePath);
        finfo_close($finfo);

        if ($this->isPdf($mime)) {
            $mime = 'pdf';
        } elseif ($this->isImage($mime)) {
            $mime = 'image';
        }

        return $mime;
    }

    private function isPdf(string $mime): bool
    {
        return $mime === 'application/pdf';
    }

    private function isImage(string $mime): bool
    {
        return strpos($mime, 'image/') === 0;
    }

    public static function dateName(){
        return date('\YY\Mm\Dd\t\i\m\eHis');
    }
}
