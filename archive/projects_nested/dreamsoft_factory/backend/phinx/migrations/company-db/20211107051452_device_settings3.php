<?php


use Phinx\Migration\AbstractMigration;

class DeviceSettings3 extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_device_speed_change_sides
change column sideRelationWidth sideRelationWidth int unsigned not null,
change column sideRelationHeight sideRelationHeight int unsigned not null,
change column efficiencyChange efficiencyChange double not null;');

        $this->query('alter table dp_device_speed_changes
change column grammageMin  grammageMin   int unsigned null,
change column grammageMax  grammageMax    int unsigned null,
change column stiffnessMin  stiffnessMin   int unsigned null,
change column stiffnessMax   stiffnessMax  int unsigned null,
change column thicknessMin   thicknessMin  int unsigned null,
change column thicknessMax  thicknessMax   int unsigned null,
change column efficiencyChange efficiencyChange double  not null;');

        $this->query('alter table dp_devices change column deviceTime deviceTime int unsigned null, 
    change column stackImpositionTime stackImpositionTime int unsigned null, 
    change column stackHeight stackHeight double unsigned null, 
    change column printedStackHeight printedStackHeight double unsigned null, 
    change column if exists depotTransportTime transportTime int unsigned null');

        $this->query('alter table ps_device_efficiency_overrides 
    change column if exists depotTransportTime transportTime int unsigned null;');

        $this->query('alter table ps_device_speed_changes_overrides
     change column grammageMin   grammageMin  int unsigned null,
    change column grammageMax  grammageMax    int unsigned null,
    change column stiffnessMin   stiffnessMin  int unsigned null,
    change column stiffnessMax  stiffnessMax   int unsigned null,
    change column thicknessMin  thicknessMin   int unsigned null,
    change column thicknessMax  thicknessMax   int unsigned null,
    change column efficiencyChange efficiencyChange double not null;');

        $this->query('alter table ps_device_side_relations_overrides 
    change column efficiencyChange efficiencyChange double not null');

    }

    public function down()
    {
    }
}
