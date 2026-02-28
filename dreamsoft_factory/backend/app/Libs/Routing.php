<?php

namespace DreamSoft\Libs;

/**
 *
 * @class Routing
 */

class Routing
{


    public $companyID;
    public $controller;
    public $action;
    public $params = array();
    public $module = false;
    public $parents = array();
    public $package = NULL;
    public $autoload = false;
    private $resources;

    /**
     * Routing constructor.
     * @param null $companyID
     */
    public function __construct($companyID = NULL)
    {

        if ($companyID > 0) {
            $this->setCompanyID($companyID);
        } else {
            $this->setCompanyID(35);
        }
        $this->resources=RoutingResources::getResources();
        $this->parseUri();
    }

    /**
     * @return bool
     *
     */
    public function getModule()
    {
        return $this->module;
    }

    /**
     * @param $module
     */
    public function setModule($module)
    {
        $this->module = $module;
    }

    /**
     * @return mixed
     */
    public function getCompanyID()
    {
        return $this->companyID;
    }

    /**
     * @return mixed
     */
    public function getController()
    {
        return $this->controller;
    }

    /**
     * @return mixed
     */
    public function getAction()
    {
        return $this->action;
    }

    private function addParam($val)
    {
        $this->params[] = $val;
    }
    /**
     * @return array
     */
    public function getParams()
    {
        if (empty($this->params)) {
            return array();
        }
        return $this->params;
    }

    /**
     * @return array
     */
    public function getParents()
    {
        return $this->parents;
    }

    /**
     * @return array
     */
    public function getResources()
    {
        return $this->resources;
    }

    /**
     * @param $companyID
     */
    public function setCompanyID($companyID)
    {
        $this->companyID = $companyID;
    }

    /**
     * @return null
     */
    public function getPackage()
    {
        return $this->package;
    }

    /**
     * @return bool
     */
    public function getAutoload()
    {
        return $this->autoload;
    }

