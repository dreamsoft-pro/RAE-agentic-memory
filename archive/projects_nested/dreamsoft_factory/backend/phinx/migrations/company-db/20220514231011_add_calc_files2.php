<?php


use Phinx\Migration\AbstractMigration;

class AddCalcFiles2 extends AbstractMigration
{

    public function up()
    {
        $this->query('CREATE TABLE `dp_calcFiles` (
            `ID` int(11) NOT NULL PRIMARY KEY,
            `name` varchar(255) NOT NULL,
            `calcFilesSetID` int(11) NOT NULL,
            `created` datetime NOT NULL
          )');

        $this->query('CREATE TABLE `dp_calcFilesSets` (
            `ID` int(11) NOT NULL PRIMARY KEY,
            `userID`  int(11) NOT NULL,
            `calcID` int(11) NOT NULL,
            `typeID` int(11) NOT NULL,
            `created` datetime NOT NULL
        )');
        
    }
    public function down()
    {
        $this->query('drop table if exists dp_calcFiles');
        $this->query('drop table if exists dp_calcFilesSets');
    }
}
