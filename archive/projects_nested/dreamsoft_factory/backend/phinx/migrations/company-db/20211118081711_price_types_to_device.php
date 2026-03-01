<?php


use Phinx\Migration\AbstractMigration;

class PriceTypesToDevice extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_priceTypes
add column devicesType tinyint null');
        $this->query('update ps_config_priceTypes
set devicesType=1 where ID in (1,2,3,4,5,19,22,43)');
    }
    public function down()
    {
        $this->query('alter table ps_config_priceTypes drop column devicesType');
    }
}
