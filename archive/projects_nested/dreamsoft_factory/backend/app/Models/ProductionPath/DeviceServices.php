<?php


namespace DreamSoft\Models\ProductionPath;


use DreamSoft\Core\Model;
use DreamSoft\Libs\DataUtils;

class DeviceServices extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('device_services', true);
    }

    public function getListByID($deviceID)
    {
        $query = 'select * from dp_device_services where deviceID=:deviceID order by ID';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        return $this->db->getAll();
    }

}
