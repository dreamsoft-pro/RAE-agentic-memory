<?php

namespace DreamSoft\Models\Group;

use DreamSoft\Core\Model;

class Group extends Model
{

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('groups', true);
    }

    /**
     * @return bool
     */
    public function getList()
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` ';
        $binds = array();
        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();
    }

    /**
     * @param $name
     * @param $desc
     * @return bool|string
     */
    public function customCreate($name, $desc)
    {
        $query = ' SELECT MAX(ID) FROM `' . $this->getTableName() . '` LIMIT 1';
        if ($this->db->exec($query)) {
            $tmpLast = $this->db->getOne();
            $tmpLast++;
        }

        $query = 'INSERT INTO `' . $this->getTableName() . '` (
              `ID`,
              `name`,
              `desc`
              ) VALUES (
              :tmpLast,  
              :name,
              :desc
              ) 
            ';
        $binds[':tmpLast'] = $tmpLast;
        $binds[':name'] = $name;
        $binds[':desc'] = $desc;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->lastInsertId();
    }
}