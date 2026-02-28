<?php


use Phinx\Migration\AbstractMigration;

class DevicesExtraSettings extends AbstractMigration
{

    public function up()
    {
        $this->query("ALTER TABLE `dp_devices` ADD `multiOperator` TINYINT(1) NULL DEFAULT NULL AFTER `stiffnessMax`, ADD `multiProcess` TINYINT(1) NULL DEFAULT NULL AFTER `multiOperator`, ADD `defaultPath` TINYINT(1) NULL DEFAULT NULL AFTER `multiProcess`;");
        $this->query("ALTER TABLE `dp_ongoingLogs` ADD `asAdditionalOperator` TINYINT(1) NULL DEFAULT NULL AFTER `customPause`;");

    }
    public function down()
    {
        //
    }
}