    /**
     * @param null $uri
     * @return bool
     */
    public function parseUri($uri = NULL)
    {
        if ($uri === NULL) {

            $exp = explode('?', $_SERVER['REQUEST_URI']);
            if (isset($exp[1]) && !empty($exp[1])) {
                $ap = explode('&', $exp[1]);
                $addedParams = array();
                foreach ($ap as $key => $val) {
                    $expAp = explode("=", $val);
                    $addedParams[$expAp[0]] = $expAp[1];
                }
            } else {
                $addedParams = array();
            }
            $uri = explode('/', $exp[0]);
            unset($exp);

            array_shift($uri);
            if( strlen(REQUEST_URI_PREFIX) > 0 && $uri[0] == REQUEST_URI_PREFIX ) {
                array_shift($uri);
            }
        }

        switch ($_SERVER['REQUEST_METHOD']) {
            case "POST":
                $prefix = 'post_';
                break;
            case "DELETE":
                $prefix = 'delete_';
                break;
            case "PUT":
                $prefix = 'put_';
                break;
            default:
                $prefix = '';
                break;
        }

        if ($this->getHeader('x-http-method-override') == 'put') {
            $prefix = 'put_';
        } elseif ($this->getHeader('x-http-method-override') == 'patch') {
            $prefix = 'patch_';
        }


        $this->companyID = $this->getCompanyID();

        foreach ($uri as $key => $r) {

            if ($key % 2 == 0) {
                if (isset($this->resources[$r]['childs'])) {
                    $childs = $this->resources[$r]['childs'];
                } else {
                    $childs = array();
                }

                if (isset($this->resources[$r]['custom'])) {
                    $customs = $this->resources[$r]['custom'];
                } else {
                    $customs = array();
                }

                if (isset($uri[$key + 2]) && in_array($uri[$key + 2], $childs)) {
                    $this->addParam($uri[$key + 1]);
                    $uri = array_splice($uri, 2, count($uri));

                    if (!empty($addedParams)) {
                        $this->addParam($addedParams);
                    }

                    return $this->parseUri($uri);
                } elseif (isset($uri[$key + 1]) && in_array($uri[$key + 1], $customs)) {

                    $this->controller = ucfirst($this->resources[$r]['controller']) . 'Controller';
                    $customKey = array_search($uri[$key + 1], $customs);
                    $this->action = $prefix . $this->resources[$r]['custom'][$customKey];
                    if (isset($uri[$key + 2])) {
                        for ($ki = $key + 2; $ki < count($uri); $ki++) {
                            $this->addParam($uri[$ki]);
                        }
                    }
                    if (!empty($addedParams)) {
                        $this->addParam($addedParams);
                    }
                    if (isset($this->resources[$r]['package'])) {
                        $this->package = $this->resources[$r]['package'];
                    } else {
                        $this->package = NULL;
                    }

                    if (isset($this->resources[$r]['autoload'])) {
                        $this->autoload = true;
                    } else {
                        $this->autoload = false;
                    }
                    return true;
                } else {
                    if( array_key_exists($r, $this->resources) ) {
                        $this->controller = ucfirst($this->resources[$r]['controller']) . 'Controller';
                        $this->action = $prefix . $this->resources[$r]['action'];
                    }
                    if (isset($this->resources[$r]['module']) &&
                        $this->resources[$r]['module'] == true && isset($uri[$key + 1])
                    ) {
                        $this->setModule($uri[$key + 1]);
                        if (isset($uri[$key + 2])) {
                            $this->addParam($uri[$key + 2]);
                        }
                    } elseif (isset($uri[$key + 1])) {
                        for ($i = $key + 1; $i < count($uri); $i++) {
                            $this->addParam($uri[$i]);
                        }
                    }
                    if (!empty($addedParams)) {
                        $this->addParam($addedParams);
                    }
                    if (isset($this->resources[$r]['package'])) {
                        $this->package = $this->resources[$r]['package'];
                    } else {
                        $this->package = NULL;
                    }

                    if (isset($this->resources[$r]['autoload'])) {
                        $this->autoload = true;
                    } else {
                        $this->autoload = false;
                    }
                    return true;
                }
            }
        }
        return false;

        $resource = NULL;
        if (is_numeric(end($uri))) {
            $resource = prev($uri);
        } else {
            $resource = end($uri);
        }

        if (isset($this->resources[$resource]['recursive']) && $this->resources[$resource]['recursive'] === true) {

            $this->controller = ucfirst($this->resources[$resource]['controller']) . 'Controller';
            $this->action = $prefix . $this->resources[$resource]['action'];

            array_shift($uri);
            foreach ($uri as $key => $u) {
                if ($key % 2 == 1) {
                    $this->addParam($u);
                }
            }
            return true;

        } elseif (key_exists($uri[1], $this->resources)) {
            $resourceIndex = 1;
            $paramIndex = 2;
            $childIndex = 3;
            $childParmIndex = 4;
            $customIndex = 2;
            $customParam = 3;
            if (isset($this->resources[$uri[$resourceIndex]]['module']) &&
                $this->resources[$uri[$resourceIndex]]['module'] == true
            ) {
                $this->setModule($uri[2]);
                $paramIndex = 3;
            }

            if (isset($this->resources[$uri[$resourceIndex]]['childs']) &&
                isset($uri[$childIndex]) &&
                strlen($uri[$childIndex]) > 0 &&
                in_array($uri[$childIndex], $this->resources[$uri[$resourceIndex]]['childs'])
            ) {
                $child = $uri[$childIndex];
                $this->parents[] = $uri[1];
                $this->controller = ucfirst($this->resources[$uri[$resourceIndex]]['controller']) . 'Controller';
                $this->action = $prefix . $child;
                $this->addParam($uri[$paramIndex]);
                if (isset($uri[$childParmIndex])) {
                    $this->addParam($uri[$childParmIndex]);
                }
            } elseif (
                isset($this->resources[$uri[$resourceIndex]]['custom']) &&
                isset($uri[$customIndex]) &&
                strlen($uri[$customIndex]) > 0 &&
                in_array($uri[$customIndex], $this->resources[$uri[$resourceIndex]]['custom'])
            ) {
                $actionKey = array_search($uri[$customIndex], $this->resources[$uri[$resourceIndex]]['custom']);
                $this->parents[] = $uri[1];
                $this->controller = ucfirst($this->resources[$uri[$resourceIndex]]['controller']) . 'Controller';
                $this->action = $prefix . $this->resources[$uri[$resourceIndex]]['custom'][$actionKey];
                if (isset($uri[$customParam])) {
                    $this->addParam($uri[$customParam]);
                }

            } else {

                $this->controller = ucfirst($this->resources[$uri[$resourceIndex]]['controller']) . 'Controller';
                $this->action = $prefix . $this->resources[$uri[$resourceIndex]]['action'];
                //$pUri = array_slice ($uri, $paramIndex);
                if (isset($uri[$paramIndex]) && strlen($uri[$paramIndex]) > 0) {
                    $this->addParam($uri[$paramIndex]);
                }

            }
            return true;
        }

        $skipAction = false;
        $ctrlIndex = 1;
        if (isset($uri[$ctrlIndex]) && !empty($uri[$ctrlIndex])) {
            $ctrl = ucfirst($uri[$ctrlIndex]);
        } else {
            $ctrl = 'Index';
        }
        $actionIndex = 2;
        if (isset($uri[$actionIndex]) && !empty($uri[$actionIndex])) {
            $action = $uri[$actionIndex];
        } else {
            $skipAction = true;
            $action = 'index';
        }

        $this->controller = $ctrl . 'Controller';
        if ($skipAction) {
            $pUri = array_slice($uri, 3);
        } else {
            $pUri = array_slice($uri, 4);
        }
        $this->params = $this->prepareParams($pUri);
        $this->action = $prefix . $action;

        return true;
    }

    /**
     * @param $parameters
     * @param bool $resource
     * @return array
     */
    public function prepareParams($parameters, $resource = false)
    {

        if (empty($parameters) || !is_array($parameters)) {
            return array();
        }

        if ($resource) {

            foreach ($parameters as $key => $val) {
                if ($key == 0) {
                    $param[] = $val;
                } else {
                    if ($key % 2 == 0) {
                        $param[] = $val;
                    } else {
                        $currentResource = $val;
                        $paramKeys = array_keys($parameters);
                        if (end($paramKeys) == $key) {
                            $param[] = array('resource' => $currentResource);
                        }
                    }
                }
            }
            return $param;
        }

        $prev=null;
        foreach ($parameters as $key => $val) {
            if ($key % 2 == 0) {
                $params[$val] = NULL;
                $prev = $val;
            } else {
                $params[$prev] = $val;
            }
        }

        return $params;
    }

    /**
     * @param $name
     * @return bool
     */
    public function getHeader($name)
    {
        $headers = apache_request_headers();
        foreach ($headers as $header => $value) {
            if (strtolower($header) == $name && strlen($value) > 0) {
                return $value;
            }
        }
        return false;
    }

}
