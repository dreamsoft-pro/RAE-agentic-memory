<?php


use Phinx\Migration\AbstractMigration;

class CalcFilesAddOriginalFilename extends AbstractMigration {

    public function up()
    {
        $this->query('alter table dp_calcFiles add column originalFileName varchar(255) not null');
    }
    public function down()
    {
        $this->query('alter table dp_calcFiles drop column originalFileName');
    }
}
