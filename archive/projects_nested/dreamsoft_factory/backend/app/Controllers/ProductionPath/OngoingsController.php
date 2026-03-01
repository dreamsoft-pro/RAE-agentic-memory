<?php
/**
 * Created by PhpStorm.
 * User: Rafał
 * Date: 25-05-2018
 * Time: 12:40
 */


namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Models\Order\OrderConfig;
use DreamSoft\Models\PrintShopUser\UserData;
use DreamSoft\Models\ProductionPath\Ongoing;
use DreamSoft\Models\ProductionPath\OngoingLog;
use DreamSoft\Models\ProductionPath\Operation;
use DreamSoft\Models\ProductionPath\OperationDevice;
use DreamSoft\Models\PrintShopUser\UserAttribute;
use DreamSoft\Models\ProductionPath\PrintTypeDevice;
use DreamSoft\Models\ProductionPath\Operator;
use DreamSoft\Models\ProductionPath\SkillDevice;
use DreamSoft\Models\ProductionPath\OperatorSkill;
use DreamSoft\Models\ProductionPath\OperationOptionController;
use DreamSoft\Models\ProductionPath\Process;
use DreamSoft\Models\ProductionPath\Department;
use DreamSoft\Models\ProductionPath\Device;
use DreamSoft\Models\ProductionPath\OngoingProgress;
use DreamSoft\Models\ProductionPath\Pause;
use DreamSoft\Models\ProductionPath\AdditionalOperation;
use DreamSoft\Models\ProductionPath\AdditionalOperationLog;
use DreamSoft\Controllers\Components\Acl;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Models\PrintShopProduct\PrintShopTypeLanguage;
use DreamSoft\Models\Setting\Setting;

/**
 * Class OngoingsController
 * @package DreamSoft\Controllers\ProductionPath
 */
class OngoingsController extends Controller
{
    public $useModels = array();
    /**
     * @var AdditionalOperation
     */
    private $AdditionalOperation;
    /**
     * @var AdditionalOperationLog
     */
    private $AdditionalOperationLog;
    /**
     * @var Ongoing
     */
    private $Ongoing;
    /**
     * @var OngoingLog
     */
    private $OngoingLog;
    /**
     * @var Operation
     */
    private $Operation;
    /**
     * @var OrderConfig
     */
    private $OrderConfig;
    /**
     * @var OperationDevice
     */
    private $OperationDevice;
    /**
     * @var UserAttribute
     */
    private $UserAttribute;
    /**
     * @var PrintTypeDevice
     */
    private $PrintTypeDevice;
    /**
     * @var UserData
     */
    private $UserData;
    /**
     * @var Operator
     */
    private $Operator;
    /**
     * @var SkillDevice
     */
    private $SkillDevice;
    /**
     * @var OperatorSkill
     */
    private $OperatorSkill;
    /**
     * @var OperationOptionController
     */
    private $OperationOptionController;
    /**
     * @var Process
     */
    private $Process;
    /**
     * @var Department
     */
    private $Department;
    /**
     * @var Device
     */
    private $Device;
    /**
     * @var OngoingProgress
     */
    private $OngoingProgress;
	/**
     * @var Pause
     */
    private $Pause;
    /**
     * @var Acl
     */
    protected $Acl;
    /**
     * @var DpProduct
     */
    protected $DpProduct;
    /**
     * @var PrintShopTypeLanguage
     */
    protected $PrintShopTypeLanguage;
    /**
     * @var Setting
     */
    protected $Setting;

    /**
     * @constructor
     * @param {Array} $params
     */
    public function __construct($params)
    {
        parent::__construct($params);
        $this->Ongoing = Ongoing::getInstance();
        $this->OngoingLog = OngoingLog::getInstance();
        $this->Operation = Operation::getInstance();
        $this->OrderConfig = OrderConfig::getInstance();
        $this->OperationDevice = OperationDevice::getInstance();
        $this->UserAttribute = UserAttribute::getInstance();
        $this->PrintTypeDevice = PrintTypeDevice::getInstance();
        $this->UserData = UserData::getInstance();
        $this->Operator = Operator::getInstance();
        $this->SkillDevice = SkillDevice::getInstance();
        $this->OperatorSkill = OperatorSkill::getInstance();
        $this->Process = Process::getInstance();
        $this->OperationOptionController = OperationOptionController::getInstance();
        $this->Ongoing->setAppVersion(1);
        $this->Department = Department::getInstance();
        $this->Device = Device::getInstance();
        $this->OngoingProgress = OngoingProgress::getInstance();
		$this->Pause = Pause::getInstance();
		$this->AdditionalOperation = AdditionalOperation::getInstance();
		$this->AdditionalOperationLog = AdditionalOperationLog::getInstance();
        $this->Acl = new Acl();
        $this->DpProduct = DpProduct::getInstance();
        $this->PrintShopTypeLanguage = PrintShopTypeLanguage::getInstance();
        $this->Setting = Setting::getInstance();
    }

    /**
     * @param $orderID
     * @param null $ID
     * @return array
     */
    public function index($orderID, $ID = NULL)
    {
        if (intval($ID) > 0) {
            $data = $this->Ongoing->get('ID', $ID);
        } else {
            $data = $this->Ongoing->getAll($orderID);
            if (!empty($data)) {
                foreach ($data as $key => $val) {
                    if (strlen($val['formatWidth']) > 0) {
                        $data[$key]['width'] = $val['formatWidth'];
                    }
                    unset($data[$key]['formatWidth']);
                    if (strlen($val['formatHeight']) > 0) {
                        $data[$key]['height'] = $val['formatHeight'];
                    }
                    unset($data[$key]['formatHeight']);
                    $attrs = $this->UserAttribute->getByOrder($val['orderID']);
                    $data[$key]['attrs'] = $attrs;
                }
            }
        }

        if (empty($data)) {
            $data = array();
        }
        return $data;
    }

    /**
     * @param $orderID
     * @return mixed
     */
    public function post_index($orderID)
    {
        $orderID = $this->Data->getPost('orderID');
        $state = $this->Data->getPost('state');
        if ($state === NULL) {
            $state = 0;
        }
        $operatorID = $this->Data->getPost('operatorID');
        $operationID = $this->Data->getPost('operationID');

        $loggedUser = $this->Auth->getLoggedUser();
        $executiveUserID = $loggedUser['ID'];

        if (!$operatorID) {
            $userInfo = $this->Auth->getLoggedUser();
            $operator = $this->Operator->get('uID', $userInfo['ID']);
            $operatorID = $operator['ID'];
        }
        $return['response'] = false;
        if ($orderID && $operatorID) {
            $lastID = $this->Ongoing->create(compact('orderID', 'operatorID', 'state', 'operationID'));
            if ($lastID) {
                $ongoingID = $this->Ongoing->get('ID', $lastID);
                if ($ongoingID > 0) {
                    $date = date('Y-m-d H:i:s');
                    $this->OngoingLog->create(
                        compact(
                            'date',
                            'ongoingID',
                            'operatorID',
                            'state',
                            'executiveUserID',
                            'operationID')
                    );
                    $return['response'] = true;
                }
            }
        }
        return $return;
    }

