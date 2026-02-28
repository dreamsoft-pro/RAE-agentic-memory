<?php


use Phinx\Migration\AbstractMigration;

class PermissionsDpCartsData extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'DpCartsData', 'index', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'DpCartsData', 'post_index', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'DpCartsData', 'patch_index', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'DpCartsData', 'post_updateAddresses', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'DpCartsData', 'patch_updateAddresses', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'DpCartsData', 'post_joinAddresses', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
