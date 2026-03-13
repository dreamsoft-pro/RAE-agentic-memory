<?php


use Phinx\Migration\AbstractMigration;

class AdditionalOperation extends AbstractMigration
{

    public function up()
    {
        $this->query("CREATE TABLE `dp_additional_operation` (
          `ID` int(11) NOT NULL auto_increment primary key,
          `ongoingID` int(11) NOT NULL,
          `operationName` varchar(200) DEFAULT NULL,
          `operationDesc` varchar(200) NOT NULL,
          `calculateTime` int(11) NOT NULL,
          `inProgress` int(11) NOT NULL DEFAULT '0',
          `state` int(11) NOT NULL DEFAULT '0',
          `operatorID` int(11) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;");

    }
    public function down()
    {
        $this->query('drop table dp_additional_operation;');
    }
}
