<?php


use Phinx\Migration\AbstractMigration;

class DeviceSettingsOverrides extends AbstractMigration
{

    public function up()
    {
        $this->query('create table ps_device_efficiency_overrides(
     ID          int not null primary key auto_increment,
     attrID int not null,
     optID int not null,
     controllerID int null,
     deviceTime          int not null default 0,
    stackImpositionTime int not null default 0,
    stackHeight         int not null default 0,
    printedStackHeight  int not null default 0,
    depotTransportTime  int not null default 0,
    foreign key (attrID) references ps_config_attributes(ID),
    foreign key (optID) references ps_config_options(ID),
    unique key `unique-attribute-option-controller`(attrID, optID, controllerID)
    );');
        $this->query('create table ps_device_speeds_overrides(
     ID          int not null primary key auto_increment,
     attrID int not null,
     optID int not null,
     controllerID int null,
     volume   int not null,
    speed    int not null,
    foreign key (attrID) references ps_config_attributes(ID),
    foreign key (optID) references ps_config_options(ID),
    unique key `unique-attribute-option-controller`(attrID, optID, controllerID)
    );');
        $this->query('create table ps_device_speed_changes_overrides(
     ID          int not null primary key auto_increment,
     attrID int not null,
     optID int not null,
     controllerID int null,
     grammageMin      int not null,
    grammageMax      int not null,
    stiffnessMin     int not null,
    stiffnessMax     int not null,
    thicknessMin     int not null,
    thicknessMax     int not null,
    efficiencyChange int not null,
    foreign key (attrID) references ps_config_attributes(ID),
    foreign key (optID) references ps_config_options(ID),
    unique key `unique-attribute-option-controller`(attrID, optID, controllerID)
    );');
        $this->query('create table ps_device_side_relations_overrides(
     ID          int not null primary key auto_increment,
     attrID int not null,
     optID int not null,
     controllerID int null,
     sideRelationWidth  int not null,
    sideRelationHeight int not null,
    efficiencyChange   int not null,
    foreign key (attrID) references ps_config_attributes(ID),
    foreign key (optID) references ps_config_options(ID),
    unique key `unique-attribute-option-controller`(attrID, optID, controllerID)
    );');
    }

    public function down()
    {
        $this->query('drop table if exists ps_device_efficiency_overrides;');
        $this->query('drop table if exists ps_device_speeds_overrides;');
        $this->query('drop table if exists ps_device_speed_changes_overrides;');
        $this->query('drop table if exists ps_device_side_relations_overrides;');
    }
}
