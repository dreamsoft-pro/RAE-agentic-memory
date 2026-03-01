<?php


use Phinx\Migration\AbstractMigration;

class DeviceSpeedChangeExtend2 extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_device_speed_changes
add column cutUseMin      int unsigned null after projectSheetsMax
');
        $this->query('alter table ps_device_speed_changes_overrides
add column cutUseMin      int unsigned null after projectSheetsMax');
    }

    public function down()
    {
        $this->query('alter table dp_device_speed_changes
drop column cutUseMin');
        $this->query('alter table ps_device_speed_changes_overrides
drop column cutUseMin');
    }
}
