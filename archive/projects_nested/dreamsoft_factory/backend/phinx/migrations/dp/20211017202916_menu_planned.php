<?php


use Phinx\Migration\AbstractMigration;

class MenuPlanned extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_subMenu` (`menuID`, `key`, `controller`, `action`, `package`, `path`, `title`, `active`) VALUES
(4, 'production_planned', 'Menu', 'ordersProductionPlanned', NULL, 'orders/productionPlanned/', 'production_planned', 1);");
    }
    public function down()
    {
        //can be rolled back manually
    }
}
