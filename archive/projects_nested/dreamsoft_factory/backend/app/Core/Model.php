<?php

namespace DreamSoft\Core;

use DreamSoft\Libs\ConnectionFactory;
use DreamSoft\Libs\ConnectionSwitchFactory;
use DreamSoft\Libs\Debugger;
use DreamSoft\Libs\Singleton;
use stdClass;
use Exception;

/**
 * Class Model
 * @package DreamSoft\Libs
 */
class Model extends Singleton
{
    /**
     * @var ConnectionFactory
     */
    public $db;
    public $isRoot;
    public $tableName;
    public $prefix;
    public $behaviours;
    protected $isPrefix = true;
    private $behavioursDir;
    public $hasMany = [];
    public $fields = '*';
    public $useBehaviours;
    protected $Errors = [];

    /**
     * Model constructor.
     * @param bool $root
     * @param null $companyID
     */
    public function __construct($root = false, $companyID = null)
    {
        parent::__construct();
        $this->isRoot = $root;
        $this->behavioursDir = BASE_DIR . 'models/behaviours';
        $this->behaviours = new stdClass();

        try {
            $connectionFactory = new ConnectionSwitchFactory($root, $companyID);
            $this->setDb($connectionFactory->getConnection());
            if ($root) {
                $this->updateTrace();
            }
        } catch (Exception $e) {
            $this->debug($e->getMessage());
        }

        $this->prefix = 'dp_';
        try {
            $this->useBehaviours();
        } catch (Exception $e) {
            $this->debug($e->getMessage());
        }
    }

    /**
     * @param mixed $db
     */
    public function setDb($db)
    {
        $this->db = $db;
    }

    /**
     * @return ConnectionFactory
     */
    public function getDb()
    {
        return $this->db;
    }

    /**
     *
     */
    public function __destruct()
    {
        $allModelErrors = [];
        if (is_object($this->db)) {
            $allModelErrors = $this->db->getError();
            $this->db->close();
        } else {
            $allModelErrors[] = 'Object $this->db is not an object';
        }

        if (!empty($allModelErrors)) {
            $this->debug($allModelErrors);
        }
    }

    /**
     * @param $newError
     */
    public function setError($newError)
    {
        $this->Errors[] = $newError;
    }

    /**
     * @return array
     */
    public function getErrors()
    {
        return $this->Errors;
    }

    /**
     * @return string
     */
    public function getDbError()
    {
        return $this->db->getError();
    }

    /**
     * @return mixed
     */
    public function getDBName()
    {
        $query = 'SELECT database()';
        $this->db->exec($query);
        return $this->db->getOne();
    }

    /**
     * @param $name
     * @param bool $prefix
     */
    public function setTableName($name, $prefix = true)
    {
        $this->isPrefix = $prefix;
        $this->tableName = $name;
    }

    /**
     * @return string
     */
    public function getTableName()
    {
        return $this->isPrefix ? $this->prefix . $this->tableName : $this->tableName;
    }

    /**
     * @return string
     */
    public function getModelName()
    {
        return get_called_class();
    }

    /**
     * @param $fields
     */
    public function setFields($fields)
    {
        $this->fields = $fields;
    }

    /**
     * @return string
     */
    public function getFields()
    {
        return $this->fields;
    }

    /**
     * @param $key
     * @param $value
     * @param bool $multiple
     * @return mixed
     */
    public function get($key, $value, $multiple = false)
    {
        $fields = is_array($this->fields) ? implode(',', array_map(fn($field) => "`{$this->getTableName()}`.{$field}", $this->fields)) : '*';
        $query = 'SELECT ' . $fields . ' FROM `' . $this->getTableName() . '` WHERE `' . $key . '` = :' . $key;
        $binds = [':' . $key => $value];
        $this->db->exec($query, $binds);

        return $multiple ? $this->db->getAll() : $this->db->getRow();
    }

    /**
     * @param $ID
     * @param $key
     * @param $value
     * @return bool
     */
    public function update($ID, $key, $value)
    {
        $value = $value === '' ? null : $value;
        $query = 'UPDATE `' . $this->getTableName() . '` SET `' . $key . '` = :' . $key . ' WHERE ID = :ID';
        $binds = [':' . $key => $value, ':ID' => $ID];
        return $this->db->exec($query, $binds);
    }

    /**
     * @param $key
     * @param $value
     * @return bool
     */
    public function exist($key, $value)
    {
        $keys = (array)$key;
        $values = (array)$value;
        if (count($keys) !== count($values)) {
            throw new Exception('keys and values length must be equal');
        }
        $where = implode(' AND ', array_map(fn($k) => "`$k` = :$k", $keys));
        $binds = array_combine(array_map(fn($k) => ":$k", $keys), $values);
        $query = 'SELECT 1 FROM `' . $this->getTableName() . '` WHERE ' . $where;
        $this->db->exec($query, $binds);

        return $this->db->rowCount() > 0;
    }

    /**
     * @throws Exception
     */
    public function useBehaviours()
    {
        if (!empty($this->useBehaviours) && is_array($this->useBehaviours)) {
            foreach ($this->useBehaviours as $row) {
                $path = $this->behavioursDir . '/' . $row . '.php';
                if (is_file($path)) {
                    include_once($path);
                    $this->behaviours->{$row} = new $row();
                } else {
                    throw new Exception("Problem z behaviorem $row nie istnieje lub ma złą nazwę.");
                }
            }
        }
    }