    /**
     * @param $ongoingID
     * @return mixed
     */
    public function patch_index($ongoingID)
    {

        $goodFields = array(
            'orderID',
            'operatorID',
            'finished',
            'state',
            'deviceID',
            'processID',
            'sheetNumber',
            'processSideType',
            'pauseID',
            'customPause'
        );
        $post = $this->Data->getAllPost();

        $data['response'] = false;

        $ID = $ongoingID;
        $operatorID = $this->Data->getPost('operatorID');
        $additionalOperators = $this->Data->getPost('additionalOperators');
        $userInfo = $this->Auth->getLoggedUser();

        $executiveUserID = $userInfo['ID'];

        $count = count($post);
        $data['stateChange'] = false;
        if (!empty($post)) {
            $saved = 0;
            $savedLogs = false;
            $item = $this->Ongoing->get('ID', $ID);

            if( !$operatorID && !$item['operatorID'] ) {
                $operatorEntity = $this->Operator->get('uID', $userInfo['ID']);
                if( !$operatorEntity ) {
                    return $this->sendFailResponse('13');
                }
                $operatorID = $operatorEntity['ID'];
            } else if (!$operatorID) {
                $operatorID = $item['operatorID'];
            }

            $userDevices = $this->SkillDevice->getByUserID($userInfo['ID']);

            if (!in_array($item['deviceID'], $userDevices)) {
                $data['info'] = 'operator_does_not_support_this_device';
                return $data;
            }
            $logs = $this->OngoingLog->getByOngoingID($ID);
            foreach ($post as $key => $value) {
                if (in_array($key, $goodFields)) {
                    if ($key == 'state' && $item['state'] == $value) {
                        continue;
                    }
                    if ($key == 'state' && empty($logs) && ($value == 3 || $value == 2)) {
                        continue;
                    }
                    if ($key == 'finished' && empty($logs) && $item['state'] == 0 && $value == 1) {
                        continue;
                    }

                    if( $key == 'finished' && $value == 1 ) {

                        $saved += intval($this->Ongoing->update($ID, 'inProgress', 0));
                        $ongoingEntity = $this->Ongoing->get('ID', $ID);
                        $nextInQueue = $this->Ongoing->getNext($ongoingEntity);

                        if( $nextInQueue ) {
                            $this->Ongoing->update($nextInQueue['ID'], 'inProgress', 1);
                        }

                        $this->Ongoing->update($ID, 'inProgress', 0);
                    }

                    if ($key == 'state' && $item['state'] != $value) {
                        $date = date('Y-m-d H:i:s');
                        $ongoingID = $ID;
                        $state = $value;
                        $ongoingEntity = $this->Ongoing->get('ID', $ID);

                        $currentDevice = $this->Device->get('ID', $ongoingEntity['deviceID']);

                        if( $value == 1 && $currentDevice['multiProcess'] != 1) {
                            $deviceBusy = $this->Ongoing->checkMachineBusy($ongoingEntity['deviceID'], $ongoingEntity['ID']);

                            if($deviceBusy > 0) {
                                $data['info'] = 'device_is_already_busy';
                                $data['response'] = false;
                                return $data;
                            }
                        }

                        $processID = $ongoingEntity['processID'];
                        $operationID = $ongoingEntity['operationID'];
                        $sheetNumber = NULL;
                        if( $post['sheetNumber'] ) {
                            $sheetNumber = $post['sheetNumber'];
                        }
                        $processSideType = NULL;
                        if( $post['processSideType'] ) {
                            $processSideType = $post['processSideType'];
                        }
						$pauseID = NULL;
                        if( $post['pauseID'] ) {
                            $pauseID = $post['pauseID'];
                        }

                        $customPause = NULL;
                        if( $post['customPause'] ) {
                            $customPause = $post['customPause'];
                        }
	
                        $lastLog = $this->OngoingLog->create(
                            compact(
                                'date',
                                'ongoingID',
                                'operatorID',
                                'state',
                                'executiveUserID',
                                'processID',
                                'operationID',
                                'sheetNumber',
                                'processSideType',
                                'pauseID',
                                'customPause'
                            )
                        );
                        if ($lastLog > 0) {
                            $savedLogs = true;
                        }

                        if(!empty($additionalOperators)){
                            $operatorID_ = $operatorID;
                            foreach($additionalOperators as $additionalOperator){
                                if($additionalOperator['ID'] != $operatorID_){
                                    $operatorID = $additionalOperator['ID'];
                                    $asAdditionalOperator = 1;
                                    $lastLog = $this->OngoingLog->create(
                                        compact(
                                            'date',
                                            'ongoingID',
                                            'operatorID',
                                            'state',
                                            'executiveUserID',
                                            'processID',
                                            'operationID',
                                            'sheetNumber',
                                            'processSideType',
                                            'pauseID',
                                            'customPause',
                                            'asAdditionalOperator'
                                        )
                                    );
                                }
                            }
                        }
                        if($state == 3) {
                            $data['finishedPausedProcesses'] = $this->finishPausedProcesses(
                                $ongoingID,
                                $operatorID,
                                $operationID,
                                $executiveUserID
                            );
                        }

                    }
                    $saved += intval($this->Ongoing->update($ID, $key, $value));
                }
            }
            if ($saved > 0) {
                $data['response'] = true;
                $data['info'] = 'saved_message';
                if ($savedLogs) {
                    $data['stateChange'] = true;
                }
            } else {
                $data['info'] = 'error_when_saving_data';
            }
        } else {
            $data['info'] = 'no_data';
        }
        return $data;
    }

    /**
     * @param $ongoingID
     * @param $operatorID
     * @param $operationID
     * @param $executiveUserID
     * @return bool
     */
    private function finishPausedProcesses($ongoingID, $operatorID, $operationID, $executiveUserID)
    {
        $ongoingLogs = $this->OngoingLog->get('ongoingID', $ongoingID, true);

        if( !$ongoingLogs ) {
            return false;
        }

        $finished = array();
        foreach ($ongoingLogs as $ongoingLog) {

            if( $ongoingLog['state'] == 3 ) {
                $finished[$ongoingLog['ongoingID'].'_'.$ongoingLog['processID']] = true;
            }

        }

        $date = date(DATE_FORMAT);

        $savedLogs = 0;

        foreach ($ongoingLogs as $ongoingLog) {

            $searchKey = $ongoingLog['ongoingID'].'_'.$ongoingLog['processID'];

            if( !array_key_exists($searchKey, $finished) ) {

                $state = 3;
                $processID = $ongoingLog['processID'];

                $saveLog = $this->OngoingLog->create(
                    compact(
                        'date',
                        'ongoingID',
                        'operatorID',
                        'state',
                        'executiveUserID',
                        'processID',
                        'operationID'
                    )
                );

                if( $saveLog > 0 ) {
                    $savedLogs++;
                    $finished[$searchKey] = true;
                }

            }

        }

        if( $savedLogs ) {
            return true;
        }

        return false;
    }

    /**
     * @param $orderID
     * @param $ID
     * @return mixed
     */
    public function delete_index($orderID, $ID)
    {
        $data['ID'] = $ID;
        $data['response'] = false;
        if (intval($ID) > 0) {
            if ($this->Ongoing->delete('ID', $ID)) {
                $data['response'] = true;
                return $data;
            }
        }
        return $data;
    }

    /**
     * @param array $params
     * @return array
     */
    public function path($params = array())
    {
        $itemID = $params['orderID'];

        $appVersion = 0;

        $orderConfig = $this->OrderConfig->get('orderID', $itemID);

        if ($orderConfig && $orderConfig['planed'] == 1) {
            return array('response' => false, 'info' => 'Już zaplanowano zadania.');
        }

        $operations = $this->Operation->getByOrderID($itemID);

        $ongoings = array();
        $order = 1;
        foreach ($operations as $o) {
            $operationID = $o['ID'];

            $controllers = $this->OperationOptionController->getSelectedControllers($o['optionID'], $operationID);
            if ($controllers && count($controllers) && $o['controllerID']) {
                if (!in_array($o['controllerID'], $controllers)) {
                    continue;
                }
            }

            $devices = $this->OperationDevice->getDevices($operationID);
            $deviceID = NULL;
            $orderOnDevice = NULL;
            if (!empty($devices)) {
                foreach ($devices as $d) {
                    $userData = $this->UserData->get('orderID', $itemID);
                    $exist = $this->PrintTypeDevice->exist($userData['printTypeID'], $d['deviceID']);
                    if ($exist) {
                        $deviceID = $d['deviceID'];
                        $orderOnDevice = intval($this->Ongoing->getMaxDeviceOrder($deviceID)) + 1;
                        break;
                    }
                }
                if (!$deviceID) {
                    foreach ($devices as $d) {
                        $printTypesList = $this->PrintTypeDevice->getByDeviceID($d['deviceID']);
                        if (empty($printTypesList)) {
                            $deviceID = $d['deviceID'];
                            $orderOnDevice = intval($this->Ongoing->getMaxDeviceOrder($deviceID)) + 1;
                            break;
                        }
                    }
                }
            }

            $lastID = $this->Ongoing->create(compact('itemID', 'operationID', 'order', 'deviceID', 'orderOnDevice', 'appVersion'));
            if ($lastID > 0) {
                $ongoings[] = $this->Ongoing->get('ID', $lastID);
            }
            unset($operationID);
            $order++;
        }
        if (!empty($ongoings)) {
            $planed = 1;
            $this->OrderConfig->create(compact('orderID', 'planed'));
        }

        return $ongoings;
    }

    /**
     * @param $orderID
     * @return mixed
     */
    public function patch_sort($orderID)
    {
        $post = $this->Data->getAllPost();
        return $this->Ongoing->sort($orderID, $post);
    }

    /**
     * @param $deviceID
     * @return array
     */
    public function patch_deviceOrder($deviceID)
    {
        $ogs = $this->Ongoing->getByDeviceID($deviceID);
        $order = intval($this->Ongoing->getMaxDeviceOrder($deviceID), 1);
        $count = 0;
        foreach ($ogs as $o) {
            if (intval($o['orderOnDevice']) < 0) {
                $order++;
                if ($this->Ongoing->update($o['ID'], 'orderOnDevice', $order)) {
                    $count++;
                }
            }
        }
        $response = false;
        if ($count > 0) {
            $response = true;
        }
        return array('response' => $response, 'info' => 'Updated ' . $count . ' wpisów.');
    }

     /**
     * @param $deviceID
     * @return array
     */
    public function patch_ongoingsOrder()
    {
        $post = $this->Data->getAllPost();
        $orderOnDevice = 1;
        foreach ($post as $ongoing) {
            $this->Ongoing->update($ongoing, 'orderOnDevice', $orderOnDevice);
            $orderOnDevice++;
        }
        $response = false;
        if ($orderOnDevice > 1) {
            $response = true;
        }
        return array('response' => $response, 'info' => 'Updated ' . $orderOnDevice . ' rows.');
    }

