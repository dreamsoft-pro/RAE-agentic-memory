<?php

namespace DreamSoft\Models\Other;

use DreamSoft\Core\Model;
use PDO;

/**
 * Class ModelIconExtension
 */
class ModelIconExtension extends Model
{

    /**
     * ModelIconExtension constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('modelsIconsExtensions', true);
    }

    public function getExtensions(){
        $this->db->exec('select * from dp_modelsIconsExtensions');
        return $this->db->getAll();
    }

    public function isAllowedFile($name):bool{
        $this->db->exec('select extension from dp_modelsIconsExtensions');
        $all=$this->db->getAll(PDO::FETCH_COLUMN);;
        $ext = ModelIconExtension::getExtension($name);
        return in_array($ext,$all);
    }
    public function nameToModelExtensionID($name):int{
        $this->db->exec('select ID,baseExtensionID from dp_modelsIconsExtensions 
            where extension=:extension and not baseExtensionID=ID',['extension'=> ModelIconExtension::getExtension($name)]);
        $row=$this->db->getRow();
        if($row){
            $this->db->exec('select ID from dp_modelsIconsExtensions 
            where ID=:ID',['ID'=>$row['baseExtensionID']]);
            $row=$this->db->getOne();
        }else{
            $this->db->exec('select ID,baseExtensionID from dp_modelsIconsExtensions 
            where extension=:extension',['extension'=> ModelIconExtension::getExtension($name)]);
            $row=$this->db->getOne();
        }
        return $row;
    }

    public static function getExtension($name): string
    {
        $parts = preg_split('/\./', $name);
        return strtolower(array_pop($parts));
    }
}
