<?php


use Phinx\Migration\AbstractMigration;

class PermissionsCalcFiles4 extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'post_setImageSepia', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'post_setCollectionToBW', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'post_setCollectionToSepia', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'orders', 'calcFilesUploader', 'post_removeCollectionFilters', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
