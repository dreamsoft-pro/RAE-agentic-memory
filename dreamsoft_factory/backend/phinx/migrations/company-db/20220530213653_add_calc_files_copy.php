<?php


use Phinx\Migration\AbstractMigration;

class AddCalcFilesCopy extends AbstractMigration{

    public function up()
    {
        $this->query('alter table dp_calcFiles add column copyOf int not null default 0');
    }
    public function down()
    {
        $this->query('alter table dp_calcFiles drop column copyOf');
    }
}
