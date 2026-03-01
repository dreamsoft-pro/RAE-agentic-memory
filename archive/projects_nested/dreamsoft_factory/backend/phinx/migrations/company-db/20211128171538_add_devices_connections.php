<?php


use Phinx\Migration\AbstractMigration;

class AddDevicesConnections extends AbstractMigration
{

    public function up()
    {
        $this->query('create table dp_priceListDevices(
    deviceID int not null,
    priceListID int not null,
    foreign key (deviceID) references dp_devices (ID),     
    foreign key (priceListID) references ps_config_workspaces (ID),
    unique key(deviceID, priceListID)       
);');
        $this->query('create table dp_workspacesDevices(
    deviceID int not null,
    workspaceID int not null,
    foreign key (deviceID) references dp_devices (ID),     
    foreign key (workspaceID) references ps_config_workspaces (ID),
    unique key(deviceID, workspaceID)       
);');
    $this->query("create table dp_optionControllerOperationDevice(
    optID int not null,
    operationID int not null,
    controllerID int not null,
    deviceID int not null,
    foreign key (optID) references ps_config_options (ID),
    foreign key (deviceID) references dp_devices (ID),
    foreign key (operationID) references dp_operations (ID),
    unique key(optID, operationID, controllerID, deviceID)
);");
    }

    public function down()
    {
        $this->query('drop table if exists dp_priceListDevices');
        $this->query('drop table if exists dp_workspacesDevices');
        $this->query('drop table if exists dp_optionControllerOperationDevice');
    }
}
