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
class AdditionalOperationLog extends Model
{
    /**
     * AdditionalOperation constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('additionalOperationLogs', true);
    }

    /**
     * @param $additionalOperationID
     * @return array|bool
     */
    public function getByAdditionalOperationID($additionalOperationID)
    {
        $query = 'SELECT `' . $this->getTableName() . '`.* FROM `' . $this->getTableName() . '`'
            . ' WHERE `' . $this->getTableName() . '`.additionalOperationID = :additionalOperationID ';

        $binds['additionalOperationID'] = $additionalOperationID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        $res = $this->db->getAll();
        if (!$res) return false;
        return $res;
    }

    /**
     * @param $additionalOperations
     * @param null $operatorID
     * @return array|bool
     */
    public function getLogsByAdditionalOperations($additionalOperations, $operatorID = NULL)
    {

        if (empty($additionalOperations)) {
            return false;
        }
        $query = ' SELECT * FROM `' . $this->getTableName() . '` WHERE `additionalOperationID` IN (' . implode(',', $additionalOperations) . ') ';

        if( $operatorID !== NULL ) {
            $query .= ' AND `operatorID` = :operatorID ';
            $binds['operatorID'] = $operatorID;
        }

        $query .=  ' ORDER BY `date` ASC ';

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();
        if (!$res) return false;

        $result = array();
        foreach ($res as $key => $val) {
            $result[$val['additionalOperationID']][] = $val;
        }

        return $result;
    }

    public function getLogsByOperatorIDAndDate($operatorID, $dateStart, $dateEnd)
    {
        $query = 'SELECT `dp_additionalOperationLogs`.*, 
        `dp_additional_operation`.`state` as `currentState`, `dp_additional_operation`.`calculateTime`, `dp_additional_operation`.`operationName` as `additionalOperationName`,
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID ,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName
        FROM `dp_additionalOperationLogs` 
        LEFT JOIN `dp_additional_operation` ON  dp_additional_operation.ID = `dp_additionalOperationLogs`.additionalOperationID 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `dp_additional_operation`.ongoingID 
        LEFT JOIN `ps_user_calc_products` ON  `dp_ongoings`.itemID = `ps_user_calc_products`.ID 
        LEFT JOIN `ps_user_calc` ON  `ps_user_calc`.ID = `ps_user_calc_products`.calcID 
        LEFT JOIN `dp_products` ON  `dp_products`.calcID = `ps_user_calc`.ID 
        LEFT JOIN `dp_orders` ON `dp_orders`.ID = dp_products.orderID
        LEFT JOIN `users` as user ON user.ID = `dp_orders`.userID
        WHERE `dp_additionalOperationLogs`.`operatorID` = :operatorID';

        if($dateStart != ""){
            $query .= ' AND `date` >= :dateStart';
            $binds['dateStart'] = $dateStart;
        }

        if($dateEnd != ""){
            $query .= ' AND `date` <= :dateEnd';
            $binds['dateEnd'] = $dateEnd;
        }

        $query .= ' ORDER BY `date` ASC';

        $binds['operatorID'] = $operatorID;
        

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = $this->db->getAll();
        return $result;
    }

    public function getLogsByDate($dateStart, $dateEnd)
    {
        $query = 'SELECT `dp_additionalOperationLogs`.*, 
        `dp_additional_operation`.`state` as `currentState`, `dp_additional_operation`.`calculateTime`, `dp_additional_operation`.`operationName` as `additionalOperationName`, `dp_additional_operation`.`ongoingID` as `ongoingID`,
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID ,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName
        FROM `dp_additionalOperationLogs` 
        LEFT JOIN `dp_additional_operation` ON  dp_additional_operation.ID = `dp_additionalOperationLogs`.additionalOperationID 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `dp_additional_operation`.ongoingID 
        LEFT JOIN `ps_user_calc_products` ON  `dp_ongoings`.itemID = `ps_user_calc_products`.ID 
        LEFT JOIN `ps_user_calc` ON  `ps_user_calc`.ID = `ps_user_calc_products`.calcID 
        LEFT JOIN `dp_products` ON  `dp_products`.calcID = `ps_user_calc`.ID 
        LEFT JOIN `dp_orders` ON `dp_orders`.ID = dp_products.orderID
        LEFT JOIN `users` as user ON user.ID = `dp_orders`.userID
        WHERE';

        if($dateStart != ""){
            $query .= ' `date` >= :dateStart';
            $binds['dateStart'] = $dateStart;
        }

        if($dateEnd != ""){
            $query .= ' AND `date` <= :dateEnd';
            $binds['dateEnd'] = $dateEnd;
        }

        $query .= ' ORDER BY `date` ASC';
        

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = $this->db->getAll();
        return $result;
    }

