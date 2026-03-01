<?php


use Phinx\Migration\AbstractMigration;

class DeviceSettings4 extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_device_efficiency_overrides
change deviceTime deviceTime int unsigned null,
change stackImpositionTime stackImpositionTime int unsigned null,
change stackHeight stackHeight int unsigned null,
change printedStackHeight printedStackHeight int unsigned null
');
    }
    public function down()
    {
        //No downgrade wider columns
    }
}
