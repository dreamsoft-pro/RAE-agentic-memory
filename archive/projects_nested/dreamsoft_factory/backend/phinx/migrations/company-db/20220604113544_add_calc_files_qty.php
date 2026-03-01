<?php


use Phinx\Migration\AbstractMigration;

class AddCalcFilesQty extends AbstractMigration{

    public function up()
    {
        $this->query('alter table dp_calcFiles add column qty int not null default 1');
    }
    public function down()
    {
        $this->query('alter table dp_calcFiles drop column qty');
    }
}
