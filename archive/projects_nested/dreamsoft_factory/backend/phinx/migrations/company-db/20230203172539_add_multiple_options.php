<?php


use Phinx\Migration\AbstractMigration;

class AddMultipleOptions extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_attributes add column multipleOptionsMax int not null default 0  after rangeID');
    }
    public function down()
    {
        $this->query('alter table ps_config_attributes drop column multipleOptionsMax');
    }
}
