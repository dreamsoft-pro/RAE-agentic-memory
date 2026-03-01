<?php


use Phinx\Migration\AbstractMigration;

class PermissionsCalcFiles2 extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'filesSet', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'createGuestSet', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
