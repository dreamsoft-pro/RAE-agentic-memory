<?php
namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

/**
 * Class Shift
 * @package DreamSoft\Models\ProductionPath
 */
class Shift extends Model
{
    /**
     * Shift constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('production_shifts', true);
    }

    /**
     * @return bool|mixed
     */
    public function getMaxSort()
    {
        $query = ' SELECT MAX(production_shifts.`sort`) FROM `' . $this->getTableName() . '` as production_shifts LIMIT 1';
        if (!$this->db->exec($query)) {
            return false;
        }
        return $this->db->getOne();
    }

    /**
     * @param $shifts
     * @return bool|array
     */
    public function sort($shifts)
    {
        $result = true;
        foreach ($shifts as $index => $ID) {
            if (empty($ID)) {
                continue;
            }

            $query = 'UPDATE `' . $this->getTableName() . '` SET `sort` = :index WHERE `ID` = :ID ';

            $binds['ID'] = array($ID, 'int');
            $binds['index'] = $index+1;
            if (!$this->db->exec($query, $binds)) {
                $result = false;
            }
        }
        return $result;
    }

    public function getDayFinishHour(){
        $query = 'SELECT * FROM `' . $this->getTableName() . '` ORDER BY stop DESC LIMIT 1';
        if (!$this->db->exec($query)) {
            return false;
        }
        return $this->db->getRow();
    }

    public function getDayStartHour(){
        $query = 'SELECT * FROM `' . $this->getTableName() . '` ORDER BY start ASC LIMIT 1';
        if (!$this->db->exec($query)) {
            return false;
        }
        return $this->db->getRow();
    }
}