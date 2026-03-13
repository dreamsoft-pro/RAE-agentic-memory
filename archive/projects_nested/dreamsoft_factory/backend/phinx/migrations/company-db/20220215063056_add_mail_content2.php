<?php


use Phinx\Migration\AbstractMigration;

class AddMailContent2 extends AbstractMigration
{

    public function up()
    {
        $ids=$this->fetchAll('select ID from dp_domains where active = 1');
        foreach ($ids as $domainID){
            $this->query("insert into dp_mail_contents (mailTypeID, domainID, lang, content) values(26,{$domainID['ID']}, 'pl', '<p>Witaj {first_name}</p><p>Została cofnięta akceptacja produktu:<br/>{product_info}<br/></p>')");
            $this->query("insert into dp_mail_titles (title, mailTypeID, domainID, lang) values('Cofnięta akceptacja produktu', 26,{$domainID['ID']}, 'pl')");
        }

    }
    public function down()
    {
        $this->query('delete from dp_mail_contents where mailTypeID=26');
        $this->query('delete from dp_mail_titles where mailTypeID=26');
    }
}
