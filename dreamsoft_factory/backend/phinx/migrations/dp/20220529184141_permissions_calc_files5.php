<?php


use Phinx\Migration\AbstractMigration;

class PermissionsCalcFiles5 extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'post_cropImage', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'post_restoreImage', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
