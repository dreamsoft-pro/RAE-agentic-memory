<?php


use Phinx\Migration\AbstractMigration;

class FixFieldName extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_products add column acceptCanceled int after acceptCalceled');
        $this->query('update dp_products set acceptCanceled=acceptCalceled');
        $this->query('alter table dp_products drop column acceptCalceled');
    }
    public function down()
    {
        $this->query('');
    }
}
