<?php


use Phinx\Migration\AbstractMigration;

class ExtendProductLabelImposition extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_productLabelImposition add column xmlFile varchar(255) not null');
    }
    public function down()
    {
        $this->query('alter table dp_productLabelImposition drop column xmlFile');
    }
}
