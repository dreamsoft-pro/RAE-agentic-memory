<?php
/**
 * Created by PhpStorm.
 * User: Rafał
 * Date: 25-05-2018
 * Time: 10:16
 */

namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

/**
 * Class Device
 * @package DreamSoft\Models\ProductionPath
 */
class Device extends Model
{
    /**
     * Device constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('devices', true);
    }

    /**
     * @param $operatorID
     * @return array|bool
     */
    public function countAll($operatorID = NULL)
    {
        $query = 'SELECT `dp_devices`.ID, COUNT(`dp_ongoings`.ID) as countTasks
                FROM `dp_devices`
                         JOIN `dp_ongoings` ON `dp_ongoings`.deviceID = `dp_devices`.ID
                         JOIN (SELECT DISTINCT deviceID FROM
                    dp_skillDevices sd
                        JOIN dp_operatorSkills os on os.skillID = sd.skillID
                               WHERE os.operatorID=:operatorID) sdj
                              ON sdj.deviceID = dp_ongoings.deviceID
                WHERE `dp_ongoings`.finished = 0
                  AND `dp_ongoings`.inProgress = 1
                group by `dp_devices`.ID';

        $binds = array();
        $binds['operatorID'] = $operatorID;


        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();
        if (!$res) return false;

        $result = array();

        foreach ($res as $row) {
            $result[] = $row;
        }
        return $result;
    }
	
	/**
     * @param $operatorID
     * @return array|bool
     */
    public function countAllPlanned($operatorID = NULL)
    {
        $query = 'SELECT `dp_devices`.ID, COUNT(`dp_ongoings`.ID) as countTasks
                FROM `dp_devices`
                         JOIN `dp_ongoings` ON `dp_ongoings`.deviceID = `dp_devices`.ID
                         JOIN (SELECT DISTINCT deviceID FROM
                    dp_skillDevices sd
                        JOIN dp_operatorSkills os on os.skillID = sd.skillID
                               WHERE os.operatorID=:operatorID) sdj
                              ON sdj.deviceID = dp_ongoings.deviceID
                WHERE `dp_ongoings`.finished = 0
                group by `dp_devices`.ID';

        $binds = array();
        $binds['operatorID'] = $operatorID;


        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();
        if (!$res) return false;

        $result = array();

        foreach ($res as $row) {
            $result[] = $row;
        }
        return $result;
    }

    /**
     * @param null $devices
     * @return array|bool
     */
    public function getAll($devices = NULL)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` ';

        if (is_array($devices) && !empty($devices)) {
            $query .= ' WHERE `ID` IN (' . implode(',', $devices) . ') ';
        }

        $binds = array();
        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        $res = $this->db->getAll();
        if (!$res) return false;

        foreach ($res as $row) {
            $result[] = $row;
        }
        return $result;
    }

    /**
     * @param null $devices
     * @return array|bool
     */
    public function getDevice($deviceID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '`  WHERE `ID` = ' . $deviceID . ';';

        $binds = array();
        $this->db->exec($query, $binds);

        return $this->db->getAll();
    }

    /**
     * @return bool|mixed
     */
    public function getMaxSort()
    {
        $query = ' SELECT MAX(devices.`sort`) FROM `' . $this->getTableName() . '` as devices LIMIT 1';
        if (!$this->db->exec($query)) {
            return false;
        }
        return $this->db->getOne();
    }

    /**
     * @param $devices
     * @return bool|array
     */
    public function sort($devices)
    {
        $result = true;
        foreach ($devices as $index => $ID) {
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
