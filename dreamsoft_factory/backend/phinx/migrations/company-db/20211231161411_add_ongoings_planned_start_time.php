<?php


use Phinx\Migration\AbstractMigration;

class AddOngoingsPlannedStartTime extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_ongoings add column plannedStart datetime null');
    }
    public function down()
    {
        $this->query('alter table dp_ongoings drop column plannedStart');
    }
}
