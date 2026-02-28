<?php


use Phinx\Migration\AbstractMigration;

class PermissionsCalcFiles8 extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'post_editImage', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
