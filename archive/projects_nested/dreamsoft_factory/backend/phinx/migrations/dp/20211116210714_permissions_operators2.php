<?php


use Phinx\Migration\AbstractMigration;

class PermissionsOperators2 extends AbstractMigration
{

    public function up()
    {
        //$this->query("INSERT IGNORE INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'ProductionPath', 'Devices', 'patch_move', '0');"); -> already in table
        $row = $this->fetchRow("SELECT * FROM `dp_permissions` WHERE `package` = 'ProductionPath' 
            AND `controller` = 'Devices' AND `action` = 'patch_move';");
        if( $row['ID'] > 0 ) {
            $this->query("INSERT INTO `dp_rolePerms` (`roleID`, `permID`) VALUES ('37', '".$row['ID']."');");
        }
        
    }
    public function down()
    {
        //can be rolled back manually
    }
}
