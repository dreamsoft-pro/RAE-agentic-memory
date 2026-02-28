<?php


use Phinx\Migration\AbstractMigration;

class AddReportFiles extends AbstractMigration
{

    public function up()
    {
        $this->query('create table dp_product_report_files(
            productID int not null,
            fileID int not null,
            comment varchar(2000),
            accept int default 0,
            acceptChangeDate datetime null,
            foreign key (productID) references dp_products(ID),
            foreign key (fileID) references uploadedFiles(ID)
            );
        ');
    }

    public function down()
    {
        $this->query('drop table if exists dp_product_report_files;');
    }
}
