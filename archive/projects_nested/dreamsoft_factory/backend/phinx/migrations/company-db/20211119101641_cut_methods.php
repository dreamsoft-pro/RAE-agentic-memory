<?php


use Phinx\Migration\AbstractMigration;

class CutMethods extends AbstractMigration
{

    public function up()
    {
        $this->query("insert into ps_config_priceTypes (`name`,`function`) values('Cięcie na ostro','cutSharp'),('Cięcie z wycinką','cutClipping')");
    }
    public function down()
    {
        $this->query("delete from ps_config_priceTypes where function in('cutSharp','cutClipping')");
    }
}
