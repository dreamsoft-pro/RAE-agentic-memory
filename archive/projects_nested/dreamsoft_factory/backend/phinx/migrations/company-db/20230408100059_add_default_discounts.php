<?php


use Phinx\Migration\AbstractMigration;

class AddDefaultDiscounts extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_discountGroups add column `default` int not null default 0');
    }
    public function down()
    {
        $this->query('alter table ps_discountGroups drop column `default`');
    }
}
