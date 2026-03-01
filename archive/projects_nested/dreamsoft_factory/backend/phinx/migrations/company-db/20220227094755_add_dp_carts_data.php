<?php


use Phinx\Migration\AbstractMigration;

class AddDpCartsData extends AbstractMigration
{

    public function up()
    {
        $this->query("CREATE TABLE `dp_carts_data` (
            `ID` int(11) NOT NULL auto_increment primary key,
            `calcID` int(11) NOT NULL,
            `orderID` int(11) NOT NULL,
            `productID` int(11) NOT NULL,
            `productAddresses` text NOT NULL,
            `userID` int(11) NULL DEFAULT '0',
            `token` varchar(200) NULL
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8;");
    }
    public function down()
    {
        $this->query('drop table dp_carts_data;');
    }
}
