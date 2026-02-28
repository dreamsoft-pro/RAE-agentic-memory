<?php
namespace DreamSoft\Models\Order;


use DreamSoft\Core\Model;


class DpCalcFileSet extends Model
{
    protected $userTable;

    public function __construct()
    {
        parent::__construct();
        $this->setTableName('calcFilesSets', true);
    }

    public function getByParams($userID, $typeID, $calcID)
    {
        $query = 'SELECT * FROM dp_calcFilesSets WHERE `userID` = :userID AND `typeID` = :typeID AND `calcID` = :calcID;';

        $binds['userID'] = $userID;
        $binds['typeID'] = $typeID;
        $binds['calcID'] = $calcID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        $res = $this->db->getRow();
        if( !$res ) {
            return false;
        }
        return $res;
    }

    public function count($setID)
    {
        $query = 'SELECT COUNT(`dp_calcFiles`.`ID`) as count '
            . ' FROM `dp_calcFiles` '
            . ' WHERE `dp_calcFiles`.calcFilesSetID = :setID';

        $binds['setID'] = $setID;

        $query .= ' GROUP BY `dp_calcFiles`.ID ';

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->rowCount();
    }

}
