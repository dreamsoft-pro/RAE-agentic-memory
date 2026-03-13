<?php


use Phinx\Migration\AbstractMigration;

class AddTemplateFrontPrintPDF extends AbstractMigration
{

    public function up()
    {
        $this->query('insert into dp_templates (name,fileName,created, useVariables) values("print-attribute-details","print-attribute-details", now(),0);');
    }
    public function down()
    {
        $this->query('delete from dp_templates where name="print-attribute-details"');
    }
}

