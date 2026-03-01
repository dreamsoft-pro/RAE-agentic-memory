<?php

namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

class OptionControllerOperationDevice extends Model
{
    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('optionControllerOperationDevice', $prefix);
    }

    public function getByOptionController($optID, $controllerID)
    {
        $query = 'select dp_optionControllerOperationDevice.*
                    from dp_optionControllerOperationDevice 
                    where optID=:optID and controllerID=:controllerID';
        $this->db->exec($query, [':optID' => $optID, ':controllerID' => $controllerID]);
        return $this->db->getAll();
    }

    public function updateOptionControllerOperation($optID, $controllerID, $operations)
    {
        $query = 'delete from dp_optionControllerOperationDevice 
                    where optID=:optID and controllerID=:controllerID';
        $this->db->exec($query, [':optID' => $optID, ':controllerID' => $controllerID]);
        foreach ($operations as $operation) {
            foreach ($operation['devices'] as $device) {
                $query = 'insert into dp_optionControllerOperationDevice(optID,operationID,controllerID,deviceID)
            values(:optID,:operationID,:controllerID,:deviceID);';
                if(!$this->db->exec($query, [':optID' => $optID,
                    ':controllerID' => $controllerID,
                    ':operationID' => $operation['operationID'],
                    ':deviceID' => $device['ID']
                ])){
                    return false;
                };
            }
        }
        return true;
    }
    public function getPairs($options, $operations)
    {
        if( !$options || !$operations ) {
            return false;
        }
        $query = 'SELECT * FROM `dp_optionControllerOperationDevice` 
            WHERE `optID` IN ('.implode(',', $options).') AND `operationID` IN ('.implode(',', $operations).') ';

        if (!$this->db->exec($query)) {
            return false;
        }
        return $this->db->getAll();
    }
}
