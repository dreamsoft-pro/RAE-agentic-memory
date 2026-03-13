<?php


use Phinx\Migration\AbstractMigration;

class AddProductLabelImpositionField extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_productLabelImposition
                            add column labelImpositionDiePdfPath varchar(512) null');
    }
    public function down()
    {
        $this->query('alter table dp_productLabelImposition drop column labelImpositionDiePdfPath');
    }
}
