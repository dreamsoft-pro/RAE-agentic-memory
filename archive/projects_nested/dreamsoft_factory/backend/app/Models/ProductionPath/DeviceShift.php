<?php
namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

/**
 * Class Shift
 * @package DreamSoft\Models\ProductionPath
 */
class DeviceShift extends Model
{
    /**
     * Shift constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('device_shift', true);
    }

    /**
     * @return bool|mixed
     */
    public function getMaxSort()
    {
        $query = ' SELECT MAX(device_shift.`sort`) FROM `' . $this->getTableName() . '` as device_shift LIMIT 1';
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

    public function getDayFinishHour($deviceID){
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `deviceID` = :deviceID ORDER BY stop DESC LIMIT 1';
        $binds['deviceID'] = $deviceID;
        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->getRow();
    }

    public function getDayStartHour($deviceID){
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `deviceID` = :deviceID ORDER BY start ASC LIMIT 1';
        $binds['deviceID'] = $deviceID;
        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->getRow();
    }

    public function getByDeviceIDSorted($deviceID){
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `deviceID` = :deviceID ORDER BY sort';
        $binds['deviceID'] = $deviceID;
        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->getAll();
    }
}