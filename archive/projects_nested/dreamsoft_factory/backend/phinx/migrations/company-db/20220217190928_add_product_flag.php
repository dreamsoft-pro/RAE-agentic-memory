<?php


use Phinx\Migration\AbstractMigration;

class AddProductFlag extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_products add column acceptCalceled int after accept');
    }
    public function down()
    {
        $this->query('alter table dp_products drop column acceptCalceled');
    }
}
