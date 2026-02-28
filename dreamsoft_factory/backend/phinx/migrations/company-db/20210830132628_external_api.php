<?php


use Phinx\Migration\AbstractMigration;

class ExternalApi extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_orders change column modified modified timestamp  default current_timestamp() not null;');
        $this->query('alter table dp_ongoings change column created created datetime  default current_timestamp() not null;');
        $this->query('alter table dp_ongoings add column estimatedTime int null;');
        $this->query('alter table users add externalID varchar(100) null default null;');
        $this->query('alter table address add externalID varchar(100) null default null;');
        $this->query('create table dp_external_products(
    typeID int not null,
    groupID int not null,
    externalID varchar(100) not null,
    unique (typeID,groupID,externalID)
);');
    }
    public function down()
    {
        $this->query('drop table dp_external_products;');
    }
}
