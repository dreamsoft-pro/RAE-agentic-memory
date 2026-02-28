<?php


use Phinx\Migration\AbstractMigration;

class AddMailContent extends AbstractMigration
{

    public function up()
    {
        $ids=$this->fetchAll('select ID from dp_domains where active = 1');
        foreach ($ids as $domainID){
            $this->query("insert into dp_mail_contents (mailTypeID, domainID, lang, content) values(24,{$domainID['ID']}, 'pl', '<p>Witaj {firstName}</p><p>Dodano raport do akceptacji:<br/>{files_info}<br/></p>')");
            $this->query("insert into dp_mail_titles (title, mailTypeID, domainID, lang) values('Dodano nowy raport', 24,{$domainID['ID']}, 'pl')");
            $this->query("insert into dp_mail_contents (mailTypeID, domainID, lang, content) values(25,{$domainID['ID']}, 'pl', '<p>Użytkownik {userName} zatwierdził raport</p><p>{files_info}</p>')");
            $this->query("insert into dp_mail_titles (title, mailTypeID, domainID, lang) values('Klient zaakceptował raport', 25,{$domainID['ID']}, 'pl')");
        }

    }
    public function down()
    {
        $this->query('');
    }
}
