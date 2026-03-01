<?php
namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Controllers\Components\Standard;
use DreamSoft\Models\ProductionPath\Shift;

class ShiftsController extends Controller
{
    /**
     * @var Standard
     */
    private $Standard;
    /**
     * @var Shift
     */
    private $Shift;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Shift = Shift::getInstance();
        $this->Standard = Standard::getInstance();

    }

    /**
     * @return array|bool
     */
    public function shifts()
    {
        $shifts = $this->Shift->getAll();

        if (!$shifts) {
            return array();
        }

        $shifts = $this->Standard->sortData($shifts, 'sort');

        return $shifts;
    }

    public function post_shifts()
    {
        $name = $this->Data->getPost('name');
        $start = $this->Data->getPost('start');
        $stop = $this->Data->getPost('stop');

        $data['response'] = true;

        if ($name) {

            $sort = $this->Shift->getMaxSort();

            if (!$sort) {
                $sort = 1;
            } else {
                $sort++;
            }

            $created = date(DATE_FORMAT);

            $lastID = $this->Shift->create(compact('name', 'sort', 'start', 'stop'));
            if ($lastID > 0) {
                $one = $this->Shift->get('ID', $lastID);
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
            $saved += intval($this->Shift->update($ID, 'name', $name));
            $saved += intval($this->Shift->update($ID, 'start', $start));
            $saved += intval($this->Shift->update($ID, 'stop', $stop));
            if ($saved > 0) {
                $data['item'] = $this->Shift->get('ID', $ID);
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
            if ($this->Shift->delete('ID', $ID)) {
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
        if ($this->Shift->sort($post)) {
            return array('response' => true);
        } else {
            return $this->sendFailResponse('03');
        }
    }
}