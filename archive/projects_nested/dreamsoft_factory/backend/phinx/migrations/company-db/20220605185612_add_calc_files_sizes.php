<?php


use Phinx\Migration\AbstractMigration;

class AddCalcFilesSizes extends AbstractMigration{

    public function up()
    {
        $this->query('alter table dp_calcFiles add column width int not null default 0');
        $this->query('alter table dp_calcFiles add column height int not null default 0');
    }
    public function down()
    {
        $this->query('alter table dp_calcFiles drop column width');
        $this->query('alter table dp_calcFiles drop column height');
    }
}
