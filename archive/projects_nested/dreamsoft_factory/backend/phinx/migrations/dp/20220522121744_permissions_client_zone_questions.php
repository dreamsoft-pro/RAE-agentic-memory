<?php


use Phinx\Migration\AbstractMigration;

class PermissionsClientZoneQuestions extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'CustomProducts', 'CustomProducts', 'getPublic', '1');");
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'CustomProducts', 'CustomProducts', 'publicCount', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
