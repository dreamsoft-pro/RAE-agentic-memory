<?php


use Phinx\Migration\AbstractMigration;

class AddFunctionalAtribute extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_attributes add column specialFunction enum("rotation","rounding") null');
    }
    public function down()
    {
        $this->query('alter table ps_config_attributes drop column specialFunction');
    }
}
