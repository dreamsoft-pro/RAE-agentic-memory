<?php

namespace DreamSoft\Controllers\Authorization;

use DreamSoft\Core\Controller;
use DreamSoft\Models\Authorization\AuthorizationLog;
use DreamSoft\Controllers\Components\QueryFilter;
use DreamSoft\Models\User\User;

class AuthorizationLogsController extends Controller
{
    protected $QueryFilter;
    protected $AuthorizationLog;
    protected $User;
    private $configs;

    public $useModels = array();

    public function __construct($params)
    {
        parent::__construct($params);
        $this->User = User::getInstance();
        $this->AuthorizationLog = AuthorizationLog::getInstance();
        $this->QueryFilter = new QueryFilter();
        $this->setConfigs();
    }

    private function setConfigs()
    {
        $this->configs = array(
            'ID' => array('type' => 'string', 'table' => 'authorizationLogs', 'alias' => true, 'field' => 'ID', 'sign' => $this->QueryFilter->signs['li']),
            'dateFrom' => array('type' => 'timestamp', 'table' => 'authorizationLogs', 'alias' => true, 'field' => 'created', 'sign' => $this->QueryFilter->signs['gt']),
            'dateTo' => array('type' => 'timestamp', 'table' => 'authorizationLogs', 'field' => 'created', 'alias' => true, 'sign' => $this->QueryFilter->signs['lt']),
            'userID' => array('type' => 'string', 'table' => 'authorizationLogs', 'alias' => true, 'field' => 'userID', 'sign' => $this->QueryFilter->signs['li']),
        );
    }

    public function getConfigs()
    {
        return $this->configs;
    }

    public function index($params)
    {
        $limit = $params['limit'] ?? 30;
        $offset = $params['offset'] ?? 0;
        $sortBy = isset($params['sort']) ? explode('|', $params['sort']) : array('-ID');

        $filters = $this->QueryFilter->prepare($this->configs, $params);
        $list = $this->AuthorizationLog->getList($filters, $offset, $limit, $sortBy);

        if (!$list) {
            return array();
        }

        $aggregateUsers = array_column($list, 'userID');
        $users = $this->User->getByList($aggregateUsers);

        foreach ($list as $key => $row) {
            if (isset($users[$row['userID']])) {
                $list[$key]['user'] = $users[$row['userID']];
            }
        }

        return $list;
    }

    public function count($params = NULL)
    {
        $filters = $this->QueryFilter->prepare($this->configs, $params);
        $count = $this->AuthorizationLog->count($filters);
        return array('count' => $count);
    }

    public function delete_deleteByUser($userID)
    {
        $deleted = $this->AuthorizationLog->delete('userID', $userID);
        return array('response' => $deleted);
    }
}
