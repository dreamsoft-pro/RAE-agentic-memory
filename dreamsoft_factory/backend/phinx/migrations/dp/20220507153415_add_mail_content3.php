<?php


use Phinx\Migration\AbstractMigration;

class AddMailContent3 extends AbstractMigration
{

    public function up()
    {
        $this->query("insert into dp_mail_variables(mailTypeID,`variable`) values (5,'##')");
        $id=$this->getAdapter()->getConnection()->lastInsertId();
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'pl','Treść nie będzie wyświetlana przy ofercie wielonakładowej')");
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'en','The content will not be displayed for a multi-sale offer')");
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'de','Der Inhalt wird bei einem Multi-Sale-Angebot nicht angezeigt')");
    }
    public function down()
    {
        
    }
}
