<?php


use Phinx\Migration\AbstractMigration;

class DeviceSettingsFixes extends AbstractMigration
{

    public function up()
    {
        $this->query('drop table if exists dp_device_speeds;');
        $this->query('create table dp_device_speeds
(
    ID  int not null primary key auto_increment,
    deviceID int not null,
    volume   int not null,
    speed    int not null,
    foreign key (deviceID) references dp_devices (ID),
    unique key `unique-device-volume`(deviceID, volume)
);');

        $this->query('drop table if exists dp_device_speed_changes;');
        $this->query('create table dp_device_speed_changes
(
    ID  int not null primary key auto_increment,
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

        $this->query('drop table if exists dp_device_speed_change_sides;');
        $this->query('create table dp_device_speed_change_sides
(
    ID  int not null primary key auto_increment,
    deviceID           int not null,
    sideRelationWidth  int not null,
    sideRelationHeight int not null,
    efficiencyChange   int not null,
    foreign key (deviceID) references dp_devices (ID)
);');
        $this->query('drop table if exists dp_device_prices;');
        $this->query('create table dp_device_prices
(
    ID  int not null primary key auto_increment,
    deviceID  int not null,
    amount    int not null,
    unitPrice double not null,
    unitCost  double null,
    foreign key (deviceID) references dp_devices (ID),
    unique key `unique-device-amount`(deviceID, amount)
);');
        $this->query('drop table if exists dp_device_services;');
        $this->query('drop table if exists dp_device_service_cycles;');
        $this->query('create table dp_device_service_cycles
(
    ID   int         not null primary key auto_increment,
    name varchar(50) not null
);');

        $this->query('create table dp_device_services
(
    ID   int         not null primary key auto_increment,
    deviceID        int not null,
    cycleID         int not null,
    hourOfBeginning int not null,
    timeDuration    int not null,
    foreign key (deviceID) references dp_devices (ID),
    foreign key (cycleID) references dp_device_service_cycles (ID)
);');
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
