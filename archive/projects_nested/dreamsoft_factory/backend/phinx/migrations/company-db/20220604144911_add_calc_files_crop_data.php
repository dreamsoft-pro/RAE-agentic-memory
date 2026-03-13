<?php


use Phinx\Migration\AbstractMigration;

class AddCalcFilesCropData extends AbstractMigration{

    public function up()
    {
        $this->query('alter table dp_calcFiles add column cropData varchar(512) null');
    }
    public function down()
    {
        $this->query('alter table dp_calcFiles drop column cropData');
    }
}
