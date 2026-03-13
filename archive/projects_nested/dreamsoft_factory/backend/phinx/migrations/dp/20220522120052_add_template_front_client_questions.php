<?php


use Phinx\Migration\AbstractMigration;

class AddTemplateFrontClientQuestions extends AbstractMigration
{

    public function up()
    {
        $this->query('insert into dp_templates (name,fileName,created, useVariables) values("client-zone-questions","client-zone-questions", now(),0);');
    }
    public function down()
    {
        $this->query('delete from dp_templates where name="client-zone-questions"');
    }
}

