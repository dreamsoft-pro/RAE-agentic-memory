<?php


use Phinx\Migration\AbstractMigration;

class ExternalApiProd extends AbstractMigration
{

    public function up()
    {
		$this->query('CREATE TABLE dp_external_data (
            ID int(11) NOT NULL auto_increment primary key,
            orderID int(11) NOT NULL,
            deviceID int(11) NOT NULL,
            unit varchar(10) NOT NULL,
            quantity int(11) NOT NULL,
            optionID int(11) NOT NULL,
            attributeID int(11) NOT NULL
          );');

    }
    public function down()
    {
        $this->query('drop table dp_external_data;');
    }
}