    /**
     * @param $ongoingID
     * @return array
     */
    public function logs($ongoingID)
    {
        if (!(intval($ongoingID) > 0)) {
            return array('response' => false, 'info' => 'nie ma ongoingID');
        }
        $logs = $this->OngoingLog->get('ongoingID', $ongoingID, true);

        if (!empty($logs)) {

            $aggregateOngoings = array();
            $aggregateOperators = array();
            $aggregateProcesses = array();
            $aggregateOperations = array();
			$aggregatePauses = array();
            foreach ($logs as $log) {
                if( $log['ongoingID'] && is_numeric($log['ongoingID']) ) {
                    $aggregateOngoings[] = $log['ongoingID'];
                }
                if( $log['operatorID'] && is_numeric($log['operatorID']) ) {
                    $aggregateOperators[] = $log['operatorID'];
                }
                if( $log['processID'] && is_numeric($log['processID']) ) {
                    $aggregateProcesses[] = $log['processID'];
                }
                if($log['operationID'] && is_numeric($log['operationID'])) {
                    $aggregateOperations[] = $log['operationID'];
                }
				if($log['pauseID'] && is_numeric($log['pauseID'])) {
                    $aggregatePauses[] = $log['pauseID'];
                }
            }
            $ongoings = $this->Ongoing->getByList($aggregateOngoings);
            $operators = $this->Operator->getByList($aggregateOperators);
            $processes = $this->Process->getByList($aggregateProcesses);
            $operations = $this->Operation->getByList($aggregateOperations);
			$pauses = $this->Pause->getByList($aggregatePauses);

            $additionalOperations = $this->AdditionalOperation->getCalculatedByOngoingID($ongoingID);
            $additionalOperationsLogs = array();
            foreach ($additionalOperations as &$singleOperation) {
                $singleOperation['logs'] = $this->AdditionalOperationLog->getByAdditionalOperationID($singleOperation['ID']);
                foreach ($singleOperation['logs'] as &$singleLog) {
                    $singleLog['operation'] = $singleOperation;
                    if($operators[$singleLog['operatorID']] ) {
                        $singleLog['operator'] = $operators[$singleLog['operatorID']];
                    }
                    $singleLog['isAdditional'] = true;
                    array_push($additionalOperationsLogs, $singleLog);
                }
            }
            $logs = array_merge($logs, $additionalOperationsLogs);

            $lastLog = NULL;
            $diffTimes = array();
            foreach ($logs as $key => $row) {

                if (($row['state'] == 2 || $row['state'] == 3) && $lastLog && $lastLog['state'] == 1) {
                    $diffTimes[] = $logs[$key]['diffTime'] = strtotime($row['date']) - strtotime($lastLog['date']);
                }

                $logs[$key]['sumTime'] = array_sum($diffTimes);

                if( $ongoings[$row['ongoingID']] ) {
                    $logs[$key]['ongoing'] = $ongoings[$row['ongoingID']];
                }
                if( $operators[$row['operatorID']] ) {
                    $logs[$key]['operator'] = $operators[$row['operatorID']];
                }
                if( $processes[$row['processID']] ) {
                    $logs[$key]['process'] = $processes[$row['processID']];
                }
                if( $operations[$row['operationID']] ) {
                    $logs[$key]['operation'] = $operations[$row['operationID']];
                }
				if( $pauses[$row['pauseID']] ) {
                    $logs[$key]['pause'] = $pauses[$row['pauseID']];
                }

                if(!$logs[$key]['isAdditional']) {
                    $logs[$key]['isAdditional'] = false;
                }

                $lastLog = $row;
            }    

        } else {
            $logs = array();
        }
        return $logs;
    }

    /**
     * @param $ongoingID
     * @return array
     */
    public function logsAdditional($ongoingID)
    {
        if (!(intval($ongoingID) > 0)) {
            return array('response' => false, 'info' => 'nie ma ongoingID');
        }
        $logs = $this->AdditionalOperationLog->get('additionalOperationID', $ongoingID, true);
        $additionalOperation = $this->AdditionalOperation->get('ID', $ongoingID, true);

        if (!empty($logs)) {
            $aggregateOperators = array();
			$aggregatePauses = array();
            foreach ($logs as $log) {
                if( $log['operatorID'] && is_numeric($log['operatorID']) ) {
                    $aggregateOperators[] = $log['operatorID'];
                }
				if($log['pauseID'] && is_numeric($log['pauseID'])) {
                    $aggregatePauses[] = $log['pauseID'];
                }
            }
            $operators = $this->Operator->getByList($aggregateOperators);
			$pauses = $this->Pause->getByList($aggregatePauses);

            $lastLog = NULL;
            $diffTimes = array();
            foreach ($logs as $key => $row) {

                if (($row['state'] == 2 || $row['state'] == 3) && $lastLog && $lastLog['state'] == 1) {
                    $diffTimes[] = $logs[$key]['diffTime'] = strtotime($row['date']) - strtotime($lastLog['date']);
                }

                $logs[$key]['sumTime'] = array_sum($diffTimes);
                $logs[$key]['isAdditional'] = true;
                $logs[$key]['operation'] = $additionalOperation[0];
                if( $operators[$row['operatorID']] ) {
                    $logs[$key]['operator'] = $operators[$row['operatorID']];
                }
				if( $pauses[$row['pauseID']] ) {
                    $logs[$key]['pause'] = $pauses[$row['pauseID']];
                }

                $lastLog = $row;
            }    

        } else {
           $logs = array();
        }
        return $logs;
    }

    public function operatorLogs($operatorID)
    {
        if (!$operatorID) {
            return $this->sendFailResponse('02');
        }
        $data = $this->Ongoing->getByOperator($operatorID);
        if (empty($data)) {
            $data = array();
        }
        return $data;
    }

    public function current()
    {

    }

    /**
     * @param $itemID
     * @return array|bool
     */
    public function showForItem($itemID)
    {
        $ongoings = $this->Ongoing->getByItemList(array($itemID));

        if( !$ongoings ) {
            return array();
        }

        $aggregateOngoings = array();
        $aggregateOperations = array();
        $aggregateDevices = array();
        $aggregateOperators = array();

        foreach ($ongoings as $items) {

            foreach ($items as $ongoing) {
                if ($ongoing['ID'] && !in_array($ongoing['ID'], $aggregateOngoings)) {
                    $aggregateOngoings[] = $ongoing['ID'];
                }
                if ($ongoing['operationID'] && !in_array($ongoing['operationID'], $aggregateOperations)) {
                    $aggregateOperations[] = $ongoing['operationID'];
                }
                if ($ongoing['deviceID'] && !in_array($ongoing['deviceID'], $aggregateDevices)) {
                    $aggregateDevices[] = $ongoing['deviceID'];
                }
                if ($ongoing['operatorID'] && !in_array($ongoing['operatorID'], $aggregateOperators)) {
                    $aggregateOperators[] = $ongoing['operatorID'];
                }
            }
        }

        $logs = $this->OngoingLog->getLogsByOngoings($aggregateOngoings);
        $operations = $this->Operation->getByList($aggregateOperations);
        $processes = $this->Process->getByOperationList($aggregateOperations);
        $devices = $this->Device->getByList($aggregateDevices);
        $operators = $this->Operator->getByList($aggregateOperators);

        $aggregateDepartments = array();
        if( $devices ) {
            foreach ($devices as $device) {
                if( $device['departmentID'] && !in_array($device['departmentID'], $aggregateDepartments) ) {
                    $aggregateDepartments[] = $device['departmentID'];
                }
            }
            $departments = $this->Department->getByList($aggregateDepartments);

            foreach ($devices as $key => $device) {
                if( array_key_exists($device['departmentID'], $departments) ) {
                    $devices[$key]['department'] = $departments[$device['departmentID']];
                }
            }
        }

        $flatLogs = array();
        if( $logs ) {
            foreach ($logs as $ongoingID => $ongoingLogs) {
                foreach ($ongoingLogs as $log) {
                    $flatLogs[] = $log;
                }
            }
        }

        foreach ($ongoings as $itemID => $items) {

            foreach ($items as $key => $ongoing) {
                $ongoings[$itemID][$key]['operator'] = NULL;
                if( array_key_exists($ongoing['operatorID'], $operations) ) {
                    $ongoings[$itemID][$key]['operator'] = $operations[$ongoing['operatorID']];
                }
                $ongoings[$itemID][$key]['operation'] = NULL;
                if( array_key_exists($ongoing['operationID'], $operations) ) {
                    $ongoings[$itemID][$key]['operation'] = $operations[$ongoing['operationID']];
                }
                $ongoings[$itemID][$key]['processes'] = NULL;
                if( array_key_exists($ongoing['operationID'], $processes) ) {
                    $ongoings[$itemID][$key]['processes'] = $processes[$ongoing['operationID']];
                }
                $ongoings[$itemID][$key]['devices'] = NULL;
                if( array_key_exists($ongoing['deviceID'], $devices) ) {
                    $ongoings[$itemID][$key]['device'] = $devices[$ongoing['deviceID']];
                }
                $dateShift = strtotime($ongoing['created'].' + 1 hour');
                $ongoings[$itemID][$key]['startDate'] = $ongoing['created'];
                $ongoings[$itemID][$key]['endDate'] = date(DATE_FORMAT, $dateShift);

                if( $ongoings[$itemID][$key]['processes'] === NULL ) {
                    $firstLog = $this->searchLog($flatLogs, $ongoing['ID'], 'ASC');
                    if($firstLog) {
                        $ongoings[$itemID][$key]['startDate'] = $firstLog['date'];
                    }
                    $lastLog = $this->searchLog($flatLogs, $ongoing['ID'], 'DESC');
                    if($lastLog) {
                        $ongoings[$itemID][$key]['endDate'] = $lastLog['date'];
                    }
                } else if ( !empty($ongoings[$itemID][$key]['processes']) ) {
                    $ongoingFirstLog = NULL;
                    $ongoingLastLog = NULL;
                    $notStartedKeys = array();
                    foreach ( $ongoings[$itemID][$key]['processes'] as $processKey => $process ) {

                        $ongoings[$itemID][$key]['processes'][$processKey]['startDate'] = $ongoing['created'];
                        $ongoings[$itemID][$key]['processes'][$processKey]['endDate'] = date(DATE_FORMAT, $dateShift);

                        $firstLog = $this->searchProcessLog($flatLogs, $ongoing['ID'], $process['ID'], 'ASC');
                        if( !$firstLog ) {
                            $ongoings[$itemID][$key]['processes'][$processKey]['ganttGroup'] = 2;
                            $notStartedKeys[] = $processKey;
                            continue;
                        }
                        if( $ongoingFirstLog === NULL || ($ongoingFirstLog['date'] > $firstLog['date'] && $firstLog['date']) ) {
                            $ongoingFirstLog = $firstLog;
                        }
                        if( $firstLog ) {
                            $ongoings[$itemID][$key]['processes'][$processKey]['startDate'] = $firstLog['date'];
                        }
                        $lastLog = $this->searchProcessLog($flatLogs, $ongoing['ID'], $process['ID'], 'DESC');
                        if( $ongoingLastLog === NULL || $ongoingLastLog['date'] < $lastLog['date'] ) {
                            $ongoingLastLog = $lastLog;
                        }
                        if( $lastLog ) {
                            $ongoings[$itemID][$key]['processes'][$processKey]['endDate'] = $lastLog['date'];
                        }
                    }
                    foreach ($notStartedKeys as $notStartedKey) {
                        if( $ongoingFirstLog ) {
                            $ongoings[$itemID][$key]['processes'][$notStartedKey]['startDate'] = $ongoingFirstLog['date'];
                        }
                        if( $ongoingLastLog ) {
                            $ongoings[$itemID][$key]['processes'][$notStartedKey]['endDate'] = $ongoingLastLog['date'];
                        }
                    }
                    $ongoings[$itemID][$key]['processes'] = array_values($ongoings[$itemID][$key]['processes']);
                    if( $ongoingFirstLog ) {
                        $ongoings[$itemID][$key]['startDate'] = $ongoingFirstLog['date'];
                    }
                    if( $ongoingLastLog ) {
                        $ongoings[$itemID][$key]['endDate'] = $ongoingLastLog['date'];
                    }
                }

                $startLog = $this->OngoingLog->getStartLog($ongoings[$itemID][$key]['ID']);
                $endLog = $this->OngoingLog->getLastLog($ongoings[$itemID][$key]['ID']);
                $ongoings[$itemID][$key]['startDate'] = $startLog['date'];
                $ongoings[$itemID][$key]['endDate'] = $endLog['date'];

                $deadline = date("Y-m-d H:i:s",  strtotime($startLog['date'])+$ongoings[$itemID][$key]['estimatedTime']);
                $ongoings[$itemID][$key]['deadline'] = $deadline;
                $ongoings[$itemID][$key]['planned_start'] = $startLog['date'];
                $ongoings[$itemID][$key]['planned_end'] = $deadline;

                $logs = $this->OngoingLog->get('ongoingID', $ongoings[$itemID][$key]['ID'], true);
                $ganttLogs = array();
                if(sizeof($logs) > 0){
                    $lastLog = null;
                    foreach($logs as $logRow){
                        if (($logRow['state'] == 2 || $logRow['state'] == 3) && $lastLog && $lastLog['state'] == 1) {
                            $tmpdata['startDate'] = $lastLog['date'];
                            $tmpdata['endDate'] = $logRow['date'];
                            $tmpdata['sheetNumber'] = $lastLog['sheetNumber'];
                            $tmpdata['processSideType'] = $lastLog['processSideType'];
                            $tmpdata['operatorID'] = $lastLog['operatorID'];
                            $tmpdata['ongoingID'] = $lastLog['ongoingID'];
                            $tmpdata['operationID'] = $lastLog['operationID'];
                            
                            $ganttLogs[] = $tmpdata;
                        }
        
                        $lastLog = $logRow;   
                    }
                }
                $ongoings[$itemID][$key]['logs'] = $ganttLogs;
            }

        }

        reset($ongoings);

        $preparedOngoings = array_values(current($ongoings));

        return array(
            'ongoings' => $preparedOngoings,
            'logs' => $flatLogs,
        );
    }

