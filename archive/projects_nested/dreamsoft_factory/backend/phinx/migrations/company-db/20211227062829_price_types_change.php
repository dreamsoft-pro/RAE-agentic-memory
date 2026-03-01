<?php


use Phinx\Migration\AbstractMigration;

class PriceTypesChange extends AbstractMigration
{

    public function up()
    {
        $this->query("update ps_config_priceTypes set devicesType=1, `unit`='liczba' where `function` in ('cutSharp','cutClipping');");
    }
    public function down()
    {
    }
}
