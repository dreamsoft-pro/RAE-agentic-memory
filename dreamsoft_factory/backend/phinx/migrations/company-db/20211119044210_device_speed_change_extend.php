<?php


use Phinx\Migration\AbstractMigration;

class DeviceSpeedChangeExtend extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_device_speed_changes
add column sheetFoldsMin      int unsigned null after thicknessMax,
add column sheetFoldsMax      int unsigned null after sheetFoldsMin,
add column projectSheetsMin      int unsigned null after sheetFoldsMax,
add column projectSheetsMax      int unsigned null after projectSheetsMin
');
        $this->query('alter table ps_device_speed_changes_overrides
add column sheetFoldsMin      int unsigned null after thicknessMax,
add column sheetFoldsMax      int unsigned null after sheetFoldsMin,
add column projectSheetsMin      int unsigned null after sheetFoldsMax,
add column projectSheetsMax      int unsigned null after projectSheetsMin');
    }

    public function down()
    {
        $this->query('alter table dp_device_speed_changes
drop column sheetFoldsMin,
drop column sheetFoldsMax,
drop column projectSheetsMin,
drop column projectSheetsMax');
        $this->query('alter table ps_device_speed_changes_overrides
drop column sheetFoldsMin,
drop column sheetFoldsMax,
drop column projectSheetsMin,
drop column projectSheetsMax');
    }
}
