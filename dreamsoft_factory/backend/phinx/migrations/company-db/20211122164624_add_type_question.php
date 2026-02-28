<?php


use Phinx\Migration\AbstractMigration;

class AddTypeQuestion extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_products_types add column isQuestionOnly tinyint unsigned');
    }
    public function down()
    {
        $this->query('alter table ps_products_types drop column isQuestionOnly');
    }
}
