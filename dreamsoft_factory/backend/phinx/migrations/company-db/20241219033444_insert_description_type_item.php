<?php


use Phinx\Migration\AbstractMigration;

class InsertDescriptionTypeItem extends AbstractMigration
{

    public function up()
    {
        $this->query('insert into descriptionTypes(ID, name, viewEverywhere) values(8, "Opis SEO",1)');
    }

    public function down()
    {
        $this->query('delete from descriptionTypes where ID = 8');
    }
}
