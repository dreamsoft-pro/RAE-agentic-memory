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
 * Class AdditionalOperation
 * @package DreamSoft\Models\ProductionPath
 */
class AdditionalOperation extends Model
{
    /**
     * AdditionalOperation constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('additional_operation', true);
    }

    public function isCalculated($additionalOperationID){
        $query = 'SELECT calculateTime FROM `' . $this->getTableName() . '` WHERE `ID` = :additionalOperationID';

        $binds['additionalOperationID'] = $additionalOperationID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getOne();
    }

    public function getCalculatedByOngoingID($ongoingID){
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE  `ongoingID` = :ongoingID AND `calculateTime` = 1';

        $binds['ongoingID'] = $ongoingID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();
    }

    /**
     * @param $ongoingID
     * @param $operatorID
     * @return bool
     */
    public function changeOperator($ongoingID, $operatorID)
    {
        $binds = array();
        $query = 'UPDATE `' . $this->getTableName() . '` SET `operatorID` = :operatorID WHERE `ID` = :ongoingID ';
        $binds['operatorID'] = $operatorID;
        $binds['ongoingID'] = $ongoingID;
        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return true;
    }
}