<?php


use Phinx\Migration\AbstractMigration;

class AddServicesData extends AbstractMigration
{

    public function up()
    {
        $this->query("alter table dp_device_services add column dayOfMonth int(2) NULL;");
        $this->query("alter table dp_device_services add column month int(2) NULL;");
        $this->query("alter table dp_device_services add column dayOfWeek int(2) NULL;");
    }
    public function down()
    {
        $this->query('alter table dp_device_services drop column dayOfMonth');
        $this->query('alter table dp_device_services drop column month');
        $this->query('alter table dp_device_services drop column dayOfWeek');
    }
}
