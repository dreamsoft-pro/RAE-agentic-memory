<?php


namespace DreamSoft\Models\ProductionPath;


use DreamSoft\Core\Model;
use DreamSoft\Libs\DataUtils;

class DeviceSpeed extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('device_speeds', true);
    }

    public function getListByDevice($deviceID)
    {
        $query = 'select * from dp_device_speeds where deviceID=:deviceID order by volume';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        return $this->db->getAll();
    }

    public function getSpeedForVolume($deviceID, $volume){
        $query = 'select volume, speed as `value` from dp_device_speeds where deviceID=:deviceID
                    order by volume;';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        $speeds=$this->db->getAll();
        return DataUtils::linearApproximation($speeds,$volume);
    }
}
