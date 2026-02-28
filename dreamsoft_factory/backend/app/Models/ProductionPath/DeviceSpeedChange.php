<?php


namespace DreamSoft\Models\ProductionPath;


use DreamSoft\Core\Model;

class DeviceSpeedChange extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('device_speed_changes', true);
    }

    public function getOrderedList($deviceID)
    {
        $query = 'select * from dp_device_speed_changes where deviceID=:deviceID order by efficiencyChange';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        return $this->db->getAll();
    }

}
