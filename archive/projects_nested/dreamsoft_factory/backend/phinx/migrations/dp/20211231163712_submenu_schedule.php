<?php


use Phinx\Migration\AbstractMigration;

class SubmenuSchedule extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_subMenu` (`menuID`, `key`, `controller`, `action`, `package`, `path`, `title`, `active`) VALUES
            (8, 'production-schedule', 'Menu', 'ordersProductionSchedule', NULL, 'orders/productionSchedule/', 'production-schedule', 1);");        
    }
    public function down()
    {
        //can be rolled back manually
    }
}
