<?php


use Phinx\Migration\AbstractMigration;

class ChangeDefaultAttributeNature extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_attributes change column natureID natureID int null');
        $this->query('alter table ps_config_attributeNatures drop column name');
        $this->query('update ps_config_attributes set natureID=null');
    }
    public function down()
    {
    }
}
