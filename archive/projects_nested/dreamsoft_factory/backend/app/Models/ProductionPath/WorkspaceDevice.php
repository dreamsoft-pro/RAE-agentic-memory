<?php

namespace DreamSoft\Models\ProductionPath;

use DreamSoft\Core\Model;

class WorkspaceDevice extends Model
{

    public function __construct()
    {
        parent::__construct();
        $prefix = true;
        $this->setTableName('workspacesDevices', $prefix);
    }
    public function getByWorkspaceID($workspaceID)
    {
        $query = 'SELECT deviceID FROM `dp_workspacesDevices` '
            . ' WHERE `workspaceID` = :workspaceID ';

        $binds[':workspaceID'] = $workspaceID;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();
    }
}

?>
