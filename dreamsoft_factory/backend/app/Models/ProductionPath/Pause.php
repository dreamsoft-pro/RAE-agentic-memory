<?php
/**
 * Created by PhpStorm.
 * User: Rafał
 * Date: 10-07-2018
 * Time: 12:02
 */

namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

/**
 * Class Pause
 * @package DreamSoft\Models\ProductionPath
 */
class Pause extends Model
{
    /**
     * Pause constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('pauses', true);
    }

    /**
     * @return bool|mixed
     */
    public function getMaxSort()
    {
        $query = ' SELECT MAX(pauses.`sort`) FROM `' . $this->getTableName() . '` as pauses LIMIT 1';
        if (!$this->db->exec($query)) {
            return false;
        }
        return $this->db->getOne();
    }

    /**
     * @param $pauses
     * @return bool|array
     */
    public function sort($pauses)
    {
        $result = true;
        foreach ($pauses as $index => $ID) {
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
}