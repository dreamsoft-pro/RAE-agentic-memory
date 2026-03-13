<?php
/**
 * Created by PhpStorm.
 * User: Rafał
 * Date: 10-07-2018
 * Time: 12:00
 */
namespace DreamSoft\Controllers\ProductionPath;

use DreamSoft\Core\Controller;
use DreamSoft\Controllers\Components\Standard;
use DreamSoft\Models\ProductionPath\Pause;

class PausesController extends Controller
{
    /**
     * @var Standard
     */
    private $Standard;
    /**
     * @var Pause
     */
    private $Pause;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->Pause = Pause::getInstance();
        $this->Standard = Standard::getInstance();

    }

    /**
     * @return array|bool
     */
    public function pauses()
    {
        $pauses = $this->Pause->getAll();

        if (!$pauses) {
            return array();
        }

        $pauses = $this->Standard->sortData($pauses, 'sort');

        return $pauses;
    }

    public function post_pauses()
    {
        $name = $this->Data->getPost('name');
        $color = $this->Data->getPost('color');

        $data['response'] = true;

        if ($name) {

            $sort = $this->Pause->getMaxSort();

            if (!$sort) {
                $sort = 1;
            } else {
                $sort++;
            }

            $created = date(DATE_FORMAT);

            $lastID = $this->Pause->create(compact('name', 'sort', 'created', 'color'));
            if ($lastID > 0) {
                $one = $this->Pause->get('ID', $lastID);
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
    public function patch_pauses()
    {
        $post = $this->Data->getAllPost();

        $updated = 0;
        if ($post) {
            foreach ($post as $pause) {
                $existRow = $this->Pause->get('ID', $pause['ID']);
                if ($existRow) {
                    $report_sheets = intval($pause['report_sheets']);
                    $localUpdated = 0;
                    $localUpdated = intval($this->Pause->update($existRow['ID'], 'report_sheets', $report_sheets));

                    if($localUpdated > 0) {
                        $updated++;
                    }
                }
            }
        } else {
            return $this->sendFailResponse('01');
        }

        if ($updated > 0) {
            return array(
                'response' => true,
                'updated' => $updated
            );
        }

        return $this->sendFailResponse('03');
    }

    /**
     * @return array
     */
    public function put_pauses()
    {
        $ID = $this->Data->getPost('ID');
        if (!$ID) {
            return $this->sendFailResponse('06');
        }

        $data['response'] = false;

        $name = $this->Data->getPost('name');
        $color = $this->Data->getPost('color');
        $saved = 0;
        if ($name) {
            $saved += intval($this->Pause->update($ID, 'name', $name));
            $saved += intval($this->Pause->update($ID, 'color', $color));
            if ($saved > 0) {
                $data['item'] = $this->Pause->get('ID', $ID);
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
    public function delete_pauses($ID)
    {
        if ($ID) {
            if ($this->Pause->delete('ID', $ID)) {
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
        if ($this->Pause->sort($post)) {
            return array('response' => true);
        } else {
            return $this->sendFailResponse('03');
        }
    }
}