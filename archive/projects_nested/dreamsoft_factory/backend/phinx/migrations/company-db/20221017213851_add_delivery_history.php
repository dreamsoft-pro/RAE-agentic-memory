<?php


use Phinx\Migration\AbstractMigration;

class AddDeliveryHistory extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_orderAddress change column ID ID int not null');

        $this->query('alter table dp_orderAddress add column baseID int not null default(ID) after ID');

        $this->query('alter table dp_orderAddress add column `current` int not null default 1 after baseID');

        $this->query('alter table dp_orderAddress add column ver int not null default 1 after `current`');

        $this->query('create table dp_orderAddressUpdates (ID int primary key, created timestamp not null default current_timestamp , userID int not null, userName varchar(100) not null, isSuperUser int not null, reason varchar(255) null)');

        $this->query('create table dp_orderAddressUpdatesAssoc (updateID int, orderAddressID int,  constraint UK_update_orderAddr unique (updateID, orderAddressID))');

        $this->query('update dp_orderAddress set baseID=ID, ver=1, `current`=1');
    }
    public function down()
    {
        $this->query('alter table dp_orderAddress drop column if exists baseID , drop column if exists ver , drop column if exists `current`;');
        $this->query('drop table if exists dp_orderAddressUpdatesAssoc');
        $this->query('drop table if exists dp_orderAddressUpdates');
    }
}
