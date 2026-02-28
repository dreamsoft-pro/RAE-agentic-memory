<?php


use Phinx\Migration\AbstractMigration;

class DeliveryDefault extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_orders add column deliveryConnected int not null default 1');
    }
    public function down()
    {
        $this->query('alter table dp_orders drop column deliveryConnected');
    }
}
