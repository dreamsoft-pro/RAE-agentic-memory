<?php

namespace DreamSoft\Core;

use DreamSoft\Libs\Debugger;
use DreamSoft\Libs\Data;
use DreamSoft\Libs\Auth;
use DreamSoft\Controllers\Components\Acl;
use stdClass;
use Exception;

class Controller extends Debugger
{
    private $modelsDir;
    private $componentsDir;
    private $responseCodes;

    public $useModels = [];
    public $useComponents = [];
    public $parents = [];
    public $models;
    public $components;
    public $params;
    public $Data;
    protected $Auth;
    protected $domainID = false;

    /**
     * Controller constructor.
     * @param array $parameters
     */
    public function __construct($parameters = [])
    {
        parent::__construct();
        $this->setDebugName('controllers');

        $this->initResponseCodes();
        $this->modelsDir = 'models';
        $this->componentsDir = 'controllers/components';

        $this->models = new stdClass();
        $this->components = new stdClass();

        $this->params = $parameters;

        $this->Data = new Data();
        $this->Auth = new Auth();

        $this->params['lang'] = $this->params['lang'] ?? 'pl';
    }

    /**
     * @param $errorCode
     * @param null $info
     * @return array
     */
    public function sendFailResponse($errorCode, $info = null)
    {
        $response = $this->responseCodes[$errorCode] ?? $this->responseCodes['07'];
        if ($info) {
            $response['info'] = $info;
        }
        return $response;
    }

    /**
     * Initialize response codes.
     */
    public function initResponseCodes()
    {
        $this->responseCodes = [
            '01' => ['httpCode' => 400, 'info' => 'empty_post', 'response' => false],
            '02' => ['httpCode' => 400, 'info' => 'fill_fields_of_form', 'response' => false],
            '03' => ['httpCode' => 500, 'info' => 'data_could_not_be_saved', 'response' => false],
            '04' => ['httpCode' => 400, 'info' => 'no_identifier', 'response' => false],
            '05' => ['httpCode' => 500, 'info' => 'Nie udało się usunąć obiektu', 'response' => false],
            '06' => ['httpCode' => 400, 'info' => 'Obiekt o podanym identyfikatorze nie istnieje', 'response' => false],
            '07' => ['httpCode' => 400, 'info' => 'Błąd niestandardowy', 'response' => false],
            '08' => ['httpCode' => 400, 'info' => 'Występuje duplikat unikalnego klucza tego obiektu', 'response' => false],
            '09' => ['httpCode' => 400, 'info' => 'Problem z nazwami językowymi', 'response' => false],
            '10' => ['httpCode' => 400, 'info' => 'Błąd podczas zapisu', 'response' => false],
            '11' => ['httpCode' => 400, 'info' => 'Zapytanie nie może zostać przetworzone', 'response' => false],
            '12' => ['httpCode' => 401, 'info' => 'Nie masz uprawnień do tej akcji', 'response' => false],
            '13' => ['httpCode' => 400, 'info' => 'Nie prawidłowa akcja', 'response' => false],
            '14' => ['httpCode' => 400, 'info' => 'Próba edycji danych innego użytkownika', 'response' => false],
            '15' => ['httpCode' => 400, 'info' => 'Taka relacja już istnieje', 'response' => false],
            '16' => ['httpCode' => 400, 'info' => 'Brak formatów w produkcie. Należy je skonfigurować.', 'response' => false],
            '17' => ['httpCode' => 403, 'info' => 'User not logged.', 'response' => false],
            '18' => ['httpCode' => 400, 'info' => 'User not exist.', 'response' => false],
            '19' => ['httpCode' => 400, 'info' => 'Captcha not valid.', 'response' => false],
            '20' => ['httpCode' => 400, 'info' => 'date expires', 'response' => false]
        ];
    }

    /**
     * @param $controller
     * @param $action
     * @param null $package
     * @param null $user
     * @return bool
     */
    public function checkPerms($controller, $action, $package = null, $user = null)
    {
        $Acl = new Acl();
        return $Acl->checkPerms($controller, $action, $package, $user);
    }

    /**
     * @param $index
     * @return bool|mixed
     */
    public function getParam($index)
    {
        return $this->params[$index] ?? false;
    }

    /**
     * @param $parents
     */
    public function setParents($parents)
    {
        $this->parents = $parents;
    }

    /**
     * @return bool
     */
    protected function _check_login()
    {
        return $this->Auth->checkLogin();
    }

    /**
     *
     */
    public static function sendJson()
    {
        header('Content-Type: application/json');
    }

    /**
     * @throws Exception
     */
    public function useModels()
    {
        error_log('Controller - useModels: ' . get_called_class());

        /*
        if (!empty($this->useModels) && is_array($this->useModels)) {
            foreach ($this->useModels as $key => $row) {
                error_log(var_export($row, true));
                if (is_array($row)) {
                    if (is_file($this->modelsDir . '/' . $row['package'] . '/' . $key . '.php')) {
                        include_once($this->modelsDir . '/' . $row['package'] . '/' . $key . '.php');
                    } else {
                        throw new Exception('Problem z modelem ' . $key . ' nie istnieje lub ma złą nazwę.');
                    }
                } else {
                    if (is_file($this->modelsDir . '/' . $row . '.php')) {
                        include_once($this->modelsDir . '/' . $row . '.php');
                    } else {
                        throw new Exception('Problem z modelem ' . $row . ' nie istnieje lub ma złą nazwę.');
                    }
                }
            }
        }
        */
    }

    /**
     * @throws Exception
     */
    public function useComponents()
    {
        error_log('Controller - useComponents: ' . get_called_class());

        /*
        if (!empty($this->useComponents) && is_array($this->useComponents)) {
            foreach ($this->useComponents as $row) {
                if (is_file($this->componentsDir . '/' . $row . '.php')) {
                    include_once($this->componentsDir . '/' . $row . '.php');
                    $nameRow = $row;
                    $this->components->{$row} = new $nameRow();
                } else {
                    throw new Exception('Problem z komponentem ' . $row . ' nie istnieje lub ma złą nazwę.');
                }
            }
        }
        */
    }

    /**
     * @param $ID
     */
    public function setDomainID($ID)
    {
        $this->domainID = $ID;
    }

    /**
     * @return bool
     */
    public function getDomainID()
    {
        return $this->domainID;
    }

    /**
     * @param $Model
     * @return mixed
     */
    public function checkModelErrors($Model)
    {
        $errors = $Model->getErrors();
        return !empty($errors) ? $errors : null;
    }

    /**
     * @param $module
     * @param $name
     * @return bool|string
     */
    public function getView($module, $name)
    {
        $file = BASE_DIR . 'views' . DIRECTORY_SEPARATOR . $module . DIRECTORY_SEPARATOR . $name . '.html';
        if (is_file($file)) {
            return file_get_contents($file);
        } else {
            $this->debug('problem with: ' . $module . ' - ' . $name);
            return false;
        }
    }
}
