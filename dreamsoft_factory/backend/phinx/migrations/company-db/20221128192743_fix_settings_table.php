<?php


use Phinx\Migration\AbstractMigration;

class FixSettingsTable extends AbstractMigration
{

    public function up()
    {
        $this->query('delete t1 from dp_settings t1
                    inner join dp_settings t2
                    where t1.ID<t2.ID and t1.`key`=t2.`key` and t1.domainID=t2.domainID and t1.module=t2.module');
    }

}
