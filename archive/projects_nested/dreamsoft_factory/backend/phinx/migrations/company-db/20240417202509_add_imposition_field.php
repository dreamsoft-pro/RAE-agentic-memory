<?php


use Phinx\Migration\AbstractMigration;

class AddImpositionField extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_labelImposition 
    add column rotationAngle enum("0","90","180","270") after labelRotation');
    }

    public function down()
    {
        $this->query('alter table ps_labelImposition drop column rotationAngle');
    }
}
