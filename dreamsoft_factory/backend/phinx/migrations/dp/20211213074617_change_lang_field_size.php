<?php


use Phinx\Migration\AbstractMigration;

class ChangeLangFieldSize extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_langs change column `value` `value` varchar(5000) not null');
    }
    public function down()
    {
    }
}
