<?php


use Phinx\Migration\AbstractMigration;

class AddMultiVolumeFiles extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_products_types add column allowVolumeDivide int not null default 0');
        $this->query('alter table ps_user_calc_product_files add column volume int null');
    }
    public function down()
    {
        $this->query('alter table ps_products_types drop column allowVolumeDivide');
        $this->query('alter table ps_user_calc_product_files drop column volume');
    }
}
