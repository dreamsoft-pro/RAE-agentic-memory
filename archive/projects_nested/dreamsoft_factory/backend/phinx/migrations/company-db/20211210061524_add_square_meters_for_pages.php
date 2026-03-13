<?php


use Phinx\Migration\AbstractMigration;

class AddSquareMetersForPages extends AbstractMigration
{

    public function up()
    {
        $this->query('update ps_config_priceTypes
set devicesType=1 where `function`="squareMetersForPages";');
    }
    public function down()
    {
        $this->query('update ps_config_priceTypes
set devicesType=0 where `function`="squareMetersForPages";');
    }
}
