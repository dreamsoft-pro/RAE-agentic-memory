<?php


use Phinx\Migration\AbstractMigration;

class OngoingProgressOperatorAdd extends AbstractMigration
{

    public function up()
    {
        $this->query("ALTER TABLE `dp_ongoingProgress` ADD `operatorID` INT(10) NULL DEFAULT NULL AFTER `created`;");
        $this->query("ALTER TABLE `dp_devices` ADD `runningTasksAlert` TINYINT(1) NULL DEFAULT NULL AFTER `countAdditionalOperation`;");

    }
    public function down()
    {
        //
    }
}
