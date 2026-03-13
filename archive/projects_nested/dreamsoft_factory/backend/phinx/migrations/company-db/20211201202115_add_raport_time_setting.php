<?php


use Phinx\Migration\AbstractMigration;

class AddRaportTimeSetting extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_settings` (`ID`, `module`, `key`, `value`, `lang`, `domainID`) VALUES (NULL, 'productionPath', 'raportTimeDayStart', '00:00', NULL, NULL);");
        $this->query("INSERT INTO `dp_settings` (`ID`, `module`, `key`, `value`, `lang`, `domainID`) VALUES (NULL, 'productionPath', 'raportTimeDayEnd', '23:59', NULL, NULL);");

    }
    public function down()
    {
        //
    }
}
