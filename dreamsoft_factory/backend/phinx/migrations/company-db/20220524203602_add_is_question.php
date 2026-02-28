<?php


use Phinx\Migration\AbstractMigration;

class AddIsQuestion extends AbstractMigration {

    public function up()
    {
        $this->query('alter table dp_orders add column isQuestion int not null default 0');
    }
    public function down()
    {
        $this->query('alter table dp_orders drop column isQuestion');
    }
}
