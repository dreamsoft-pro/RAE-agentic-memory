<?php


namespace DreamSoft\Models\ProductionPath;


use DreamSoft\Core\Model;
use DreamSoft\Libs\DataUtils;

class DevicePrice extends Model
{
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('device_prices', true);
    }

    public function getListByRange($deviceID)
    {
        $query = 'select * from dp_device_prices where deviceID=:deviceID order by amount';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        return $this->db->getAll();
    }
    public function getPriceForAmount($deviceID, $amount){
        $query = 'select amount as `volume`,unitPrice as `value` from dp_device_prices where deviceID=:deviceID
                    order by `volume`;';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        $prices=$this->db->getAll();
        return DataUtils::linearApproximation($prices,$amount);
    }
    public function getExpenseForAmount($deviceID, $amount){
        $query = 'select amount as `volume`,unitCost as `value` from dp_device_prices where deviceID=:deviceID
                    order by `volume`;';
        $this->db->exec($query, [':deviceID' => $deviceID]);
        $prices=$this->db->getAll();
        return DataUtils::linearApproximation($prices,$amount);
    }
}
