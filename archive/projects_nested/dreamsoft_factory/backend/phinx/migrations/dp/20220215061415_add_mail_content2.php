<?php


use Phinx\Migration\AbstractMigration;

class AddMailContent2 extends AbstractMigration
{

    public function up()
    {
        $this->query("insert into dp_mail_types(ID,`key`) values (26,'productRejected')");
        $this->query("insert into dp_mail_typeLangs(mailTypeID,lang,name) values (26,'pl', 'Produkt odrzucony')");
        $this->query("insert into dp_mail_typeLangs(mailTypeID,lang,name) values (26,'en', 'Product rejected')");
        $this->query("insert into dp_mail_variables(mailTypeID,`variable`) values (26,'product_info')");
        $id=$this->getAdapter()->getConnection()->lastInsertId();
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'pl','Informacja o produkcie')");
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'en','Product details')");
        $this->query("insert into dp_mail_variables(mailTypeID,`variable`) values (26,'first_name')");
        $id=$this->getAdapter()->getConnection()->lastInsertId();
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'pl','Imię użytkownika')");
        $this->query("insert into dp_mail_variableLangs(variableID,lang,`desc`) values ($id,'en','User name')");
    }
    public function down()
    {
        $this->query('delete from dp_mail_types where ID = 26');
        $this->query('delete from dp_mail_typeLangs where mailTypeID = 26');
        $this->query('delete from dp_mail_variables where mailTypeID = 26');
    }
}
