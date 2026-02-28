<?php


use Phinx\Migration\AbstractMigration;

class NewMenu extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_menu` (`ID`, `key`, `desc`, `super`, `title`, `active`) VALUES
(8, 'production', NULL, 0, 'production', 1);");
        $this->query("INSERT INTO `dp_subMenu` (`ID`, `menuID`, `key`, `controller`, `action`, `package`, `path`, `title`, `active`) VALUES
(60, 8, 'production-settings', 'Menu', 'customerServiceRegister', NULL, 'customerservice/customerservice-register', 'settings', 1),
(61, 8, 'production-planning', 'Menu', 'customerServiceRegister', NULL, 'customerservice/customerservice-register', 'planning', 1),
(62, 8, 'production-path', 'Menu', 'ordersProductionPath', NULL, 'orders/productionPath/', 'production_path', 1),
(63, 8, 'production-operators', 'Menu', 'ordersOperators', NULL, 'orders_operators', 'operators', 1);");
    }
    public function down()
    {
        //can be rolled back manually
    }
}
