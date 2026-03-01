<?php


use Phinx\Migration\AbstractMigration;

class PermissionsCalcFiles7 extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'patch_changeQty', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
