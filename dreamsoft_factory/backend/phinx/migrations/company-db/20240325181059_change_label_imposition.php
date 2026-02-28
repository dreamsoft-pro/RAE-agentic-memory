<?php


use Phinx\Migration\AbstractMigration;

class ChangeLabelImposition extends AbstractMigration
{

    public function up()
    {

        $this->query('alter table dp_productLabelImposition add column hotFolderJobMarker varchar(255) not null');
        $this->query('alter table dp_productLabelImposition add column hotFolderJobImposition varchar(255) not null');
        $this->query('alter table dp_productLabelImposition drop column hotFolderJobXmlFile');
    }
    public function down()
    {

    }
}
