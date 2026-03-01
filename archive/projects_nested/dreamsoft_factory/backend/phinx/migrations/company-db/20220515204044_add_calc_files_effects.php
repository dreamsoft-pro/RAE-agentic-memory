<?php


use Phinx\Migration\AbstractMigration;

class AddCalcFilesEffects extends AbstractMigration{

    public function up()
    {
        $this->query('alter table dp_calcFiles add column isBW int not null default 0');
        $this->query('alter table dp_calcFiles add column isSepia int not null default 0');
    }
    public function down()
    {
        $this->query('alter table dp_calcFiles drop column isBW');
        $this->query('alter table dp_calcFiles drop column isSepia');
    }
}
