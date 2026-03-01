<?php


namespace DreamSoft\Models\ProductionPath;


use DreamSoft\Core\Model;
use DreamSoft\Libs\DataUtils;

class DeviceSideRelations extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('device_speed_change_sides', true);
    }

    public function getOrderedList($deviceID)
    {
        $query = 'select * from dp_device_speed_change_sides where deviceID=:deviceID order by efficiencyChange';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        return $this->db->getAll();
    }
    public function getOrderedListByRelation($deviceID)
    {
        $query = 'select *,sideRelationWidth/sideRelationWidth as relation from dp_device_speed_change_sides where deviceID=:deviceID order by relation';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        return $this->db->getAll();
    }
}
