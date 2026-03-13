<?php


use Phinx\Migration\AbstractMigration;

class PermissionsMultiOffer extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'DpOrders', 'post_changeMultiOffer', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
