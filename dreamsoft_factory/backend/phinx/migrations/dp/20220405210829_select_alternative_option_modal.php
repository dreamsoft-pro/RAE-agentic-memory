<?php


use Phinx\Migration\AbstractMigration;

class SelectAlternativeOptionModal extends AbstractMigration
{

    public function up()
    {
        $this->query('insert into dp_templates (name,fileName,created, useVariables) values("select-alternative-option-modal","select-alternative-option-modal", now(),0);');
    }
    public function down()
    {
        $this->query('delete from dp_templates where name="select-alternative-option-modal"');
    }
}

