<?php


use Phinx\Migration\AbstractMigration;

class AddDevicesSettings extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_devices
    add workUnit          varchar(20) not null ,
    add deviceTime          int not null default 0,
    add stackImpositionTime int not null default 0,
    add stackHeight         int not null default 0,
    add printedStackHeight  int not null default 0,
    add depotTransportTime  int not null default 0,
    add sheetSizeMax        int,
    add sheetSizeMin        int,
    add grammageMax         int,
    add grammageMin         int,
    add thicknessMin        int,
    add thicknessMax        int,
    add stiffnessMin        int,
    add stiffnessMax        int;');
        $this->query('create table dp_device_speeds
(
    deviceID int not null,
    volume   int not null,
    speed    int not null,
    foreign key (deviceID) references dp_devices (ID)
);');
        $this->query('create table dp_device_speed_changes
(
    deviceID         int not null,
    grammageMin      int not null,
    grammageMax      int not null,
    stiffnessMin     int not null,
    stiffnessMax     int not null,
    thicknessMin     int not null,
    thicknessMax     int not null,
    efficiencyChange int not null,
    foreign key (deviceID) references dp_devices (ID)
);');
        $this->query('create table dp_device_speed_change_sides
(
    deviceID           int not null,
    sideRelationWidth  int not null,
    sideRelationHeight int not null,
    efficiencyChange   int not null,
    foreign key (deviceID) references dp_devices (ID)
);');
        $this->query('create table dp_device_prices
    (
        deviceID  int not null,
    amount    int not null,
    unitPrice double not null,
    unitCost  double not null,
    foreign key (deviceID) references dp_devices (ID)
);');
        $this->query('create table dp_device_service_cycles
(
    ID   int         not null primary key,
    name varchar(50) not null
);');
        $this->query('create table dp_device_services
(
    deviceID        int not null,
    cycleID         int not null,
    hourOfBeginning int not null,
    timeDuration    int not null,
    foreign key (deviceID) references dp_devices (ID),
    foreign key (cycleID) references dp_device_service_cycles (ID)
);');
        $this->query('alter table ps_config_detailPrices
add column manHours int not null default 0;');
    }
    public function down()
    {
        $this->query('drop table if exists dp_device_speed_changes;');
        $this->query('drop table if exists dp_device_speed_change_sides;');
        $this->query('drop table if exists dp_device_prices;');
        $this->query('drop table if exists dp_device_service_cycles;');
        $this->query('drop table if exists dp_device_services;');
    }
}