    /**
     * @return array
     */
    public function patch_progress()
    {
        $post = $this->Data->getAllPost();

        $madeSheets = $post['madeSheets'];
        $madeSheetsReverse = $post['madeSheetsReverse'];
        $ongoingID = $post['ongoingID'];

        if( !$ongoingID ) {
            $this->sendFailResponse('02');
        }
        
        $userInfo = $this->Auth->getLoggedUser();
        $operator = $this->Operator->get('uID', $userInfo['ID']);
        $operatorID = null;
        if( $operator  ) {
            $operatorID = $operator['ID'];
        }

        $saved = 0;

        if( !empty($madeSheets) ) {

            foreach ($madeSheets as $sheetNumber => $sheetsAmount) {

                if( $this->saveSheetProgress(
                    $ongoingID,
                    TYPE_OPERATION_ON_SHEET_OBVERSE,
                    $sheetNumber,
                    $sheetsAmount,
                    $operatorID)
                ) {
                    $saved++;
                }

            }

        }

        if( !empty($madeSheetsReverse) ) {

            foreach ($madeSheetsReverse as $sheetNumber => $sheetsAmount) {

                if( $this->saveSheetProgress(
                    $ongoingID,
                    TYPE_OPERATION_ON_SHEET_REVERSE,
                    $sheetNumber,
                    $sheetsAmount,
                    $operatorID)
                ) {
                    $saved++;
                }

            }

        }

        if( $saved > 0 ) {
            return array(
                'response' => true,
                'saved' => $saved
            );
        }

        return array(
            'response' => false
        );
    }

    private function saveSheetProgress($ongoingID, $type, $sheetNumber, $sheets, $operatorID)
    {
        $created = date(DATE_FORMAT);

        $lastID = $this->OngoingProgress->create(
            compact(
                'ongoingID',
                'type',
                'sheets',
                'sheetNumber',
                'created',
                'operatorID'
            )
        );
        if( $lastID > 0 ) {
            return true;
        }

        return false;
    }

    /**
     * @param $ongoing
     * @return array
     */
    private function setDefaultDates($ongoing)
    {
        $ongoing['startDate'] = $ongoing['created'];
        $ongoing['endDate'] = $ongoing['created'];

        return $ongoing;
    }

    /**
     * @param $logs
     * @param $ongoingID
     * @param string $order
     * @return null
     */
    private function searchLog($logs, $ongoingID, $order = 'ASC')
    {
        if( empty($logs) ) {
            return NULL;
        }

        $lastLog = NULL;

        foreach ($logs as $log) {

            if( $log['ongoingID'] != $ongoingID || $log['processID'] ) {
                continue;
            }

            if( $lastLog === NULL ) {
                $lastLog = $log;
            }

            if( $order === 'ASC' ) {
                if( $log['date'] && $log['date'] < $lastLog['date'] ) {
                    $lastLog = $log;
                }
            } else {
                if( $log['date'] > $lastLog['date'] ) {
                    $lastLog = $log;
                }
            }

        }

        return $lastLog;
    }

    /**
     * @param $logs
     * @param $ongoingID
     * @param $processID
     * @param string $order
     * @return null
     */
    private function searchProcessLog($logs, $ongoingID, $processID, $order = 'ASC')
    {
        if( empty($logs) ) {
            return NULL;
        }

        $lastLog = NULL;

        foreach ($logs as $log) {

            if( $log['ongoingID'] != $ongoingID || $log['processID'] != $processID ) {
                continue;
            }

            if( $lastLog === NULL ) {
                $lastLog = $log;
            }

            if( $order === 'ASC' ) {
                if( $log['date'] && $log['date'] < $lastLog['date'] ) {
                    $lastLog = $log;
                }
            } else {
                if( $log['date'] > $lastLog['date'] ) {
                    $lastLog = $log;
                }
            }

        }

        return $lastLog;
    }
	
	/**
     * @return array
     */
    public function patch_sortProd()
    {
        $post = $this->Data->getAllPost();
        if ($this->Ongoing->sortByDevice($post)) {
            return array('response' => true);
        } else {
            //return $this->sendFailResponse('03');
            return array('response' => false);
        }
    }

    /**
     * @param $itemID
     * @return array
     */
    public function taskWorkplaces($itemID)
    {
        $data = array();
        $taskOngoings = $this->Ongoing->getAll($itemID);
        if(!empty($taskOngoings)){
            foreach($taskOngoings as $ongoing){
                $device = $this->Device->getDevice($ongoing["deviceID"]);
                $ongoing["name"] = $device[0]["name"];
                array_push($data, $ongoing);
            }
        }

        if (empty($data)) {
            $data = array();
        }

        return $data;
    }

    /**
     * @param null
     * @return array
     */
    public function patch_taskWorkplaces()
    {
        $post = $this->Data->getAllPost();
        if ($post) {
            if($this->Ongoing->changeWorkplace($post['ID'], $post['itemID'])){
                return array('response' => true, 'info' => "Zmieniono workplace");
            }else{
                return array('response' => false, 'info' => "Błąd: Unable to change workplace");
            }            
        } else {
            return array('response' => false, 'info' => "Błąd: No workplace data received");
        }
    }

    /**
     * @param $ongoingID
     * @return array
     */
    public function operatorsWithSkills($ongoingID)
    {
        $data = array();
        $ongoing = $this->Ongoing->getById($ongoingID);
        $operators = $this->Operator->getAll();
        //$deviceSkills = $this->SkillDevice->getByDeviceID($deviceID);
        foreach($operators as $operator){
            $operatorSkills = $this->OperatorSkill->getByOperatorID($operator["ID"]);
            foreach($operatorSkills as $skill){
                if($this->SkillDevice->exist($skill["skillID"], $ongoing[0]["deviceID"])){
                    $operator["ongoingID"] = $ongoingID;
                    array_push($data, $operator);
                    break;
                }
            }
        }
        return $data;
    }

     /**
     * @param null
     * @return array
     */
    public function patch_operator()
    {
        $post = $this->Data->getAllPost();
        if ($post) {
            if($this->Ongoing->changeOperator($post['ongoingID'], $post['ID'])){
                return array('response' => true, 'info' => "Zmieniono operatora");
            }else{
                return array('response' => false, 'info' => "Błąd: Unable to operator workplace");
            }            
        } else {
            return array('response' => false, 'info' => "Błąd: No operator data received");
        }
    }

