<?php


use Phinx\Migration\AbstractMigration;

class AddFormatField extends AbstractMigration
{

    public function up()
    {
        $this->query("alter table ps_products_formats
    add column binding enum ('sewn','glue','spiral') null;");
    }

    public function down()
    {
        $this->query('alter table ps_products_formats
    drop column binding;');
    }
}
