<?php


use Phinx\Migration\AbstractMigration;

class AddWeightPriceTypes extends AbstractMigration
{

    public function up()
    {
        $this->query("insert into ps_config_priceTypes(`order`,name,`function`,unit,devicesType) values
                        (37,'Waga paczki','packageWeight','kg',1),(38,'Waga','weight','kg',1)");
    }

    public function down()
    {
        $this->query("delete from ps_config_priceTypes where `function`='packageWight' or `function`='weight';");
    }
}
