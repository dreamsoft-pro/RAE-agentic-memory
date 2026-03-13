<?php


use Phinx\Migration\AbstractMigration;

class AddDefaultTimeOperation extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_devices
                            add column defaultOperationTime int null');
    }

    public function down()
    {
        $this->query('alter table dp_devices 
                            drop column defaultOperationTime');
    }
}
