<?php


use Phinx\Migration\AbstractMigration;

class AddProductsMultioffer extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_products add column isMultiVolumeOffer int not null default 0;');
    }
    public function down()
    {
        $this->query('alter table dp_products
                    drop column if exists `dp_products`
                    ');
    }
}
