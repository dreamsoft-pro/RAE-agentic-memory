<?php


use Phinx\Migration\AbstractMigration;

class AddCustomProductParams extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_customProducts
add column baseGroupID int null,
add column baseTypeID int null;');
    }

    public function down()
    {
        $this->query('alter table dp_customProducts
drop column baseGroupID,
drop column baseTypeID;');
    }
}
