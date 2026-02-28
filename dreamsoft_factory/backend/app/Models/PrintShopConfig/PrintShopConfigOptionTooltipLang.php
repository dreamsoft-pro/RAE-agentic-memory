<?php

namespace DreamSoft\Models\PrintShopConfig;

use DreamSoft\Core\Model;

class PrintShopConfigOptionTooltipLang extends Model
{

    public function __construct()
    {
        parent::__construct();
        $this->prefix = 'ps_';
        $this->setTableName('config_option_tooltip_lang', true);
    }

    /**
     * @param $lang
     * @param $name
     * @param $optionID
     * @return bool
     */
    public function set($lang, $tooltip, $optionID)
    {
        $ID = $this->exist($optionID, $lang);
        if ($ID===false) {
            $lastID = $this->create(compact('lang', 'tooltip', 'optionID'));
            if ($lastID > 0) {
                return true;
            }
        } else {
            $res = $this->update($ID, 'tooltip', $tooltip);
            return $res;
        }
        return false;
    }


    /**
     * @param $optionID
     * @param $lang
     * @return mixed
     */
    public function exist($optionID, $lang)
    {
        $query = 'SELECT ID FROM `' . $this->getTableName() . '` WHERE `lang` = :lang AND `optionID` = :optionID ';
        $binds['lang'] = $lang;
        $binds['optionID'] = $optionID;

        $this->db->exec($query, $binds);

        return $this->db->getOne();
    }

}
