<?php


use Phinx\Migration\AbstractMigration;

class DeviceSpeedChangeExtend2Fix extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_device_speed_changes
add column cutUseMax      int unsigned null after cutUseMin
');
        $this->query('alter table ps_device_speed_changes_overrides
add column cutUseMax      int unsigned null after cutUseMin');
    }

    public function down()
    {
        $this->query('alter table dp_device_speed_changes
drop column cutUseMax');
        $this->query('alter table ps_device_speed_changes_overrides
drop column cutUseMax');
    }
}
