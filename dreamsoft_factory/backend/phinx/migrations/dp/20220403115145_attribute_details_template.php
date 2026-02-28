<?php


use Phinx\Migration\AbstractMigration;

class AttributeDetailsTemplate extends AbstractMigration
{

    public function up()
    {
        $this->query('insert into dp_templates (name,fileName,created, useVariables) values("attribute-details","attribute-details", now(),0);');
    }
    public function down()
    {
        $this->query('delete from dp_templates where name="attribute-details"');
    }
}

