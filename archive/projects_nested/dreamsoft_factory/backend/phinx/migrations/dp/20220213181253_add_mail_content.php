<?php


use Phinx\Migration\AbstractMigration;

class AddMailContent extends AbstractMigration
{

    public function up()
    {
        $this->query("insert into dp_mail_types(ID,`key`) values (24,'newReportToClient')");
        $this->query("insert into dp_mail_typeLangs(mailTypeID,lang,name) values (24,'pl', 'Dodany nowy raport')");
        $this->query("insert into dp_mail_typeLangs(mailTypeID,lang,name) values (24,'en', 'New report add')");
        $this->query("insert into dp_mail_variables(mailTypeID,`variable`) values (24,'files_info')");
        $id=$this->getAdapter()->getConnection()->lastInsertId();
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'pl','Informacja o plikach')");
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'en','Files description')");
        $this->query("insert into dp_mail_variables(mailTypeID,`variable`) values (24,'firstName')");
        $id=$this->getAdapter()->getConnection()->lastInsertId();
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'pl','Imię użytkownika')");
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'en','User name')");
        $this->query("insert into dp_mail_types(ID,`key`) values (25,'reportAcceptedToPrinthouse')");
        $this->query("insert into dp_mail_typeLangs(mailTypeID,lang,name) values (25,'pl', 'Raport zaakceptowany - dla drukarni')");
        $this->query("insert into dp_mail_typeLangs(mailTypeID,lang,name) values (25,'en', 'Report accepted - for printhouse')");
        $this->query("insert into dp_mail_variables(mailTypeID,`variable`) values (25,'files_info')");
        $id=$this->getAdapter()->getConnection()->lastInsertId();
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'pl','Informacja o plikach')");
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'en','Files description')");
        $this->query("insert into dp_mail_variables(mailTypeID,`variable`) values (25,'userName')");
        $id=$this->getAdapter()->getConnection()->lastInsertId();
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'pl','Imię i nazwisko użytkownika')");
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'en','User full name')");
    }
    public function down()
    {
        $this->query('delete from dp_mail_types where ID in(24,25)');
        $this->query('delete from dp_mail_typeLangs where mailTypeID in(24,25)');
        $this->query('delete from dp_mail_variables where mailTypeID in(24,25)');
    }
}
