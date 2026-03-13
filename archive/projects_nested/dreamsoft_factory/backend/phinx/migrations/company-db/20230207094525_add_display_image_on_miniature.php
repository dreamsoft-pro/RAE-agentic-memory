<?php


use Phinx\Migration\AbstractMigration;

class AddDisplayImageOnMiniature extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_attributes add column displayImageOnMiniature int not null default 0  after multipleOptionsMax');
    }
    public function down()
    {
        $this->query('alter table ps_config_attributes drop column displayImageOnMiniature');
    }
}
