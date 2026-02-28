<?php

/**
 * Description of DpOrderStatus
 *
 * @author Rafał
 */

namespace DreamSoft\Models\Order;

use DreamSoft\Core\Model;
use DreamSoft\Models\Behaviours\LangFilter;

class OrderStatus extends Model
{

    protected $orderStatusLang;
    private $domainID;

    /**
     * @var LangFilter
     */
    private $LangFilter;


    /**
     * OrderStatus constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->setTableName('orderStatuses', true);
        $this->orderStatusLang = $this->prefix . 'orderStatusLangs';

        $this->LangFilter = new LangFilter();
    }

    /**
     * @param int $domainID
     */
    public function setDomainID($domainID)
    {
        $this->domainID = $domainID;
    }

    /**
     * @return int
     */
    public function getDomainID()
    {
        return $this->domainID;
    }

    /**
     * @param bool $active If true, only active statuses will be returned.
     * @param bool $onlyForDomain If true, filters the results to the current domain by using the domain ID.
     * @return bool|array Returns an array of order statuses with language data if successful, or false on failure.
     */
    public function getAll($active = false, $onlyForDomain = false)
    {
        $query = ' SELECT so.*, GROUP_CONCAT( DISTINCT CONCAT_WS("::", osl.lang, osl.name) SEPARATOR "||") AS langs FROM `' . $this->getTableName() . '` AS so ';
        $query .= ' LEFT JOIN `' . $this->orderStatusLang . '` as osl ON osl.statusID = so.ID ';
        $binds = array();

        if ($onlyForDomain) {
            $query .= ' WHERE so.`domainID` = :domainID ';
            $binds['domainID'] = $this->getDomainID();

            if ($active) {
                $query .= ' AND so.`active` = 1 ';
            }
        } elseif ($active) {
            $query .= ' WHERE so.`active` = 1 ';
        }




        $query .= ' GROUP BY so.ID ';

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getAll();
        return $this->LangFilter->splitFlatArray($res, 'langs');
    }

    /**
     * @param $ID
     * @return array|bool
     */
    public function getOne($ID)
    {
        $query = ' SELECT so.*, GROUP_CONCAT( DISTINCT CONCAT_WS("::", osl.lang, osl.name)) AS langs FROM `' . $this->getTableName() . '` AS so ';
        $query .= ' LEFT JOIN `' . $this->orderStatusLang . '` as osl ON osl.statusID = so.ID ';
        $query .= ' WHERE so.`ID` = :ID GROUP BY so.ID ';

        $binds['ID'] = $ID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->getRow();
    }

    /**
     * @param $statuses
     * @return bool|array
     */
    public function sort($statuses)
    {
        $result = true;
        foreach ($statuses as $index => $ID) {
            if (empty($ID)) {
                continue;
            }

            $query = 'UPDATE `' . $this->getTableName() . '` SET `sort` = :index WHERE `ID` = :ID ';

            $binds['ID'] = array($ID, 'int');
            $binds['index'] = $index;
            if (!$this->db->exec($query, $binds)) {
                $result = false;
            }
        }
        return $result;
    }

    /**
     * @param bool $onlyForDomain If true, filters the results to the current domain by using the domain ID.
     * @return bool|array
     */
    public function getFirstStatus($onlyForDomain=False)
    {
        $binds = array();
        $query = 'SELECT ID AS firstStatus
            FROM  `' . $this->getTableName() . '` AS so
            WHERE so.`type` = 1';

        if($onlyForDomain){
            $query .= ' AND so.`domainID` = :domainID';
            $binds['domainID'] = $this->getDomainID();
        }
        $query .= ' LIMIT 1';

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->getOne();
    }

    /**
     * @return bool|array
     */
    public function getMaxOrder()
    {
        $binds = array();
        $query = 'SELECT MAX(sort)
            FROM  `' . $this->getTableName() . '` AS so
            WHERE so.`active` = 1 
            LIMIT 1';

        if (!$this->db->exec($query, $binds)) {
            return false;
        }
        return $this->db->getOne();
    }

}
