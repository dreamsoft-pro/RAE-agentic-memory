<?php

namespace DreamSoft\Models\Other;

use DreamSoft\Core\Model;

class Country extends Model
{

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('countries', true);
    }

    public function getCountries()
    {
        $query = 'SELECT code, areaCode, name_pl, name_en, name_de FROM `dp_countries` WHERE NOT disabled=1 ORDER BY isDefault DESC, code ASC';

        $this->db->exec($query);
        $result = $this->db->getAll();
        if (!in_array(lang, ['pl', 'en', 'de'])) {
            foreach ($result as &$item) {
                $item['name_' . lang] = $item['name_en'];
            }
        }
        return $result;
    }

    public function getAll()
    {
        $query = 'SELECT * FROM `dp_countries`';

        if (!$this->db->exec($query)) {
            return false;
        }

        $result = $this->db->getAll();

        return $result;
    }

    public function updateDisabledAndDefault($code, $disabled, $default)
    {
        $query = 'UPDATE  `dp_countries` SET `disabled` = :disabled , `isDefault` = :default WHERE code = :code ';
        $binds['code'] = $code;
        $binds['disabled'] = $disabled;
        $binds['default'] = $default;

        if (!$this->db->exec($query, $binds)) {
            return false;
        } else {
            return true;
        }
    }
}
