<?php


use Phinx\Migration\AbstractMigration;

class AddOrderNumber extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_orders add column orderNumber int null');
        $this->query('update dp_orders set orderNumber=ID');
    }
    public function down()
    {
        $this->query('alter table dp_orders drop column orderNumber');
    }
}
