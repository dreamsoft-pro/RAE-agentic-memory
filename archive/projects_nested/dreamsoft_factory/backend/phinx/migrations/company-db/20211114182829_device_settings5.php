<?php


use Phinx\Migration\AbstractMigration;

class DeviceSettings5 extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_devices change column workUnit workUnit varchar(20) not null default \'sheet\'');
    }
    public function down()
    {

    }
}
