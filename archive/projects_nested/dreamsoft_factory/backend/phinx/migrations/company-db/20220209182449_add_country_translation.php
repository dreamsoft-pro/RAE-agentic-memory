<?php


use Phinx\Migration\AbstractMigration;

class AddCountryTranslation extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_countries add column name_de varchar(255) null');
    }
    public function down()
    {
        $this->query('alter table dp_countries drop column name_de');
    }
}
