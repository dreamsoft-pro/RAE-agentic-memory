<?php

namespace DreamSoft\Core;

use DreamSoft\Libs\Debugger;
use stdClass;
use Exception;

class Component extends Debugger
{
    private $modelsDir;
    private $componentsDir;

    public $useModels = [];
    public $useComponents = [];

    public $models;
    public $components;

    public function __construct()
    {
        parent::__construct();
        $this->setDebugName('components');

        $this->modelsDir = BASE_DIR . 'models';
        $this->componentsDir = BASE_DIR . 'controllers/components';

        $this->models = new stdClass();
        $this->components = new stdClass();
    }

    /**
     * Log the usage of models.
     * @throws Exception
     */
    public function useModels()
    {
        error_log('Component - useModels: ' . get_called_class());
    }

    /**
     * Log the usage of components.
     * @throws Exception
     */
    public function useComponents()
    {
        error_log('Component - useComponents: ' . get_called_class());
    }
}
