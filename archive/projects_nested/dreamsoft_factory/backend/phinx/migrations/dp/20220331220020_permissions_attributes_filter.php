<?php


use Phinx\Migration\AbstractMigration;

class PermissionsAttributesFilter extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_permissions` (`ID`, `desc`, `package`, `controller`, `action`, `default`) VALUES (NULL, NULL, 'printshop_config', 'Attributes', 'post_attributeFilters', '1');");
    }
    public function down()
    {
        // rollback manually
    }
}
