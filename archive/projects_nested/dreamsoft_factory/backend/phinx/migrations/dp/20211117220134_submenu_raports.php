<?php


use Phinx\Migration\AbstractMigration;

class SubmenuRaports extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_subMenu` (`menuID`, `key`, `controller`, `action`, `package`, `path`, `title`, `active`) VALUES
            (8, 'production-raports', 'Menu', 'ordersProductionRaports', NULL, 'orders/productionRaports/', 'production-raports', 1);");        
    }
    public function down()
    {
        //can be rolled back manually
    }
}
