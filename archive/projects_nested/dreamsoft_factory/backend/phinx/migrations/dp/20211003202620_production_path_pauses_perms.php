<?php


use Phinx\Migration\AbstractMigration;

class ProductionPathPausesPerms extends AbstractMigration
{

    public function up()
    {
		$this->query("INSERT INTO dp_permissions (`desc`, `package`, `controller`, `action`, `default`) VALUES
		(NULL, 'ProductionPath', 'Pauses', 'count', 0),
		(NULL, 'ProductionPath', 'Pauses', 'put_pauses', 0),
		(NULL, 'ProductionPath', 'Pauses', 'delete_pauses', 0),
		(NULL, 'ProductionPath', 'Pauses', 'post_pauses', 0),
		(NULL, 'ProductionPath', 'Pauses', 'pauses', 0);");
    }
    public function down()
    {
        //null
    }
}