<?php


use Phinx\Migration\AbstractMigration;

class AdditionalOperationFix extends AbstractMigration
{

    public function up()
    {
        $this->query("ALTER TABLE `dp_additional_operation` CHANGE `operatorID` `operatorID` INT(11) NULL DEFAULT NULL;");

    }
    public function down()
    {
        //
    }
}