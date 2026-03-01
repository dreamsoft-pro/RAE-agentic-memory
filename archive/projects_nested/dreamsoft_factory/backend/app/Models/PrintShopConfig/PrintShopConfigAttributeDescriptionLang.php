<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Core\Model;

class PrintShopConfigAttributeDescriptionLang extends Model
{

    public function __construct()
    {
        parent::__construct();
        $this->prefix = 'ps_';
        $this->setTableName('config_attribute_description_lang', true);
    }

    public function set($lang, $description, $attributeID)
    {
        $ID = $this->exist($attributeID, $lang);
        if (!$ID) {
            $lastID = $this->create(compact('lang', 'description', 'attributeID'));
            if ($lastID > 0) {
                return true;
            }
        } else {
            $res = $this->update($ID, 'description', $description);
            return $res;
        }
        return false;
    }

    public function exist($attributeID, $lang)
    {
        $query = 'SELECT ID FROM `' . $this->getTableName() . '` WHERE `lang` = :lang AND `attributeID` = :attributeID ';
        $binds['lang'] = $lang;
        $binds['attributeID'] = $attributeID;

        $this->db->exec($query, $binds);

        return $this->db->getOne();
    }

}
