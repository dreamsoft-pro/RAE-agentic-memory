<?php
define('BASE_DIR', dirname(__FILE__) . '/');
define('BS', chr(92));
define('APP_DIR', BASE_DIR . 'app/');
$_SERVER['REQUEST_URI'] = '';
define('sourceApp', 'manager');
define('lang', 'pl');
define('companyID', 25);
define('domainID', 4);
error_reporting(E_ERROR);
function invokeNotPubMethod(&$object, $methodName, array $parameters = array())
{
    $reflection = new \ReflectionClass(get_class($object));
    $method = $reflection->getMethod($methodName);
    $method->setAccessible(true);
    return $method->invokeArgs($object, $parameters);
}
function setNotPubField(&$object, $fieldName,$value)
{
    $reflection = new \ReflectionClass(get_class($object));
    $field = $reflection->getProperty($fieldName);
    $field->setAccessible(true);
    return $field->setValue($object, $value);
}
