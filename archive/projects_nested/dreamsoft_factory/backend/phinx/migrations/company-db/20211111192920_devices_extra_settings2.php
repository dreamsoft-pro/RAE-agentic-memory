<?php


use Phinx\Migration\AbstractMigration;

class DevicesExtraSettings2 extends AbstractMigration
{

    public function up()
    {
        $this->query("ALTER TABLE `dp_devices` ADD `countAdditionalOperation` TINYINT(1) NULL DEFAULT NULL AFTER `defaultPath`;");
    }
    public function down()
    {
        //
    }
}