    /**
     * @param $ID
     * @param bool $recursive
     * @return bool|array
     */
    public function findByID($ID, $recursive = false)
    {
        $fields = is_array($this->fields) ? implode(',', array_map(fn($field) => "`{$this->getTableName()}`.{$field}", $this->fields)) : "`{$this->getTableName()}`.{$this->fields}";

        $joins = '';
        if ($recursive && !empty($this->hasMany)) {
            foreach ($this->hasMany as $model => $row) {
                $inst = $model::getInstance();
                $tableName = $inst->getTableName();
                $modelFields = is_array($inst->getFields()) ? implode(',', array_map(fn($field) => "`$tableName`.$field", $inst->getFields())) : "`$tableName`.{$inst->getFields()}";
                $fields .= ",$modelFields";
                $joins .= "LEFT JOIN `$tableName` ON `{$this->getTableName()}`.ID = `$tableName`." . $row['key'] . ' ';
            }
        }

        $query = "SELECT $fields FROM `{$this->getTableName()}` $joins WHERE `{$this->getTableName()}`.ID = :ID";
        $binds = [':ID' => $ID];
        $this->db->exec($query, $binds);

        return $recursive ? $this->db->getAll() : $this->db->getRow();
    }

    /**
     * @return array|bool
     */
    public function getAll()
    {
        $fields = is_array($this->fields) ? implode(',', array_map(fn($field) => "`{$this->getTableName()}`.$field", $this->fields)) : '*';
        $query = "SELECT $fields FROM `{$this->getTableName()}`";
        $this->db->exec($query);
        return $this->db->getAll();
    }

    public function getAllWithLang($langTable, $joinColumn)
    {
        $query = "SELECT t1.ID, l.name, l.slug, l.lang FROM `{$this->getTableName()}` t1 JOIN `$langTable` l ON l.$joinColumn = t1.ID";
        $this->db->exec($query);
        return $this->db->getAll();
    }

    /**
     * @param $key
     * @param $value
     * @return bool
     */
    public function delete($key, $value)
    {
        $keys = (array)$key;
        $values = (array)$value;
        if (count($keys) !== count($values)) {
            throw new Exception('keys and values length must be equal');
        }
        $where = implode(' AND ', array_map(fn($k) => "`$k` = :$k", $keys));
        $binds = array_combine(array_map(fn($k) => ":$k", $keys), $values);
        $query = 'DELETE FROM `' . $this->getTableName() . '` WHERE ' . $where;
        return $this->db->exec($query, $binds);
    }

    /**
     * @param $params array | object
     * @param bool $isAutoIncrementTable
     * @param string $idColName
     * @return bool|string
     */
    public function create($params, $isAutoIncrementTable = true, $idColName = 'ID')
    {
        if (empty($params)) {
            return false;
        }

        $incrementID = false;
        if ($isAutoIncrementTable) {
            $query = "SELECT MAX($idColName) FROM `{$this->getTableName()}` LIMIT 1";
            if ($this->db->exec($query)) {
                $incrementID = true;
                $tmpLast = $this->db->getOne();
                $tmpLast = $tmpLast === false ? 0 : $tmpLast + 1;
            }
        }

        $fields = implode(',', array_map(fn($p) => "`$p`", array_keys($params)));
        $values = implode(',', array_map(fn($p) => ":$p", array_keys($params)));
        $binds = $params;

        if ($incrementID) {
            $query = "INSERT INTO `{$this->getTableName()}` ($idColName, $fields) VALUES ('$tmpLast', $values)";
        } else {
            $tmpLast = $params[$idColName];
            $query = "INSERT INTO `{$this->getTableName()}` ($fields) VALUES ($values)";
        }

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $isAutoIncrementTable ? $tmpLast : true;
    }

    /**
     * @param $ID
     * @param $params array Updated columns
     * @param string $idColName
     * @return bool
     */
    public function updateAll($ID, $params, $idColName = 'ID')
    {
        if (empty($params)) {
            return false;
        }

        $pairs = implode(',', array_map(fn($p) => "`$p` = :$p", array_keys($params)));
        $binds = array_merge($params, [':ID' => $ID]);

        $query = "UPDATE `{$this->getTableName()}` SET $pairs WHERE $idColName = :ID";
        return $this->db->exec($query, $binds);
    }

    /**
     * @param $list
     * @return array|bool
     */
    public function getByList($list)
    {
        if (empty($list)) {
            return false;
        }

        $query = 'SELECT * FROM `' . $this->getTableName() . '` WHERE `ID` IN (' . implode(',', $list) . ')';
        $this->db->exec($query);
        $res = $this->db->getAll();

        $result = [];
        foreach ($res as $row) {
            $result[$row['ID']] = $row;
        }
        return $result;
    }

    /**
     * @return bool
     */
    public function debug()
    {
        $Debugger = new Debugger();
        $Debugger->setDebugName('model');
        return $Debugger->debug(func_get_args());
    }

    public function updateTrace()
    {
        $Debugger = new Debugger();
        return $Debugger->updateTrace();
    }

    /**
     * @return mixed
     */
    public static function getInstance()
    {
        $class = get_called_class();
        if (!isset(self::$instances[$class])) {
            self::$instances[$class] = new $class;
        } else if (isset(self::$instances[$class]) && method_exists(self::$instances[$class], 'getDb')) {
            $pdo = self::$instances[$class]->getDb();
            if (!$pdo || !method_exists($pdo, 'getStmt') || !$pdo->getStmt()) {
                self::$instances[$class] = new $class;
            }
        }
        return self::$instances[$class];
    }

    public function getNextID()
    {
        $query = 'SELECT MAX(ID) FROM `' . $this->getTableName() . '` LIMIT 1';
        if ($this->db->exec($query)) {
            $last = $this->db->getOne();
            return $last === false ? 1 : $last + 1;
        }
        return 1;
    }
}
