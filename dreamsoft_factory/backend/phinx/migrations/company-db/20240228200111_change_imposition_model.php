<?php


use Phinx\Migration\AbstractMigration;

class ChangeImpositionModel extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_labelImposition add column showLaserTriggers int null');
        $this->query('alter table dp_productLabelImposition add column anotherSignFile varchar(255) null');
    }
    public function down()
    {
        $this->query('alter table ps_labelImposition drop column showLaserTriggers');
        $this->query('alter table dp_productLabelImposition drop column anotherSignFile');
    }
}
