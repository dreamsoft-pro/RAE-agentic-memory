<?php


use Phinx\Migration\AbstractMigration;

class AddRealisationTimeExpand extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_user_calc add column realisationDateExpandBy int not null default 0');
    }
    public function down()
    {
        $this->query('alter table ps_user_calc drop column realisationDateExpandBy');
    }
}
