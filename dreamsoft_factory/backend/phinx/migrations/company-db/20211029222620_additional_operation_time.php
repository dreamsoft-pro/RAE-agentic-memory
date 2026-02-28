<?php


use Phinx\Migration\AbstractMigration;

class AdditionalOperationTime extends AbstractMigration
{

    public function up()
    {
        $this->query("CREATE TABLE `dp_additionalOperationLogs` (
            `ID` int(11) NOT NULL auto_increment primary key,
            `additionalOperationID` int(11) NOT NULL,
            `state` tinyint(3) NOT NULL,
            `date` datetime NOT NULL,
            `operatorID` int(11) NOT NULL,
            `executiveUserID` int(11) NOT NULL,
            `pauseID` int(11) DEFAULT NULL,
            `customPause` varchar(50) DEFAULT NULL
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8;");

    }
    public function down()
    {
        $this->query('drop table dp_additionalOperationLogs;');
    }
}
