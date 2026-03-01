<?php


use Phinx\Migration\AbstractMigration;

class ProductionPathPauses extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_ongoingLogs add column pauseID int(11) null default null;');
        $this->query('alter table dp_ongoingLogs add column customPause varchar(50) null default null;');
		$this->query('CREATE TABLE dp_pauses (
						  ID int(11) NOT NULL  auto_increment primary key,
						  name varchar(200) NOT NULL,
						  sort int(11) NOT NULL,
						  created datetime NOT NULL,
						  color varchar(10) DEFAULT NULL
		);');
    }
    public function down()
    {
        $this->query('drop table dp_pauses;');
    }
}
