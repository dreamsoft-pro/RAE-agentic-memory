<?php


use Phinx\Migration\AbstractMigration;

class AddGanttScaleSetting extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_settings` (`ID`, `module`, `key`, `value`, `lang`, `domainID`) VALUES (NULL, 'productionPath', 'defaultGanttScale', 'hour', NULL, NULL);");

    }
    public function down()
    {
        //
    }
}
