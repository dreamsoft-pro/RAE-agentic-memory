<?php
namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Controllers\Components\Standard;

use DreamSoft\Controllers\Components\Filter;
use DreamSoft\Models\Address\Address;
use DreamSoft\Models\Order\DpProduct;
use DreamSoft\Models\Order\DpProductFile;
use DreamSoft\Models\PrintShopProduct\PrintShopType;
use DreamSoft\Models\PrintShopUser\UserCalc;
use DreamSoft\Models\PrintShopUser\UserCalcProductAttribute;
use DreamSoft\Models\PrintShopUser\UserCalcProductSpecialAttribute;
use DreamSoft\Models\PrintShopUser\UserCalcProduct;
use DreamSoft\Controllers\Components\ProductionPath;
use DreamSoft\Models\ProductionPath\Ongoing;
use DreamSoft\Models\ProductionPath\OngoingLog;
use DreamSoft\Models\ProductionPath\Department;
use DreamSoft\Models\ProductionPath\Device;
use DreamSoft\Models\ProductionPath\Operation;
use DreamSoft\Models\ProductionPath\OperationDevice;
use DreamSoft\Models\ProductionPath\Shift;
use DreamSoft\Models\ProductionPath\DeviceServices;
use DreamSoft\Models\Setting\Setting;
use DreamSoft\Models\ProductionPath\DeviceShift;
use DreamSoft\Models\RealizationTime\Holiday;
use DreamSoft\Controllers\Components\DateComponent;

class PlanningController extends Controller
{
    /**
     * @var Filter
     */
    protected $Filter;
     /**
     * @var Address
     */
    protected $Address;
    /**
     * @var DpProduct
     */
    protected $DpProduct;
    /**
     * @var DpProductFile
     */
    protected $DpProductFile;
    /**
     * @var PrintShopType
     */
    protected $PrintShopType;
    /**
     * @var UserCalc
     */
    protected $UserCalc;
    /**
     * @var UserCalcProduct
     */
    protected $UserCalcProduct;
    /**
     * @var UserCalcProductAttribute
     */
    protected $UserCalcProductAttribute;
    /**
     * @var UserCalcProductSpecialAttribute
     */
    protected $UserCalcProductSpecialAttribute;
    /**
     * @var ProductionPath
     */
    private $ProductionPath;
    /**
     * @var Ongoing
     */
    private $Ongoing;
    /**
     * @var OngoingLog
     */
    private $OngoingLog;
    /**
     * @var Department
     */
    private $Department;
    /**
     * @var Device
     */
    private $Device;
    /**
     * @var Operation
     */
    private $Operation;
    /**
     * @var OperationDevice
     */
    private $OperationDevice;
    /**
     * @var Shift
     */
    private $Shift;
    /**
     * @var DeviceServices
     */
    private $DeviceServices;
    /**
     * @var DeviceShift
     */
    private $DeviceShift;
    /**
     * @var Setting
     */
    private $Setting;
    /**
     * @var Holiday
     */
    protected $Holiday;
    /**
     * @var Standard
     */
    private $Standard;
    /**
     * @var array
     */
    private $configs;
    /**
     * @var DateComponent
     */
    protected $DateComponent;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Standard = Standard::getInstance();

