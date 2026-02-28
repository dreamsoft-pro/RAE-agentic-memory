<?php


use Phinx\Migration\AbstractMigration;

class AddPsProductsTypesCalcFiles extends AbstractMigration{

    public function up()
    {
        $this->query('alter table ps_products_types add column allowCalcFilesUpload int not null default 0');
    }
    public function down()
    {
        $this->query('alter table ps_products_types drop column allowCalcFilesUpload');
    }
}