    /**
     * @param null
     * @return array
     */
    public function patch_operatorAdditional()
    {
        $post = $this->Data->getAllPost();
        if ($post) {
            if($this->AdditionalOperation->changeOperator($post['ongoingID'], $post['ID'])){
                return array('response' => true, 'info' => "Zmieniono operatora");
            }else{
                return array('response' => false, 'info' => "Błąd: Unable to change operator");
            }            
        } else {
            return array('response' => false, 'info' => "Błąd: No operator data received");
        }
    }
    

    /**
     * @param $operation
     * @return array
     */
    public function post_additionalOperation()
    {
        $ongoingID = $this->Data->getPost('ongoingID');
        $operationName = $this->Data->getPost('operationName');
        $operationDesc = $this->Data->getPost('operationDesc');
        if(!$operationDesc){
            $operationDesc = "";
        }
        $calculateTime = $this->Data->getPost('calculateTime');
        if(!$calculateTime){
            $calculateTime = 0;
        }
        $data = array();
        $data['response'] = false;

        if ($operationName) {
            $lastID = $this->AdditionalOperation->create(compact('ongoingID', 'operationName', 'operationDesc', 'calculateTime'));
            if ($lastID) {
                $data['response'] = true;
            }
        } else {
            return $this->sendFailResponse('02');
        }

        return $data;
    }

    /**
     * @param $operationID
     * @return array
     */
    public function patch_additionalOperation($operationID)
    {
        $state = $this->Data->getPost('state');
        if ($state) {
            $additionalOperation = $this->AdditionalOperation->get('ID', $operationID);
            $userInfo = $this->Auth->getLoggedUser();
            $operator = $this->Operator->get('uID', $userInfo['ID']);
            if( !$operator  ) {
                return $this->sendFailResponse('13');
            }
            if($additionalOperation['operatorID'] == $operator['ID'] || $this->Acl->isAdmin($loggedUser) || $this->Acl->isSuperUser($loggedUser) || $additionalOperation['operatorID'] == NULL){
                if($this->AdditionalOperation->update($operationID, 'state', $state)){
                        $date = date('Y-m-d H:i:s');
                        $additionalOperationID = $operationID;
                        $operatorID = $operator['ID'];
                        $executiveUserID = $userInfo['ID'];
                        $lastLog = $this->AdditionalOperationLog->create(
                            compact(
                                'date',
                                'additionalOperationID',
                                'operatorID',
                                'state',
                                'executiveUserID'
                                //'pauseID',
                                //'customPause'
                            )
                        );
                        if ($lastLog > 0) {
                            $savedLogs = true;
                        }
                    return array('response' => true, 'info' => "Zaktualizowano");
                }else{
                    return array('response' => false, 'info' => "Unable to change state");
                }  
            }else{
                return array('response' => false, 'info' => "operator_does_not_support_this_operation");
            }          
        } else {
            return array('response' => false, 'info' => "No state data received");
        }
    }

     /**
     * @param $ongoingID
     * @return array
     */
    public function alreadyStartedTasks($ongoingID)
    {
        $ongoing = $this->Ongoing->get('ID', $ongoingID);
        $deviceID = $ongoing['deviceID'];
        $userInfo = $this->Auth->getLoggedUser();
        $operator = $this->Operator->get('uID', $userInfo['ID']);
        if( !$operator  ) {
            return $this->sendFailResponse('13');
        }

        $alreadyStartedOnAnotherDevices = $this->Ongoing->getWithStatusOnAnotherDevicesByOperator($deviceID, $operator['ID'], 1);
        $pausedOnAnotherDevices = $this->Ongoing->getWithStatusOnAnotherDevicesByOperator($deviceID, $operator['ID'], 2);

        $onAnotherDevices = array_merge($alreadyStartedOnAnotherDevices, $pausedOnAnotherDevices);
        
        return $onAnotherDevices;
    }

    /**
     * @param $ongoingID
     * @return array
     */
    public function finishedByOperator($operatorID)
    {
        $finishedByOperator = $this->Ongoing->getFinishedByOperator($operatorID);

        $dates = [];
        $result = [];

        foreach($finishedByOperator as &$row){
            $time = date("Ymd",  strtotime($row['finishedDate']));
            $row['finishedTitleDate'] = date("Y-m-d",  strtotime($row['finishedDate']));
            $result[intval($time)][] = $row;
        } 
        ksort($result);

        /*foreach($finishedByOperator as $row){
            $time = date("Ymd",  strtotime($row['finishedDate']));
            array_push($dates, $time);
        }
        $dates = array_unique($dates);*/ 
        
        return $result;
    }

    public function post_getOperatorLogs($operatorID)
    {
        $dateStart = $this->Data->getPost('dateStart');
        $dateEnd = $this->Data->getPost('dateEnd');
        $dateStart = date("Y-m-d", ($dateStart+86400));
        $dateEnd = date("Y-m-d", $dateEnd+86400);

        if($dateStart == $dateEnd){
            $this->Setting->setModule('productionPath');
            $this->Setting->setDomainID(NULL);
            $this->Setting->setLang(NULL);
            $dayStartTime = $this->Setting->getValue('raportTimeDayStart');
            $dayEndTime = $this->Setting->getValue('raportTimeDayEnd');
            $dateStart = $dateStart." ".$dayStartTime;
            $dateEnd = $dateEnd." ".$dayEndTime;
        }else{
            $dateStart = $dateStart." 00:00:00";
            $dateEnd = $dateEnd." 23:59:59";
        }
        
        $normalLogsByOperatorIDAndDate = $this->OngoingLog->getLogsByOperatorIDAndDate($operatorID, $dateStart, $dateEnd);
        $additionalLogsByOperatorIDAndDate = $this->AdditionalOperationLog->getLogsByOperatorIDAndDate($operatorID, $dateStart, $dateEnd);

        $logsByOperatorIDAndDate = array_merge($normalLogsByOperatorIDAndDate, $additionalLogsByOperatorIDAndDate);
        $ord = array();
        foreach ($logsByOperatorIDAndDate as $key => $value){
            $ord[] = strtotime($value['date']);
        }
        array_multisort($ord, SORT_ASC, $logsByOperatorIDAndDate);

        $dates = [];
        $result = [];

        foreach($logsByOperatorIDAndDate as &$row){
            $time = date("Ymd",  strtotime($row['date']));
            $displayDate = date("Y-m-d",  strtotime($row['date']));

            $row['device'] = $this->Device->get('ID', $row['deviceID']);

            $products = $this->DpProduct->getOrdersProducts(array($row['orderID']));
            foreach($products as &$prod){
                if($prod['productID'] == $row['productID']){
                    $languages = $this->PrintShopTypeLanguage->get('typeID', $prod['typeID'], true);
                    if ($languages) {
                        foreach ($languages as $language) {
                            if (is_array($language) &&
                                array_key_exists('lang', $language) &&
                                array_key_exists('name', $language)) {
                                    $prod['names'][$language['lang']] = $language['name'];
                            }
                        }
                    }
                    $row['product'] = $prod;
                }
            }

            $result[intval($time)]["dateStart"] = $dateStart;
            $result[intval($time)]["dateEnd"] = $dateEnd;
            $result[intval($time)]["title"] = $displayDate;
            $result[intval($time)]["data"][] = $row;            
        } 
        ksort($result);

        foreach($result as $key2 => &$dataArray){
            $lastLog = NULL;
            $lastTime = "";
            $diffTimesWork = array();
            $diffTimesBreak = array();
            $breaksArray = array();
            $finishedTasks = 0;
            $lateFinishedTasks = 0;
            foreach ($dataArray['data'] as $key => &$row) {
                if (($row['state'] == 2 || $row['state'] == 3) && $lastLog && $lastLog['state'] == 1) {
                    $diffTimesWork[] = $row['diffTime'] = strtotime($row['date']) - strtotime($lastLog['date']);
                }

                $sumTime = array_sum($diffTimesWork);
                if($sumTime == $lastTime){
                    $row['timeOfWork'] = "none";
                }else{
                    $row['timeOfWork'] = $row['diffTime'];
                    $lastTime = $sumTime;
                }

                if (($row['state'] == 1) && $lastLog && ($lastLog['state'] == 2 || $lastLog['state'] == 3)) {
                    $timeOfBreak = strtotime($row['date']) - strtotime($lastLog['date']);
                    $diffTimesBreak[] = $row['timeOfBreak'] = $timeOfBreak;
                }else{
                    $row['timeOfBreak'] = "none";
                }
                $row['isBrake'] = false;

                $lastLog = $row;

                if($row['timeOfWork'] == "none" && $row['timeOfBreak'] != "none"){
                    $empty = array();
                    $empty['isBrake'] = true;
                    $empty['timeOfBreak'] = $row['timeOfBreak'];
                    $empty['timeOfWork'] = "none";
                    $empty['device']['name'] = "Przerwa";
                    $emptyDate = strtotime('-1 second', strtotime($row['date']));
                    $empty['date'] = date('Y-m-d H:i:s', $emptyDate);
                    $breaksArray[] = $empty;
                }

                $row['isLateRealisation'] = false;
                if($row['isBrake'] == false){
                    if(isset($row['additionalOperationID'])){
                        $row['taskTime'] = $this->AdditionalOperationLog->getTaskTime($row['ID'], $row['additionalOperationID']);
                    }else{
                        $row['taskTime'] = $this->OngoingLog->getTaskTime($row['ID'], $row['ongoingID']);
                    }
                    if($row['estimatedTime'] != null && $row['estimatedTime'] > 0){
                        $row['plannedTaskTime'] = $row['estimatedTime'];
                    }

                    $realisationDate = strtotime($row['realisationDate']);
                    $finishedDate = strtotime($row['date']);
                    if($finishedDate > $realisationDate){
                        $row['isLateRealisation'] = true;
                    }
                }
                if($row['state'] == 3){
                    $finishedTasks++;
                    if($row['isLateRealisation']){
                        $lateFinishedTasks++;
                    }
                }

                $row['client'] = $row['userCompanyName']." ".$row['userName']." ".$row['userLastname'];
            }
            $dataArray['data'] = array_merge($dataArray['data'], $breaksArray);
            usort($dataArray['data'], function($a, $b) {return strcmp($a['date'], $b['date']);});

            $dataArray['timeOfWork'] = array_sum($diffTimesWork);
            $dataArray['timeOfBreak'] = array_sum($diffTimesBreak);
            $dataArray['workingDay'] = strtotime($dataArray['data'][sizeof($dataArray['data'])-1]['date']) - strtotime($dataArray['data'][0]['date']);
            $dataArray['workingDayStart'] = date("H:i:s",  strtotime($dataArray['data'][0]['date']));
            $dataArray['workingDayEnd'] = date("H:i:s",  strtotime($dataArray['data'][sizeof($dataArray['data'])-1]['date']));
            $dataArray['finishedTasks'] = $finishedTasks;
            $dataArray['lateFinishedTasks'] = $lateFinishedTasks;
        }

        return $result;
    }

