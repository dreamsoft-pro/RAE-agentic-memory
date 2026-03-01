<?php


use Phinx\Migration\AbstractMigration;

class AddMargins extends AbstractMigration
{

    public function up()
    {
        $this->query('create table dp_margins(
                        ID int primary key ,
                        priceTypeID int not null,
                        natureID int not null,
                        piecesMin decimal(10,2),
                        piecesMax decimal(10,2),
                        sheetsMin decimal(10,2),
                        sheetsMax decimal(10,2),
                        sqmetersMin decimal(10,2),
                        sqmetersMax decimal(10,2),
                        kilogramsMin decimal(10,2),
                        kilogramsMax decimal(10,2),
                        metersMin decimal(10,2),
                        metersMax decimal(10,2),
                        percentage decimal(10,2) not null
        )');

        $this->query('create table dp_margins_supplier(
                        ID int primary key ,
                        supplierName varchar(512) not null,
                        percentage decimal(10,2) not null
        )');
    }

    public function down()
    {
        $this->query('drop table if exists dp_margins');
        $this->query('drop table if exists dp_margins_supplier');
    }
}
