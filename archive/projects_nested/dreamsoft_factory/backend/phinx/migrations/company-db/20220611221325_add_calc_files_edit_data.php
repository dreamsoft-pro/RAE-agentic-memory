<?php


use Phinx\Migration\AbstractMigration;

class AddCalcFilesEditData extends AbstractMigration{

    public function up()
    {
        $this->query('alter table dp_calcFiles add column editData varchar(512) null');
    }
    public function down()
    {
        $this->query('alter table dp_calcFiles drop column editData');
    }
}
