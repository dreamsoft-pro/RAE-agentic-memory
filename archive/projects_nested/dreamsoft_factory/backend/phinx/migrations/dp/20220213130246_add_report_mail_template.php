<?php


use Phinx\Migration\AbstractMigration;

class AddReportMailTemplate extends AbstractMigration
{

    public function up()
    {
        $this->query("insert into dp_templates (ID, name, fileName, created) values(123, 'product-report', 'product-report', now())");
    }
    public function down()
    {
        $this->query('delete from dp_templates where ID = 123');
    }
}