    public function post_getAllOperatorLogs()
    {
        $dateStart = $this->Data->getPost('dateStart');
        $dateEnd = $this->Data->getPost('dateEnd');
        $dateStart = date("Y-m-d", ($dateStart+86400));
        $dateEnd = date("Y-m-d", $dateEnd+86400);

        if($dateStart == $dateEnd){
            $this->Setting->setModule('productionPath');
            $this->Setting->setDomainID(NULL);
            $this->Setting->setLang(NULL);
            $dayStartTime = $this->Setting->getValue('raportTimeDayStart');
            $dayEndTime = $this->Setting->getValue('raportTimeDayEnd');
            $dateStart = $dateStart." ".$dayStartTime;
            $dateEnd = $dateEnd." ".$dayEndTime;
        }else{
            $dateStart = $dateStart." 00:00:00";
            $dateEnd = $dateEnd." 23:59:59";
        }
        
        $normalLogsByDate = $this->OngoingLog->getLogsByDate($dateStart, $dateEnd);
        $additionalLogsByDate = $this->AdditionalOperationLog->getLogsByDate($dateStart, $dateEnd);

        $logsByDate = array_merge($normalLogsByDate, $additionalLogsByDate);
        $ord = array();
        foreach ($logsByDate as $key => $value){
            $ord[] = strtotime($value['date']);
        }
        array_multisort($ord, SORT_ASC, $logsByDate);

        $operatorsLogs = [];
        $agregateOperatorLogs = [];
        $result = [];

        foreach($logsByDate as $row){
            if(!isset($operatorsLogs[$row['operatorID']])){
                $operator = $this->Operator->get('ID', $row['operatorID']);
                $operatorsLogs[$row['operatorID']]['operator'] = $operator; 
                $agregateOperatorLogs[$row['operatorID']]['operator'] = $operator;  
            }  
            
            if(!isset($operatorsLogs[$row['operatorID']]['ongoings'][$row['ongoingID']])){
                $ongoing = $this->Ongoing->get('ID', $row['ongoingID']);
                $operatorsLogs[$row['operatorID']]['ongoings'][$row['ongoingID']] = $ongoing;   
            }  
        } 

        foreach($logsByDate as $row){
            $operatorsLogs[$row['operatorID']]['ongoings'][$row['ongoingID']]['logs'][] = $row;
            $agregateOperatorLogs[$row['operatorID']]['logs'][] = $row;
        }

        $operatorsLogs = $this->prepareMainTypeRaport($operatorsLogs);

        //Break time calc
        foreach($agregateOperatorLogs as $singleOperator){
            $breakeTime = 0;
            $lastDate = "";
            $lastLog = null;
            foreach($singleOperator['logs'] as $singleLog){
                $currentDate = explode(' ', $singleLog['date']);
                $currentDate = $currentDate[0];
                if($lastDate != $currentDate){
                    $lastDate = $currentDate;
                }else{
                    if (($singleLog['state'] == 1) && $lastLog && ($lastLog['state'] == 2 || $lastLog['state'] == 3)) {
                        $breakeTime += strtotime($singleLog['date']) - strtotime($lastLog['date']);
                    }
                }
                $lastLog = $singleLog;    
            }
            $operatorsLogs[$singleOperator['operator']['ID']]['data']['totalTasksBreakesTime'] = $breakeTime;
        }
        //Break time calc END

        $result = array();
        foreach($operatorsLogs as $singleLog){
            $result[] = $singleLog;
        }

        return $result;
    }

    public function post_getDeviceLogs($deviceID)
    {
        $dateStart = $this->Data->getPost('dateStart');
        $dateEnd = $this->Data->getPost('dateEnd');
        $dateStart = date("Y-m-d", ($dateStart+86400));
        $dateEnd = date("Y-m-d", $dateEnd+86400);

        if($dateStart == $dateEnd){
            $this->Setting->setModule('productionPath');
            $this->Setting->setDomainID(NULL);
            $this->Setting->setLang(NULL);
            $dayStartTime = $this->Setting->getValue('raportTimeDayStart');
            $dayEndTime = $this->Setting->getValue('raportTimeDayEnd');
            $dateStart = $dateStart." ".$dayStartTime;
            $dateEnd = $dateEnd." ".$dayEndTime;
        }else{
            $dateStart = $dateStart." 00:00:00";
            $dateEnd = $dateEnd." 23:59:59";
        }
        
        $normalLogsByDeviceIDAndDate = $this->OngoingLog->getLogsByDeviceIDAndDate($deviceID, $dateStart, $dateEnd);
        $additionalLogsByDeviceIDAndDate = $this->AdditionalOperationLog->getLogsByDeviceIDAndDate($deviceID, $dateStart, $dateEnd);

        $logsByDeviceIDAndDate = array_merge($normalLogsByDeviceIDAndDate, $additionalLogsByDeviceIDAndDate);
        $ord = array();
        foreach ($logsByDeviceIDAndDate as $key => $value){
            $ord[] = strtotime($value['date']);
        }
        array_multisort($ord, SORT_ASC, $logsByDeviceIDAndDate);

        $dates = [];
        $result = [];

        foreach($logsByDeviceIDAndDate as &$row){
            $time = date("Ymd",  strtotime($row['date']));
            $displayDate = date("Y-m-d",  strtotime($row['date']));

            $row['device'] = $this->Device->get('ID', $row['deviceID']);

            $products = $this->DpProduct->getOrdersProducts(array($row['orderID']));
            foreach($products as &$prod){
                if($prod['productID'] == $row['productID']){
                    $languages = $this->PrintShopTypeLanguage->get('typeID', $prod['typeID'], true);
                    if ($languages) {
                        foreach ($languages as $language) {
                            if (is_array($language) &&
                                array_key_exists('lang', $language) &&
                                array_key_exists('name', $language)) {
                                    $prod['names'][$language['lang']] = $language['name'];
                            }
                        }
                    }
                    $row['product'] = $prod;
                }
            }

            $result[intval($time)]["dateStart"] = $dateStart;
            $result[intval($time)]["dateEnd"] = $dateEnd;
            $result[intval($time)]["title"] = $displayDate;
            $result[intval($time)]["data"][] = $row;
            
        } 
        ksort($result);

        foreach($result as $key2 => &$dataArray){
            $lastLog = NULL;
            $lastTime = "";
            $diffTimesWork = array();
            $diffTimesBreak = array();
            $breaksArray = array();
            $finishedTasks = 0;
            $lateFinishedTasks = 0;
            foreach ($dataArray['data'] as $key => &$row) {
                if (($row['state'] == 2 || $row['state'] == 3) && $lastLog && $lastLog['state'] == 1) {
                    $diffTimesWork[] = $row['diffTime'] = strtotime($row['date']) - strtotime($lastLog['date']);
                }

                $sumTime = array_sum($diffTimesWork);
                if($sumTime == $lastTime){
                    $row['timeOfWork'] = "none";
                }else{
                    $row['timeOfWork'] = $row['diffTime'];
                    $lastTime = $sumTime;
                }

                if (($row['state'] == 1) && $lastLog && ($lastLog['state'] == 2 || $lastLog['state'] == 3)) {
                    $timeOfBreak = strtotime($row['date']) - strtotime($lastLog['date']);
                    $diffTimesBreak[] = $row['timeOfBreak'] = $timeOfBreak;
                }else{
                    $row['timeOfBreak'] = "none";
                }
                $row['isBrake'] = false;

                $lastLog = $row;

                if($row['timeOfWork'] == "none" && $row['timeOfBreak'] != "none"){
                    $empty = array();
                    $empty['isBrake'] = true;
                    $empty['timeOfBreak'] = $row['timeOfBreak'];
                    $empty['timeOfWork'] = "none";
                    $empty['device']['name'] = "Przerwa";
                    $emptyDate = strtotime('-1 second', strtotime($row['date']));
                    $empty['date'] = date('Y-m-d H:i:s', $emptyDate);
                    $breaksArray[] = $empty;
                }

                $operator = $this->Operator->get('ID', $row['operatorID']);
                $row['operator'] = $operator;

                $row['isLateRealisation'] = false;
                if($row['isBrake'] == false){
                    if(isset($row['additionalOperationID'])){
                        $row['taskTime'] = $this->AdditionalOperationLog->getTaskTime($row['ID'], $row['additionalOperationID']);
                    }else{
                        $row['taskTime'] = $this->OngoingLog->getTaskTime($row['ID'], $row['ongoingID']);
                    }
                    if($row['estimatedTime'] != null && $row['estimatedTime'] > 0){
                        $row['plannedTaskTime'] = $row['estimatedTime'];
                    }

                    $realisationDate = strtotime($row['realisationDate']);
                    $finishedDate = strtotime($row['date']);
                    if($finishedDate > $realisationDate){
                        $row['isLateRealisation'] = true;
                    }
                }
                if($row['state'] == 3){
                    $finishedTasks++;
                    if($row['isLateRealisation']){
                        $lateFinishedTasks++;
                    }
                }
                $row['client'] = $row['userCompanyName']." ".$row['userName']." ".$row['userLastname'];
            }
            $dataArray['data'] = array_merge($dataArray['data'], $breaksArray);
            usort($dataArray['data'], function($a, $b) {return strcmp($a['date'], $b['date']);});

            $dataArray['timeOfWork'] = array_sum($diffTimesWork);
            $dataArray['timeOfBreak'] = array_sum($diffTimesBreak);
            $dataArray['workingDay'] = strtotime($dataArray['data'][sizeof($dataArray['data'])-1]['date']) - strtotime($dataArray['data'][0]['date']);
            $dataArray['workingDayStart'] = date("H:i:s",  strtotime($dataArray['data'][0]['date']));
            $dataArray['workingDayEnd'] = date("H:i:s",  strtotime($dataArray['data'][sizeof($dataArray['data'])-1]['date']));
            $dataArray['finishedTasks'] = $finishedTasks;
            $dataArray['lateFinishedTasks'] = $lateFinishedTasks;
        }

        return $result;
    }

