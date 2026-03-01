<?php


use Phinx\Migration\AbstractMigration;

class AddRepeatedOperationsCount extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_options add column repeatedOperationsCount int not null default 1');
    }
    public function down()
    {
        $this->query('alter table ps_config_options drop column repeatedOperationsCount');
    }
}
