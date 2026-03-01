<?php


use Phinx\Migration\AbstractMigration;

class ChangeImposition extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_labelImposition
                        add column barcodeEnabled int not null default 0,
                        add column qrCodeEnabled int not null default 0,
                        add column photocellEnabled int not null default 0,
                        add column laserTriggerEnabled int not null default 0,
                        add column laserTriggerPositionX varchar(10) ,
                        add column laserTriggerPositionY varchar(10) ,
                        add column laserTriggerWidth int ,
                        add column laserTriggerHeight int,
                        add column qrCodeAnotherSignFilePositionY int,
                        add column photocellAnotherSignFilePositionY int
    ');
    }

    public function down()
    {
        $this->query('alter table ps_labelImposition
                        drop column barcodeEnabled,
                        drop column qrCodeEnabled ,
                        drop column photocellEnabled ,
                        drop column laserTriggerEnabled ,
                        drop column laserTriggerPositionX,
                        drop column laserTriggerPositionY ,
                        drop column laserTriggerWidth ,
                        drop column laserTriggerHeight,
                        drop column qrCodeAnotherSignFilePositionY,
                        drop column photocellAnotherSignFilePositionY
    ');
    }
}