    public function post_getAllDeviceLogs()
    {
        $dateStart = $this->Data->getPost('dateStart');
        $dateEnd = $this->Data->getPost('dateEnd');
        $dateStart = date("Y-m-d", ($dateStart+86400));
        $dateEnd = date("Y-m-d", $dateEnd+86400);

        if($dateStart == $dateEnd){
            $this->Setting->setModule('productionPath');
            $this->Setting->setDomainID(NULL);
            $this->Setting->setLang(NULL);
            $dayStartTime = $this->Setting->getValue('raportTimeDayStart');
            $dayEndTime = $this->Setting->getValue('raportTimeDayEnd');
            $dateStart = $dateStart." ".$dayStartTime;
            $dateEnd = $dateEnd." ".$dayEndTime;
        }else{
            $dateStart = $dateStart." 00:00:00";
            $dateEnd = $dateEnd." 23:59:59";
        }
        
        $normalLogsByDate = $this->OngoingLog->getLogsByDate($dateStart, $dateEnd);
        $additionalLogsByDate = $this->AdditionalOperationLog->getLogsByDate($dateStart, $dateEnd);

        $logsByDate = array_merge($normalLogsByDate, $additionalLogsByDate);
        $ord = array();
        foreach ($logsByDate as $key => $value){
            $ord[] = strtotime($value['date']);
        }
        array_multisort($ord, SORT_ASC, $logsByDate);

        $devicesLogs = [];
        $agregateDeviceLogs = [];
        $result = [];

        foreach($logsByDate as $row){
            if(!isset($devicesLogs[$row['deviceID']])){
                $device = $this->Device->get('ID', $row['deviceID']);
                $devicesLogs[$row['deviceID']]['device'] = $device;
                $department = $this->Department->get('ID', $device['departmentID']);
                $devicesLogs[$row['deviceID']]['device']['department'] = $department;
                $agregateDeviceLogs[$row['deviceID']]['device'] = $device;
            }  
            
            if(!isset($devicesLogs[$row['deviceID']]['ongoings'][$row['ongoingID']])){
                $ongoing = $this->Ongoing->get('ID', $row['ongoingID']);
                $devicesLogs[$row['deviceID']]['ongoings'][$row['ongoingID']] = $ongoing;   
            }  
        } 

        foreach($logsByDate as $row){
            $devicesLogs[$row['deviceID']]['ongoings'][$row['ongoingID']]['logs'][] = $row;
            $agregateDeviceLogs[$row['deviceID']]['logs'][] = $row;
        }


        $devicesLogs = $this->prepareMainTypeRaport($devicesLogs);

        //Break time calc
        foreach($agregateDeviceLogs as $singleDevice){
            $breakeTime = 0;
            $lastDate = "";
            $lastLog = null;
            foreach($singleDevice['logs'] as $singleLog){
                $currentDate = explode(' ', $singleLog['date']);
                $currentDate = $currentDate[0];
                if($lastDate != $currentDate){
                    $lastDate = $currentDate;
                }else{
                    if (($singleLog['state'] == 1) && $lastLog && ($lastLog['state'] == 2 || $lastLog['state'] == 3)) {
                        $breakeTime += strtotime($singleLog['date']) - strtotime($lastLog['date']);
                    }
                }
                $lastLog = $singleLog;    
            }
            $devicesLogs[$singleDevice['device']['ID']]['data']['totalTasksBreakesTime'] = $breakeTime;
        }
        //Break time calc END

        $result = array();
        foreach($devicesLogs as $singleLog){
            $result[] = $singleLog;
        }

        return $result;
    }

    public function post_getOrderLogs($orderID)
    {
        $dateStart = $this->Data->getPost('dateStart');
        $dateEnd = $this->Data->getPost('dateEnd');
        $dateStart = date("Y-m-d 00:00:00", ($dateStart+86400));
        $dateEnd = date("Y-m-d 23:59:59", $dateEnd+86400);
        
        $normalLogsByOrderIDAndDate = $this->OngoingLog->getLogsByOrderIDAndDate($orderID, $dateStart, $dateEnd);
        $additionalLogsByOrderIDAndDate = $this->AdditionalOperationLog->getLogsByOrderIDAndDate($orderID, $dateStart, $dateEnd);

        $logsByOrderIDAndDate = array_merge($normalLogsByOrderIDAndDate, $additionalLogsByOrderIDAndDate);
        $ord = array();
        foreach ($logsByOrderIDAndDate as $key => $value){
            $ord[] = strtotime($value['date']);
        }
        array_multisort($ord, SORT_ASC, $logsByOrderIDAndDate);

        $dates = [];
        $result = [];

        foreach($logsByOrderIDAndDate as &$row){
            $time = date("Ymd",  strtotime($row['date']));
            $displayDate = date("Y-m-d",  strtotime($row['date']));

            $row['device'] = $this->Device->get('ID', $row['deviceID']);

            $products = $this->DpProduct->getOrdersProducts(array($row['orderID']));
            foreach($products as &$prod){
                if($prod['productID'] == $row['productID']){
                    $languages = $this->PrintShopTypeLanguage->get('typeID', $prod['typeID'], true);
                    if ($languages) {
                        foreach ($languages as $language) {
                            if (is_array($language) &&
                                array_key_exists('lang', $language) &&
                                array_key_exists('name', $language)) {
                                    $prod['names'][$language['lang']] = $language['name'];
                            }
                        }
                    }
                    $row['product'] = $prod;
                }
            }

            $result[intval($time)]["dateStart"] = $dateStart;
            $result[intval($time)]["dateEnd"] = $dateEnd;
            $result[intval($time)]["title"] = $displayDate;
            $result[intval($time)]["data"][] = $row;
            
        } 
        ksort($result);

        foreach($result as $key2 => &$dataArray){
            $lastLog = NULL;
            $lastTime = "";
            $diffTimesWork = array();
            $diffTimesBreak = array();
            $breaksArray = array();
            foreach ($dataArray['data'] as $key => &$row) {
                if (($row['state'] == 2 || $row['state'] == 3) && $lastLog && $lastLog['state'] == 1) {
                    $diffTimesWork[] = $row['diffTime'] = strtotime($row['date']) - strtotime($lastLog['date']);
                }

                $sumTime = array_sum($diffTimesWork);
                if($sumTime == $lastTime){
                    $row['timeOfWork'] = "none";
                }else{
                    $row['timeOfWork'] = $row['diffTime'];
                    $lastTime = $sumTime;
                }

                if (($row['state'] == 1) && $lastLog && ($lastLog['state'] == 2 || $lastLog['state'] == 3)) {
                    $timeOfBreak = strtotime($row['date']) - strtotime($lastLog['date']);
                    $diffTimesBreak[] = $row['timeOfBreak'] = $timeOfBreak;
                }else{
                    $row['timeOfBreak'] = "none";
                }
                $row['isBrake'] = false;

                $lastLog = $row;

                if($row['timeOfWork'] == "none" && $row['timeOfBreak'] != "none"){
                    $empty = array();
                    $empty['isBrake'] = true;
                    $empty['timeOfBreak'] = $row['timeOfBreak'];
                    $empty['timeOfWork'] = "none";
                    $empty['device']['name'] = "Przerwa";
                    $emptyDate = strtotime('-1 second', strtotime($row['date']));
                    $empty['date'] = date('Y-m-d H:i:s', $emptyDate);
                    $breaksArray[] = $empty;
                }

                $operator = $this->Operator->get('ID', $row['operatorID']);
                $row['operator'] = $operator;
                $row['client'] = $row['userCompanyName']." ".$row['userName']." ".$row['userLastname'];
            }
            $dataArray['data'] = array_merge($dataArray['data'], $breaksArray);
            usort($dataArray['data'], function($a, $b) {return strcmp($a['date'], $b['date']);});

            $dataArray['timeOfWork'] = array_sum($diffTimesWork);
            $dataArray['timeOfBreak'] = array_sum($diffTimesBreak);
            $dataArray['workingDay'] = strtotime($dataArray['data'][sizeof($dataArray['data'])-1]['date']) - strtotime($dataArray['data'][0]['date']);
            $dataArray['workingDayStart'] = date("H:i:s",  strtotime($dataArray['data'][0]['date']));
            $dataArray['workingDayEnd'] = date("H:i:s",  strtotime($dataArray['data'][sizeof($dataArray['data'])-1]['date']));
        }

        return $result;
    }

