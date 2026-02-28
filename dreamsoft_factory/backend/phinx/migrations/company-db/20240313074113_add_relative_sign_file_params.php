<?php


use Phinx\Migration\AbstractMigration;

class AddRelativeSignFileParams extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_labelImposition
                            add column qrCodeAnotherSignFilePositionX int not null default 0 after qrCodePositionX,
                            add column photocellAnotherSignFilePositionX int not null default 0 after photocellPositionX
    ');
    }
    public function down()
    {
        $this->query('alter table ps_labelImposition drop column qrCodeAnotherSignFilePositionX, 
            drop column photocellAnotherSignFilePositionX');
    }
}
