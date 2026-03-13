<?php
namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Controllers\Components\Standard;
use DreamSoft\Models\ProductionPath\DeviceShift;

class DeviceShiftController extends Controller
{
    /**
     * @var Standard
     */
    private $Standard;
    /**
     * @var DeviceShift
     */
    private $DeviceShift;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->DeviceShift = DeviceShift::getInstance();
        $this->Standard = Standard::getInstance();

    }

    /**
     * @return array|bool
     */
    public function shifts($deviceID)
    {
        $shifts = $this->DeviceShift->get('deviceID', $deviceID, true);

        if (!$shifts) {
            return array();
        }

        $shifts = $this->Standard->sortData($shifts, 'sort');

        return $shifts;
    }

    public function post_shifts()
    {
        $name = $this->Data->getPost('name');
        $deviceID = $this->Data->getPost('deviceID');
        $start = $this->Data->getPost('start');
        $stop = $this->Data->getPost('stop');

        $data['response'] = true;

        if ($name) {

            $sort = $this->DeviceShift->getMaxSort();

            if (!$sort) {
                $sort = 1;
            } else {
                $sort++;
            }

            $created = date(DATE_FORMAT);

            $lastID = $this->DeviceShift->create(compact('name', 'deviceID', 'sort', 'start', 'stop'));
            if ($lastID > 0) {
                $one = $this->DeviceShift->get('ID', $lastID);
                $data['item'] = $one;
            }
        } else {
            return $this->sendFailResponse('02');
        }
        return $data;
    }

    /**
     * @return array
     */
    public function put_shifts()
    {
        $ID = $this->Data->getPost('ID');
        if (!$ID) {
            return $this->sendFailResponse('06');
        }

        $data['response'] = false;

        $name = $this->Data->getPost('name');
        $start = $this->Data->getPost('start');
        $stop = $this->Data->getPost('stop');
        $saved = 0;
        if ($name) {
            $saved += intval($this->DeviceShift->update($ID, 'name', $name));
            $saved += intval($this->DeviceShift->update($ID, 'start', $start));
            $saved += intval($this->DeviceShift->update($ID, 'stop', $stop));
            if ($saved > 0) {
                $data['item'] = $this->DeviceShift->get('ID', $ID);
                $data['response'] = true;
            }
        } else {
            $data = $this->sendFailResponse('02');
        }
        return $data;
    }

    /**
     * @param $ID
     * @return mixed
     */
    public function delete_shifts($ID)
    {
        if ($ID) {
            if ($this->DeviceShift->delete('ID', $ID)) {
                $data['response'] = true;
                return $data;
            }
        } else {
            $data['response'] = false;
            return $data;
        }
    }

    /**
     * @return array
     */
    public function patch_sort()
    {
        $post = $this->Data->getAllPost();
        if ($this->DeviceShift->sort($post)) {
            return array('response' => true);
        } else {
            return $this->sendFailResponse('03');
        }
    }

    public function post_copyFrom()
    {
        $copyTo = $this->Data->getPost('copyToDeviceID');
        $copyFrom = $this->Data->getPost('copyFromDeviceID');

        $data['response'] = true;

        if ($copyTo && $copyFrom) {

            $this->DeviceShift->delete('deviceID', $copyTo);

            $shifts = $this->DeviceShift->get('deviceID', $copyFrom, true);
            $newShifts = array();
            foreach($shifts as $shift){
                $name = $shift['name'];
                $deviceID = $copyTo;
                $sort = $shift['sort'];
                $start = $shift['start'];
                $stop = $shift['stop'];
                $lastID = $this->DeviceShift->create(compact('name', 'deviceID', 'sort', 'start', 'stop'));
                $newShifts[] = $this->DeviceShift->get('ID', $lastID);
            }

            usort($newShifts, function ($item1, $item2) {
                return $item1['sort'] <=> $item2['sort'];
            });
            $data['items'] = $newShifts;
        } else {
            return $this->sendFailResponse('02');
        }
        return $data;
    }
}