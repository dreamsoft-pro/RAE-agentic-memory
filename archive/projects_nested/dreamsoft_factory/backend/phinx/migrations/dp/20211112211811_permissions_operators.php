<?php


use Phinx\Migration\AbstractMigration;

class PermissionsOperators extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'ProductionPath', 'Ongoings', 'alreadyStartedTasks', '0');");
        $row = $this->fetchRow("SELECT * FROM `dp_permissions` WHERE `package` = 'ProductionPath' 
            AND `controller` = 'Ongoings' AND `action` = 'alreadyStartedTasks';");
        if( $row['ID'] > 0 ) {
            $this->query("INSERT INTO `dp_rolePerms` (`roleID`, `permID`) VALUES ('37', '".$row['ID']."');");
        }
        
    }
    public function down()
    {
        //can be rolled back manually
    }
}
