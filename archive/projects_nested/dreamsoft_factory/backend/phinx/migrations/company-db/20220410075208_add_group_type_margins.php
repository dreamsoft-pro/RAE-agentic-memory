<?php


use Phinx\Migration\AbstractMigration;

class AddGroupTypeMargins extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_margins add column groupID int null,
                     add column typeID int null,
                     add constraint foreign key `fk_groupID` (groupID) references ps_products_groups (ID),
                     add constraint foreign key `fk_typeID` (typeID) references ps_products_types (ID)');
    }
    public function down()
    {
        $this->query('alter table dp_margins
                    drop foreign key if exists`fk_groupID`,
                    drop column if exists `groupID`,
                    drop foreign key if exists `fk_typeID`,
                    drop column if exists `typeID`
                    ');
    }
}
