<?php


use Phinx\Migration\AbstractMigration;

class AddDevicePlannedTime extends AbstractMigration
{

    public function up()
    {
        $this->query("ALTER TABLE `dp_devices` ADD `operationPlannedTime` TINYINT(1) NULL DEFAULT NULL AFTER `runningTasksAlert`;");

    }
    public function down()
    {
        //
    }
}
