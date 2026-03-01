<?php


use Phinx\Migration\AbstractMigration;

class AddCuttingDiesFile extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_attributes 
                    change column specialFunction specialFunction enum("rotation","rounding", "cuttingDie") null');
    }
    public function down()
    {
        $this->query('alter table ps_config_attributes 
                    change column specialFunction specialFunction enum("rotation","rounding") null');
    }
}
