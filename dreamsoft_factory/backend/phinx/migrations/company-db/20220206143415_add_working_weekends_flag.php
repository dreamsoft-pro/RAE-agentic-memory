<?php


use Phinx\Migration\AbstractMigration;

class AddWorkingWeekendsFlag extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_devices
                            add column worksInSaturday int null,
                            add column worksInSunday int null');
    }

    public function down()
    {
        $this->query('alter table dp_devices 
                            drop column worksInSaturday, 
                            drop column worksInSunday');
    }
}
