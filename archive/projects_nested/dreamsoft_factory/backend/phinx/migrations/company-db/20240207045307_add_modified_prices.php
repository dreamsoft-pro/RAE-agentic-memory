<?php


use Phinx\Migration\AbstractMigration;

class AddModifiedPrices extends AbstractMigration
{

    public function up()
    {
        $this->query("create table ps_user_fixFilePrices(
    ID int not null,
    productID int not null,
    price int not null,
    primary key (ID),
    foreign key (productID) references dp_products(ID)
)");
    }
    public function down()
    {
        $this->query('drop table ps_user_fixFilePrices');
    }
}
