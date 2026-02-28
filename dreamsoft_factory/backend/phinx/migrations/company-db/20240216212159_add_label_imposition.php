<?php


use Phinx\Migration\AbstractMigration;

class AddLabelImposition extends AbstractMigration
{

    public function up()
    {
        $this->query('create table ps_labelImposition(
        ID int not null,
        enabled int not null,
        productTypeID int not null,
        
        labelRotation enum("0","90","180","270"),
        numberOfColumns int,
        numberOfRows int,
        minSheetLength int,
        sheetWidth int,
        labelDistance int,
        columnsDistance int,
        
        barcodeData varchar(512),
        barcodePositionX int,
        barcodePositionY int,
        barcodeWidth int,
        barcodeHeight int,
        
        qrCodeData varchar(512),
        qrCodePositionX int,
        qrCodePositionY int,
        qrCodeSize int,
        
        photocellPositionX char(10),
        photocellPositionY int,
        photocellWidth int,
        photocellHeight int,
        
        primary key(ID),
        foreign key(productTypeID) references ps_products_types(ID),
        unique key(productTypeID)
        );');

        $this->query('create table dp_productLabelImposition(
                            productID int not null primary key,
                            labelImpositionPath varchar(512) null,
                            labelImpositionDieCutPath varchar(512) null,
                            sheetLengthInMm int null,
                            sheetSurfaceInSquareMm int null,
                            sumLabelsOnSheet int null,
                            foreign key(productID) references dp_products(ID)
                            )
    ');
    }
    public function down()
    {
        $this->query('drop table dp_productLabelImposition');
        $this->query('drop table ps_labelImposition');
    }
}
