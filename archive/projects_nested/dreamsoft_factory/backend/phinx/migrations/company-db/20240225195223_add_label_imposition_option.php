<?php


use Phinx\Migration\AbstractMigration;

class AddLabelImpositionOption extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_labelImposition add column anotherSignFile int');
    }
    public function down()
    {
        $this->query('alter table ps_labelImposition drop column anotherSignFile');
    }
}
