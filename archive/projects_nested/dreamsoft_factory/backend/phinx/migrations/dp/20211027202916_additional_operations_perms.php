<?php


use Phinx\Migration\AbstractMigration;

class AdditionalOperationsPerms extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO dp_permissions (`desc`, `package`, `controller`, `action`, `default`) VALUES
		(NULL, 'ProductionPath', 'Ongoings', 'post_additionalOperation', 0),
		(NULL, 'ProductionPath', 'Ongoings', 'patch_additionalOperation', 0);");
    }
    public function down()
    {
        //can be rolled back manually
    }
}
