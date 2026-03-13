<?php
/**
 * Created by PhpStorm.
 * User: Rafał
 * Date: 25-05-2018
 * Time: 10:45
 */

namespace DreamSoft\Models\ProductionPath;

use DateTime;
use DreamSoft\Core\Model;
use DreamSoft\Models\Behaviours\QueryFilter;
use Exception;

class OngoingLog extends Model
{
    /**
     * @var string
     */
    private $ongoings;
    /**
     * @var QueryFilter
     */
    private $QueryFilter;

    public function __construct()
    {
        parent::__construct();
        $this->QueryFilter = new QueryFilter();
        $prefix = true;
        $this->setTableName('ongoingLogs', $prefix);
        $this->ongoings = $this->prefix . 'ongoings';
    }

    /**
     * @param $itemID
     * @return array|bool
     * @throws Exception
     */
    public function getByOrderID($itemID)
    {
        $result = array();

        $query = 'SELECT `' . $this->getTableName() . '`.*,`users`.name, '
            . ' `users`.lastname, `users`.user, `dp_operations`.name as operationName  FROM `' . $this->getTableName() . '` '
            . ' LEFT JOIN `dp_ongoings` ON `dp_ongoings`.ID = `' . $this->getTableName() . '`.ongoingID   '
            . ' LEFT JOIN `dp_operators` ON `dp_operators`.ID = `' . $this->getTableName() . '`.operatorID '
            . ' LEFT JOIN `users` ON `users`.ID = `dp_operators`.uID '
            . ' LEFT JOIN `dp_operations` ON `dp_operations`.ID = `dp_ongoings`.operationID '
            . ' WHERE `dp_ongoings`.`itemID` = :itemID '
            . ' GROUP BY `' . $this->getTableName() . '`.ID'
            . ' ORDER BY `' . $this->getTableName() . '`.date ASC  ';
        $binds['itemID'] = $itemID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();
        if (!$res) return false;

        foreach ($res as $key => $row) {

            $date = new DateTime($row['date']);
            $row['timestamp'] = $date->format('U');
            $result[] = $row;
        }
        return $result;

    }

    /**
     * @param $ongoingID
     * @return array|bool
     */
    public function getByOngoingID($ongoingID)
    {
        $query = 'SELECT `' . $this->getTableName() . '`.* FROM `' . $this->getTableName() . '`'
            . ' WHERE `' . $this->getTableName() . '`.ongoingID = :ongoingID ';

        $binds['ongoingID'] = $ongoingID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        $res = $this->db->getAll();
        if (!$res) return false;
        return $res;
    }

    /**
     * @param $ongoings
     * @param null $operatorID
     * @return array|bool
     */
    public function getLogsByOngoings($ongoings, $operatorID = NULL)
    {

        if (empty($ongoings)) {
            return false;
        }
        $query = ' SELECT * FROM `' . $this->getTableName() . '` WHERE `ongoingID` IN (' . implode(',', $ongoings) . ') ';

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
            $result[$val['ongoingID']][] = $val;
        }

