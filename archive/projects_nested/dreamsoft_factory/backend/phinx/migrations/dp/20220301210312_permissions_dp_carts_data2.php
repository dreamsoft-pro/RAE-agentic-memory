<?php


use Phinx\Migration\AbstractMigration;

class PermissionsDpCartsData2 extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'DpCartsData', 'post_getUserCart', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
