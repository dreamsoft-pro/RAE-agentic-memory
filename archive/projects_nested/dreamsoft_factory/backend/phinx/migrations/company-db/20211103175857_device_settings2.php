<?php


use Phinx\Migration\AbstractMigration;

class DeviceSettings2 extends AbstractMigration
{

    public function up()
    {
        $this->query('drop table if exists dp_device_speed_change_sides;');
        $this->query('create table dp_device_speed_change_sides
(
    ID  int not null primary key auto_increment,
    deviceID           int not null,
    sideRelationWidth  int not null,
    sideRelationHeight int not null,
    efficiencyChange   int not null,
    foreign key (deviceID) references dp_devices (ID),
    unique key `unique`(deviceID, sideRelationWidth, sideRelationHeight, efficiencyChange)
);');
        $this->query('drop table if exists dp_device_services');
        $this->query('create table dp_device_services
(
    ID  int not null primary key auto_increment,
    deviceID        int not null,
    cycleID         int not null,
    name varchar(100) not null,
    hourOfBeginning int not null,
    timeDuration    int not null,
    foreign key (deviceID) references dp_devices (ID),
    unique key `record` (name, cycleID, hourOfBeginning, timeDuration)
);');
        $this->query('drop table if exists dp_device_service_cycles');
    }
    public function down()
    {
        $this->query('drop table if exists dp_device_speed_change_sides');
        $this->query('drop table if exists dp_device_services');
    }
}