    /*public function post_getAllOrderLogs()
    {
        $dateStart = $this->Data->getPost('dateStart');
        $dateEnd = $this->Data->getPost('dateEnd');
        $dateStart = date("Y-m-d", ($dateStart+86400));
        $dateEnd = date("Y-m-d", $dateEnd+86400);

        if($dateStart == $dateEnd){
            $this->Setting->setModule('productionPath');
            $this->Setting->setDomainID(NULL);
            $this->Setting->setLang(NULL);
            $dayStartTime = $this->Setting->getValue('raportTimeDayStart');
            $dayEndTime = $this->Setting->getValue('raportTimeDayEnd');
            $dateStart = $dateStart." ".$dayStartTime;
            $dateEnd = $dateEnd." ".$dayEndTime;
        }else{
            $dateStart = $dateStart." 00:00:00";
            $dateEnd = $dateEnd." 23:59:59";
        }
        
        $logsByDate = $this->OngoingLog->getLogsByDate($dateStart, $dateEnd);

        $ordersLogs = [];
        $result = [];

        foreach($logsByDate as $row){
            if($ordersLogs[$row['orderID']] == null){
                $device = $this->Device->get('ID', $row['orderID']);
                $ordersLogs[$row['orderID']]['device'] = $device;
            }  
            
            if($ordersLogs[$row['orderID']]['ongoings'][$row['ongoingID']] == null){
                $ongoing = $this->Ongoing->get('ID', $row['ongoingID']);
                $ordersLogs[$row['orderID']]['ongoings'][$row['ongoingID']] = $ongoing;   
                $this->debug('ongoing', $ongoing);
            }  
        } 

        foreach($logsByDate as $row){
            $ordersLogs[$row['orderID']]['ongoings'][$row['ongoingID']]['logs'][] = $row;
        }


        $ordersLogs = $this->prepareMainTypeRaport($ordersLogs);

        $result = array();
        foreach($ordersLogs as $singleLog){
            $result[] = $singleLog;
        }

        return $result;
    }*/

    public function getOperationsLogsCount($params)
    {
        $dateStart = $params['dateStart'];
        $dateEnd = $params['dateEnd'];
        $dateStart = date("Y-m-d", ($dateStart+86400));
        $dateEnd = date("Y-m-d", $dateEnd+86400);

        if($dateStart == $dateEnd){
            $this->Setting->setModule('productionPath');
            $this->Setting->setDomainID(NULL);
            $this->Setting->setLang(NULL);
            $dayStartTime = $this->Setting->getValue('raportTimeDayStart');
            $dayEndTime = $this->Setting->getValue('raportTimeDayEnd');
            $dateStart = $dateStart." ".$dayStartTime;
            $dateEnd = $dateEnd." ".$dayEndTime;
        }else{
            $dateStart = $dateStart." 00:00:00";
            $dateEnd = $dateEnd." 23:59:59";
        }

        $normalLogsByDate = $this->OngoingLog->getLogsByDateAndState($dateStart, $dateEnd, 3);
        $additionalLogsByDate = $this->AdditionalOperationLog->getLogsByDateAndState($dateStart, $dateEnd, 3);

        $logsByDate = array_merge($normalLogsByDate, $additionalLogsByDate);
        /*$ord = array();
        foreach ($logsByOrderIDAndDate as $key => $value){
            $ord[] = strtotime($value['date']);
        }
        array_multisort($ord, SORT_ASC, $logsByOrderIDAndDate);*/

        return array('count' => sizeof($logsByDate));
    }

    public function getOperationsLogs($params)
    {
        $dateStart = $params['dateStart'];
        $dateEnd = $params['dateEnd'];
        $dateStart = date("Y-m-d", ($dateStart+86400));
        $dateEnd = date("Y-m-d", $dateEnd+86400);

        if($dateStart == $dateEnd){
            $this->Setting->setModule('productionPath');
            $this->Setting->setDomainID(NULL);
            $this->Setting->setLang(NULL);
            $dayStartTime = $this->Setting->getValue('raportTimeDayStart');
            $dayEndTime = $this->Setting->getValue('raportTimeDayEnd');
            $dateStart = $dateStart." ".$dayStartTime;
            $dateEnd = $dateEnd." ".$dayEndTime;
        }else{
            $dateStart = $dateStart." 00:00:00";
            $dateEnd = $dateEnd." 23:59:59";
        }

        $limit = 30;
        if (isset($params['limit'])) {
            $limit = $params['limit'];
        }
        $offset = 0;
        if (isset($params['offset'])) {
            $offset = $params['offset'];
        }
        
        $normalLogsByDate = $this->OngoingLog->getLogsByDateAndState($dateStart, $dateEnd, 3);
        $additionalLogsByDate = $this->AdditionalOperationLog->getLogsByDateAndState($dateStart, $dateEnd, 3);

        $logsByDate = array_merge($normalLogsByDate, $additionalLogsByDate);
        $ord = array();
        foreach ($logsByDate as $key => $value){
            $ord[] = strtotime($value['date']);
        }
        array_multisort($ord, SORT_ASC, $logsByDate);

        foreach($logsByDate as &$row){
            $operator = $this->Operator->get('ID', $row['operatorID']);
            $row['operator'] = $operator;   
            if(isset($row['additionalOperationID'])){
                $row['taskTime'] = $this->AdditionalOperationLog->getTaskTime($row['ID'], $row['additionalOperationID']);
            }else{
                $row['taskTime'] = $this->OngoingLog->getTaskTime($row['ID'], $row['ongoingID']);
            }
            $row['device'] = $this->Device->get('ID', $row['deviceID']);

            $row['isLateRealisation'] = false;
            $realisationDate = strtotime($row['realisationDate']);
            $finishedDate = strtotime($row['date']);
            if($finishedDate > $realisationDate){
                $row['isLateRealisation'] = true;
            }

            $row['timeDifference'] = $row['estimatedTime'] - $row['taskTime'];
            $row['taskOverdue'] = false;
            if($row['timeDifference'] < 0){
                $row['timeDifference'] = $row['timeDifference'] * -1;
                $row['taskOverdue'] = true;
            }

            $products = $this->DpProduct->getOrdersProducts(array($row['orderID']));
            foreach($products as &$prod){
                if($prod['productID'] == $row['productID']){
                    $languages = $this->PrintShopTypeLanguage->get('typeID', $prod['typeID'], true);
                    if ($languages) {
                        foreach ($languages as $language) {
                            if (is_array($language) &&
                                array_key_exists('lang', $language) &&
                                array_key_exists('name', $language)) {
                                    $prod['names'][$language['lang']] = $language['name'];
                            }
                        }
                    }
                    $row['product'] = $prod;
                }
            }

            $row['efficency'] = round($row['product']['volume'] / $row['taskTime']);
        }
        

        return $logsByDate;
    }

    public function ongoingsForCalcProduct($calcProductID)
    {
        $ongoingsForCalcProduct = $this->Ongoing->get('itemID', $calcProductID, true); 

        foreach($ongoingsForCalcProduct as &$row){
            $lastOngoingLog = $this->OngoingLog->getLastLog($row['ID']);
            $row['realTime'] = $this->OngoingLog->getTaskTime($lastOngoingLog['ID'], $row['ID']);
        }
        
        return $ongoingsForCalcProduct;
    }

    public function productionSettings()
    {
        $this->Setting->setModule('productionPath');
        $this->Setting->setDomainID(NULL);
        $this->Setting->setLang(NULL);
        $result = array();
        $result['raportTimeDayStart'] = $this->Setting->getValue('raportTimeDayStart');
        $result['raportTimeDayEnd'] = $this->Setting->getValue('raportTimeDayEnd');
        $result['defaultGanttScale'] = $this->Setting->getValue('defaultGanttScale');

        return $result;
    }

    public function put_productionSettings()
    {
        $post = $this->Data->getAllPost();
        $saved = true;
        $this->Setting->setModule('productionPath');
        $this->Setting->setDomainID(NULL);
        $this->Setting->setLang(NULL);
        foreach($post as $key => $value){
            if(!$this->Setting->set($key, $value)){
                $saved = false;
            }
        }
        
        if($saved == true){
            $response = ['response' => 'true'];
        }else{
            $response['error'] = 'Error saving settings';
        }
        return $response;
    }

    private function prepareMainTypeRaport($array){
        $arrayReturn = $array;
        foreach($arrayReturn as &$row){
            $row['data']['lateOngoings'] = 0;
            $row['data']['overdueOngoings'] = 0;
            $row['data']['ongoings'] = 0;
            $row['data']['totalPlannedTimes'] = 0;
            $row['data']['totalRealTimes'] = 0;
            $row['data']['totalTasksBreakesTime'] = 0;
            foreach($row['ongoings'] as &$ongoing){
                $row['data']['ongoings']++;
                $ongoing['isLate'] = false;
                $ongoing['isOverdue'] = false;
                foreach($ongoing['logs'] as &$log){
                    $ongoing['realTime'] = $this->OngoingLog->getTaskTime($log['ID'], $log['ongoingID']);
                    if($ongoing['realTime'] > $ongoing['estimatedTime']){
                        $ongoing['isOverdue'] = true;
                    }
                    $realisationDate = strtotime($log['realisationDate']);
                    $finishedDate = strtotime($log['date']);
                    if($finishedDate > $realisationDate){
                        $ongoing['isLate'] = true;
                    }
                }
                if($ongoing['isLate'] == true){
                    $row['data']['lateOngoings']++;
                }
                if($ongoing['isOverdue'] == true){
                    $row['data']['overdueOngoings']++;
                }
                $row['data']['totalPlannedTimes'] += $ongoing['estimatedTime'];
                $row['data']['totalRealTimes'] += $ongoing['realTime'];
            }
        }
        return $arrayReturn;
    }
}
