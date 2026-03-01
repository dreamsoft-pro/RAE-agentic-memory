<?php


use Phinx\Migration\AbstractMigration;

class AddProductionShifts extends AbstractMigration
{

    public function up()
    {
        $this->query('CREATE TABLE `dp_production_shifts` (
            `ID` int(11) NOT NULL PRIMARY KEY,
            `name` varchar(50) NOT NULL,
            `sort` int(11) NOT NULL,
            `start` time NOT NULL,
            `stop` time NOT NULL
          ) DEFAULT CHARSET=utf8;');
        
    }
    public function down()
    {
        $this->query('drop table if exists dp_production_shifts');
    }
}
