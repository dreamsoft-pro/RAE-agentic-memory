<?php


use Phinx\Migration\AbstractMigration;

class AddAttributeNature extends AbstractMigration
{

    public function up()
    {
        $this->query('create table ps_config_attributeNatures(
                        ID int not null primary key,
                        name varchar(50) not null unique ,
                        `function` varchar(50) not null unique
);');
        $this->query("insert into ps_config_attributeNatures (ID, name, `function`) values (1,'materiał','material'),(2,'usługa','service'),(3,'inne','another')");
        $this->query('alter table ps_config_attributes
                        add column natureID int not null default 1 after `type`,
                        add foreign key (natureID) references ps_config_attributeNatures(ID)
');
    }

    public function down()
    {
        $this->query('drop  table if exists ps_config_attributeNatures');
        $this->query('alter table ps_config_attributes drop column if exists natureID');
    }
}
