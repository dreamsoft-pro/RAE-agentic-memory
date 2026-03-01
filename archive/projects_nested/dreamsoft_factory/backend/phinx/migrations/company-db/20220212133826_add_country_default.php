<?php


use Phinx\Migration\AbstractMigration;

class AddCountryDefault extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_countries add column isDefault int not null default 0');
    }
    public function down()
    {
        $this->query('alter table dp_countries drop column isDefault');
    }
}
