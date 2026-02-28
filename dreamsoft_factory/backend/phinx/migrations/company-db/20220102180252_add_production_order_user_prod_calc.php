<?php


use Phinx\Migration\AbstractMigration;

class AddProductionOrderUserProdCalc extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_products add column productionOrder int null');
    }
    public function down()
    {
        $this->query('alter table dp_products drop column productionOrder');
    }
}
