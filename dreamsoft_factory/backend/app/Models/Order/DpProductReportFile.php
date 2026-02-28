<?php

namespace DreamSoft\Models\Order;

use DreamSoft\Controllers\Components\Uploader;
use DreamSoft\Core\Model;
use DreamSoft\Models\Upload\UploadFile;

class DpProductReportFile extends Model
{

    const UPLOAD_PATH = 'uploadedFiles/' . companyID;
    /**
     * @var Uploader
     */
    private $Uploader;
    /**
     * @var UploadFile
     */
    private $UploadFile;

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('product_report_files', true);
        $this->Uploader = Uploader::getInstance();
        $this->UploadFile = UploadFile::getInstance();
    }

    public function getFilesForProduct($productID)
    {
        $query = 'select name, path, created, acceptChangeDate, acceptRejectUserName, accept, ID, `comment`, uploadedFiles.ID fileID from dp_product_report_files 
                join uploadedFiles on uploadedFiles.ID=dp_product_report_files.fileID
                where productID=:productID';
        if (!$this->db->exec($query, [':productID' => $productID])) {
            return false;
        }
        return $this->db->getAll();
    }

    public function getFile($fileID)
    {
        $query = 'select name, path, created, acceptChangeDate, acceptRejectUserName, accept, ID, `comment` from dp_product_report_files 
                join uploadedFiles on uploadedFiles.ID=dp_product_report_files.fileID
                where fileID=:fileID';
        if (!$this->db->exec($query, [':fileID' => $fileID])) {
            return false;
        }
        return $this->db->getRow();
    }

    public function deleteByUploadID($uploadFileID)
    {
        $query = 'delete from dp_product_report_files where fileID = :fileID';
        if (!$this->db->exec($query, [':fileID' => $uploadFileID])) {
            throw new Exception('nie usunięto');
        }
        return true;
    }

    public function countFilesForProduct($productID)
    {
        $query = 'select count(1) from dp_product_report_files 
                where productID=:productID';
        if (!$this->db->exec($query, [':productID' => $productID])) {
            return false;
        }
        return $this->db->getOne();
    }

    public function getByOrderList($orders)
    {
        if (!$orders) {
            return false;
        }
        $query = 'SELECT r.comment, r.accept, r.acceptChangeDate, r.productID, u.name, u.ID, u.path, u.created
            FROM  `dp_product_report_files` AS r
            JOIN  `uploadedFiles` AS u ON u.ID = r.`fileID`
            LEFT JOIN  `dp_products` AS p ON p.ID = r.`productID`
            LEFT JOIN  `dp_orders` AS o ON o.ID = p.`orderID`
            WHERE o.`ID` IN  (' . implode(',', $orders) . ')';

        if (!$this->db->exec($query)) {
            return false;
        }

        $res = $this->db->getAll();
        if (!$res) return false;

        return $res;
    }

    public function setAccepted($fileID, $userID, $userName)
    {
        $query = 'update dp_product_report_files set accept=1, 
                                   acceptChangeDate=CURRENT_TIMESTAMP(),
                                   acceptRejectUserID=:acceptRejectUserID,
                                   acceptRejectUserName=:acceptRejectUserName
                    where fileID=:fileID';
        if ($this->db->exec($query, ['fileID' => $fileID,
            'acceptRejectUserID' => $userID,
            'acceptRejectUserName' => $userName])) {
            return true;
        }
        return false;
    }

    public function setRejected($fileID, $comment, $userID, $userName)
    {
        $query = 'update dp_product_report_files set accept=-1, 
                                   acceptChangeDate=CURRENT_TIMESTAMP(),
                                   comment=:comment,
                                   acceptRejectUserID=:acceptRejectUserID,
                                   acceptRejectUserName=:acceptRejectUserName
                    where fileID=:fileID';
        if ($this->db->exec($query, [
            'fileID' => $fileID,
            'comment' => $comment,
            'acceptRejectUserID' => $userID,
            'acceptRejectUserName' => $userName
        ])) {
            return true;
        }
        return false;
    }

    public function deleteAllForProduct($productID)
    {
        foreach ($this->getFilesForProduct($productID) as $file) {
            if (!$this->delete(['fileID', 'productID'], [$file['fileID'], $productID])) {
                return false;
            }
            if(!$this->UploadFile->delete('ID', $file['fileID'])){
                return false;
            }
            if (!$this->Uploader->remove(DpProductReportFile::UPLOAD_PATH . '/' . $file['path'], $file['name'])) {
                return false;
            }

        }
        return true;
    }
}
