<?php


use Phinx\Migration\AbstractMigration;

class AddProductPriority extends AbstractMigration
{

    public function up()
    {
        $this->query("alter table dp_products add column priority int(2) NOT NULL DEFAULT '5';");
    }
    public function down()
    {
        $this->query('alter table dp_products drop column priority');
    }
}
