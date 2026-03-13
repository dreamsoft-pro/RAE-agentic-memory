<?php


use Phinx\Migration\AbstractMigration;

class AddEditorCartMode extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_products add column inEditor tinyint null');
    }
    public function down()
    {
        $this->query('alter table dp_products drop column inEditor');
    }
}
