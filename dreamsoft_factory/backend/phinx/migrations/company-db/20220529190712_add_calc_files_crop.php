<?php


use Phinx\Migration\AbstractMigration;

class AddCalcFilesCrop extends AbstractMigration{

    public function up()
    {
        $this->query('alter table dp_calcFiles add column isCropped int not null default 0');
    }
    public function down()
    {
        $this->query('alter table dp_calcFiles drop column isCropped');
    }
}