    public function getLogsByDeviceIDAndDate($deviceID, $dateStart, $dateEnd)
    {
        $query = 'SELECT `dp_additionalOperationLogs`.*, 
        `dp_additional_operation`.`state` as `currentState`, `dp_additional_operation`.`calculateTime`, `dp_additional_operation`.`operationName` as `additionalOperationName`,
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID ,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName
        FROM `dp_additionalOperationLogs` 
        LEFT JOIN `dp_additional_operation` ON  dp_additional_operation.ID = `dp_additionalOperationLogs`.additionalOperationID 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `dp_additional_operation`.ongoingID 
        LEFT JOIN `ps_user_calc_products` ON  `dp_ongoings`.itemID = `ps_user_calc_products`.ID 
        LEFT JOIN `ps_user_calc` ON  `ps_user_calc`.ID = `ps_user_calc_products`.calcID 
        LEFT JOIN `dp_products` ON  `dp_products`.calcID = `ps_user_calc`.ID 
        LEFT JOIN `dp_orders` ON `dp_orders`.ID = dp_products.orderID
        LEFT JOIN `users` as user ON user.ID = `dp_orders`.userID
        WHERE `dp_ongoings`.`deviceID` = :deviceID';

        if($dateStart != ""){
            $query .= ' AND `date` >= :dateStart';
            $binds['dateStart'] = $dateStart;
        }

        if($dateEnd != ""){
            $query .= ' AND `date` <= :dateEnd';
            $binds['dateEnd'] = $dateEnd;
        }

        $query .= ' ORDER BY `date` ASC';

        $binds['deviceID'] = $deviceID;
        

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = $this->db->getAll();
        return $result;
    }

    public function getLogsByOrderIDAndDate($orderID, $dateStart, $dateEnd)
    {
        $query = 'SELECT `dp_additionalOperationLogs`.*, 
        `dp_additional_operation`.`state` as `currentState`, `dp_additional_operation`.`calculateTime`, `dp_additional_operation`.`operationName` as `additionalOperationName`,
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID ,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName
        FROM `dp_additionalOperationLogs` 
        LEFT JOIN `dp_additional_operation` ON  dp_additional_operation.ID = `dp_additionalOperationLogs`.additionalOperationID 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `dp_additional_operation`.ongoingID 
        LEFT JOIN `ps_user_calc_products` ON  `dp_ongoings`.itemID = `ps_user_calc_products`.ID 
        LEFT JOIN `ps_user_calc` ON  `ps_user_calc`.ID = `ps_user_calc_products`.calcID 
        LEFT JOIN `dp_products` ON  `dp_products`.calcID = `ps_user_calc`.ID 
        LEFT JOIN `dp_orders` ON `dp_orders`.ID = dp_products.orderID
        LEFT JOIN `users` as user ON user.ID = `dp_orders`.userID
        WHERE `dp_orders`.`ID` = :orderID';

        if($dateStart != ""){
            //$query .= ' AND `date` >= :dateStart';
            //$binds['dateStart'] = $dateStart;
        }

        if($dateEnd != ""){
            //$query .= ' AND `date` <= :dateEnd';
            //$binds['dateEnd'] = $dateEnd;
        }

        $query .= ' ORDER BY `date` ASC';

        $binds['orderID'] = $orderID;
        

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = $this->db->getAll();
        return $result;
    }

    public function getLogsByDateAndState($dateStart, $dateEnd, $state, $limit = 0, $offset = 0)
    {
        $query = 'SELECT `dp_additionalOperationLogs`.*, 
        `dp_additional_operation`.`state` as `currentState`, `dp_additional_operation`.`calculateTime`, `dp_additional_operation`.`operationName` as `additionalOperationName`,
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`state` as `currentState`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID ,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName,
        `dp_operations`.name as operationName
        FROM `dp_additionalOperationLogs` 
        LEFT JOIN `dp_additional_operation` ON  dp_additional_operation.ID = `dp_additionalOperationLogs`.additionalOperationID 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `dp_additional_operation`.ongoingID 
        LEFT JOIN `ps_user_calc_products` ON  `dp_ongoings`.itemID = `ps_user_calc_products`.ID 
        LEFT JOIN `ps_user_calc` ON  `ps_user_calc`.ID = `ps_user_calc_products`.calcID 
        LEFT JOIN `dp_products` ON  `dp_products`.calcID = `ps_user_calc`.ID 
        LEFT JOIN `dp_orders` ON `dp_orders`.ID = dp_products.orderID
        LEFT JOIN `users` as user ON user.ID = `dp_orders`.userID
        LEFT JOIN `dp_operations` ON dp_operations.ID = `dp_ongoings`.operationID
        WHERE `dp_additionalOperationLogs`.`state` = :state';

        if($dateStart != ""){
            $query .= ' AND `date` >= :dateStart';
            $binds['dateStart'] = $dateStart;
        }

        if($dateEnd != ""){
            $query .= ' AND `date` <= :dateEnd';
            $binds['dateEnd'] = $dateEnd;
        }

        $query .= ' ORDER BY `date` ASC';
        
        $binds['state'] = $state;

        if($limit != 0){
            $query .= ' LIMIT ' . intval($offset) . ',' . intval($limit) . ' ';
        }

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = $this->db->getAll();
        return $result;
    }

    public function getTaskTime($ongoingLogID, $additionalOperationID){
        $query = 'SELECT *
        FROM `' . $this->getTableName() . '` 
        WHERE `ID` <= :ongoingLogID AND `additionalOperationID` = :additionalOperationID';
        $binds['ongoingLogID'] = $ongoingLogID;
        $binds['additionalOperationID'] = $additionalOperationID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $result = $this->db->getAll();

        $lastLog = NULL;
        $diffTimes = array();
        foreach ($result as $key => $row) {
            if (($row['state'] == 2 || $row['state'] == 3) && $lastLog && $lastLog['state'] == 1) {
                $diffTimes[] = $result[$key]['diffTime'] = strtotime($row['date']) - strtotime($lastLog['date']);
            }

            $result[$key]['sumTime'] = array_sum($diffTimes);

            $lastLog = $row;
        }
        
        return array_sum($diffTimes); 
    }
}