        return $result;
    }

    /**
     * @param $operatorID
     * @return array|bool
     */
    public function isStartedByOperator($ongoingID, $operatorID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `state` = 1 AND `ongoingID` = :ongoingID ORDER BY ID DESC LIMIT 1;';

        $binds[':ongoingID'] = $ongoingID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $row = $this->db->getAll();

        $row[0]['operatorID'] == $operatorID ? $result = true : $result = false;

        return $result;
    }

    /**
     * @param $ongoingID
     * @return array|bool
     */
    public function getFinishedLog($ongoingID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `state` = 3 AND `ongoingID` = :ongoingID ORDER BY ID DESC LIMIT 1;';

        $binds[':ongoingID'] = $ongoingID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $row = $this->db->getAll();

        return $row[0];
    }

    /**
     * @param $ongoingID
     * @return array|bool
     */
    public function getStartLog($ongoingID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `state` = 1 AND `ongoingID` = :ongoingID ORDER BY `date` ASC LIMIT 1;';

        $binds[':ongoingID'] = $ongoingID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        if( $row = $this->db->getAll() ){
            return $row[0];
        }else{
            return false;
        }
    }

    /**
     * @param $ongoingID
     * @return array|bool
     */
    public function getLastLog($ongoingID)
    {
        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `ongoingID` = :ongoingID ORDER BY `date` DESC LIMIT 1;';

        $binds[':ongoingID'] = $ongoingID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        if( $row = $this->db->getAll() ){
            return $row[0];
        }else{
            return false;
        }
    }

    public function getLogsByOperatorIDAndDate($operatorID, $dateStart, $dateEnd)
    {
        $query = 'SELECT `' . $this->getTableName() . '`.*, 
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`state` as `currentState`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID ,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName
        FROM `' . $this->getTableName() . '` 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `' . $this->getTableName() . '`.ongoingID 
        LEFT JOIN `ps_user_calc_products` ON  `dp_ongoings`.itemID = `ps_user_calc_products`.ID 
        LEFT JOIN `ps_user_calc` ON  `ps_user_calc`.ID = `ps_user_calc_products`.calcID 
        LEFT JOIN `dp_products` ON  `dp_products`.calcID = `ps_user_calc`.ID 
        LEFT JOIN `dp_orders` ON `dp_orders`.ID = dp_products.orderID
        LEFT JOIN `users` as user ON user.ID = `dp_orders`.userID
        WHERE `' . $this->getTableName() . '`.`operatorID` = :operatorID';

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
        $query = 'SELECT `' . $this->getTableName() . '`.*, 
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`state` as `currentState`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID ,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName
        FROM `' . $this->getTableName() . '` 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `' . $this->getTableName() . '`.ongoingID 
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

    public function getLogsByDateAndState($dateStart, $dateEnd, $state, $limit = 0, $offset = 0)
    {
        $query = 'SELECT `' . $this->getTableName() . '`.*, 
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`state` as `currentState`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID ,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName,
        `dp_operations`.name as operationName
        FROM `' . $this->getTableName() . '` 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `' . $this->getTableName() . '`.ongoingID 
        LEFT JOIN `ps_user_calc_products` ON  `dp_ongoings`.itemID = `ps_user_calc_products`.ID 
        LEFT JOIN `ps_user_calc` ON  `ps_user_calc`.ID = `ps_user_calc_products`.calcID 
        LEFT JOIN `dp_products` ON  `dp_products`.calcID = `ps_user_calc`.ID 
        LEFT JOIN `dp_orders` ON `dp_orders`.ID = dp_products.orderID
        LEFT JOIN `users` as user ON user.ID = `dp_orders`.userID
        LEFT JOIN `dp_operations` ON dp_operations.ID = `dp_ongoings`.operationID
        WHERE `' . $this->getTableName() . '`.`state` = :state';

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

    public function getLogsByDeviceIDAndDate($deviceID, $dateStart, $dateEnd)
    {
        $query = 'SELECT `' . $this->getTableName() . '`.*, 
        `dp_ongoings`.`estimatedTime`, `dp_ongoings`.`itemID`, `dp_ongoings`.`state` as `currentState`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName 
        FROM `' . $this->getTableName() . '` 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `' . $this->getTableName() . '`.ongoingID 
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
        $query = 'SELECT `' . $this->getTableName() . '`.*, 
        `dp_ongoings`.`itemID`, `dp_ongoings`.`state` as `currentState`, `dp_ongoings`.`deviceID`,
        `ps_user_calc_products`.sheets, 
        `ps_user_calc_products`.projectSheets, `ps_user_calc_products`.numberOfSquareMeters, `ps_user_calc_products`.ID as calcProductID, `ps_user_calc`.realisationDate,
        `ps_user_calc`.amount, `ps_user_calc`.volume, dp_products.ID as productID, dp_orders.ID as orderID, dp_orders.userID,
        `user`.name as userName, `user`.lastname as userLastname, `user`.companyName as userCompanyName
        FROM `' . $this->getTableName() . '` 
        LEFT JOIN `dp_ongoings` ON  dp_ongoings.ID = `' . $this->getTableName() . '`.ongoingID 
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

    public function getTaskTime($ongoingLogID, $ongoingID){
        $query = 'SELECT *
        FROM `' . $this->getTableName() . '` 
        WHERE `ID` <= :ongoingLogID AND `ongoingID` = :ongoingID';
        $binds['ongoingLogID'] = $ongoingLogID;
        $binds['ongoingID'] = $ongoingID;

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