        $this->Filter = Filter::getInstance();
        $this->Address = Address::getInstance();
        $this->DpProduct = DpProduct::getInstance();
        $this->DpProductFile = DpProductFile::getInstance();
        $this->PrintShopType = PrintShopType::getInstance();
        $this->UserCalc = UserCalc::getInstance();
        $this->UserCalcProduct = UserCalcProduct::getInstance();
        $this->UserCalcProductAttribute = UserCalcProductAttribute::getInstance();
        $this->UserCalcProductSpecialAttribute = UserCalcProductSpecialAttribute::getInstance();
        $this->ProductionPath = new ProductionPath();
        $this->Ongoing = Ongoing::getInstance();
        $this->OngoingLog = OngoingLog::getInstance();
        $this->Department = Department::getInstance();
        $this->Device = Device::getInstance();
        $this->Operation = Operation::getInstance();
        $this->OperationDevice = OperationDevice::getInstance();
        $this->Shift = Shift::getInstance();
        $this->DeviceServices = DeviceServices::getInstance();
        $this->Setting = Setting::getInstance();
        $this->DeviceShift = DeviceShift::getInstance();
        $this->Holiday = Holiday::getInstance();
        $this->DateComponent = DateComponent::getInstance();

    }

    /**
     * product list
     * @method index
     *
     * @param array
     * @return array
     */
    public function index($params)
    {
        $departments = $this->Department->getAll();
        foreach($departments as &$department){
            $devices = $this->Device->get('departmentID', $department['ID'], true);
            foreach($devices as &$device){
                    $ongoings = $this->Ongoing->getByDeviceIDDate($device['ID']);
                    foreach($ongoings as &$ongoing){
                        $ongoing['plannedEnd'] = null;
                        if($ongoing['plannedStart'] != null){
                            $ongoing['plannedEnd'] = date("Y-m-d H:i:s",  strtotime($ongoing['plannedStart'])+$ongoing['estimatedTime']);
                        }

                        $logs = $this->OngoingLog->get('ongoingID', $ongoing['ID'], true);
                        $ongoing['logs'] = $logs;

                        $lastLog = NULL;
                        $diffTimes = array();
                        foreach ($logs as $key => $row) {
                            if (($row['state'] == 2 || $row['state'] == 3) && $lastLog && $lastLog['state'] == 1) {
                                $diffTimes[] = strtotime($row['date']) - strtotime($lastLog['date']);
                            }
                            $lastLog = $row;
                        }
                        $ongoing['sumTime'] = array_sum($diffTimes);

                        $ongoing['clientAddress'] = $this->Address->getByUser($ongoing['userID']);

                        $startLog = $this->OngoingLog->getStartLog($ongoing['ID']);
                        if (!$startLog){
                            $startLog = null;
                        }
                        $lastLog = $this->OngoingLog->getLastLog($ongoing['ID']);
                        if (!$lastLog){
                            $lastLog = null;
                        }
                        $ongoing['startLog'] = $startLog;
                        $ongoing['lastLog'] = $lastLog;
                    }
                $device['ongoings'] = $ongoings;
                $device['services'] = $this->DeviceServices->getListByID($device['ID']);
                $device['shifts'] = $this->DeviceShift->getByDeviceIDSorted($device['ID']);
                $device['startDay'] = $this->DeviceShift->getDayStartHour($device['ID'])['start'];
                $device['finishDay'] = $this->DeviceShift->getDayFinishHour($device['ID'])['stop'];
            }
            $department['devices'] = $devices;

            $department['generationDate'] = date("Y-m-d H:i:s");
            $this->Setting->setModule('productionPath');
            $this->Setting->setDomainID(NULL);
            $this->Setting->setLang(NULL);
            $department['defaultGanttScale'] = $this->Setting->getValue('defaultGanttScale');

            $nationalHolidays = $this->Holiday->getHolidays('nationalholiday');
            $churchHolidays = $this->DateComponent->getChurchHolidays($this->DateComponent->getEasterDate(date('Y')), date('Y'));
            $allHolidays = array_merge($nationalHolidays, $churchHolidays);
            $department['holidays'] = $allHolidays;

        }

        return $departments;
    }

    /**
     * @param $params
     * @return array
     */
    public function count($params)
    {
        return array('count' => 2);
    }

    /*public function indexOLD($params)
    {
        
        $department = $this->Department->get('ID', $params['department']);
        
            $devices = $this->Device->get('departmentID', $department['ID'], true);
            foreach($devices as &$device){
                $operations = $this->OperationDevice->get('deviceID', $device['ID'], true);
                foreach($operations as &$operation){
                    $operation['operation'] = $this->Operation->get('ID', $operation['operationID']);

                    $ongoings = $this->Ongoing->getByDeviceIDOperationIDDate($operation['deviceID'], $operation['operationID']);
                    foreach($ongoings as &$ongoing){
                        $ongoing['plannedEnd'] = null;
                        if($ongoing['plannedStart'] != null){
                            $ongoing['plannedEnd'] = date("Y-m-d H:i:s",  strtotime($ongoing['plannedStart'])+$ongoing['estimatedTime']);
                        }

                        $logs = $this->OngoingLog->get('ongoingID', $ongoing['ID'], true);
                        $ongoing['logs'] = $logs;

                        $startLog = $this->OngoingLog->getStartLog($ongoing['ID']);
                        if (!$startLog){
                            $startLog = null;
                        }
                        $lastLog = $this->OngoingLog->getLastLog($ongoing['ID']);
                        if (!$lastLog){
                            $lastLog = null;
                        }
                        $ongoing['startLog'] = $startLog;
                        $ongoing['lastLog'] = $lastLog;
                    }

                    $operation['ongoings'] = $ongoings;
                }
                $device['operations'] = $operations;
            }
            $department['devices'] = $devices;
        

        return [$department];
    }*/
}