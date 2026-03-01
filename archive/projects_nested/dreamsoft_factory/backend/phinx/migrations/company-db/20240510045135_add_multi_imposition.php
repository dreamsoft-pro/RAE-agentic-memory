<?php


use Phinx\Migration\AbstractMigration;

class AddMultiImposition extends AbstractMigration
{

    public function up()
    {
        $this->query('delete from dp_productLabelImposition where 1');
        $this->query('alter table dp_productLabelImposition drop constraint `dp_productlabelimposition_ibfk_1`');
        $this->query('alter table dp_productLabelImposition drop primary key');
        $this->query('alter table dp_productLabelImposition drop column productID');
        $this->query('alter table dp_productLabelImposition add column fileID int not null');
        $this->query('alter table dp_productLabelImposition add constraint foreign key `fk_fileID` (fileID) references ps_user_calc_product_files(ID)');
    }

    public function down()
    {
    }
}
