<?php


use Phinx\Migration\AbstractMigration;

class AddMachinesShifts extends AbstractMigration
{

    public function up()
    {
        $this->query('CREATE TABLE `dp_device_shift` (
            `ID` int(11) NOT NULL PRIMARY KEY,
            `deviceID` int(11) NOT NULL,
            `name` varchar(50) NOT NULL,
            `sort` int(11) NOT NULL,
            `start` time NOT NULL,
            `stop` time NOT NULL
          ) DEFAULT CHARSET=utf8;');
        
    }
    public function down()
    {
        $this->query('drop table if exists dp_device_shift');
    }
}
