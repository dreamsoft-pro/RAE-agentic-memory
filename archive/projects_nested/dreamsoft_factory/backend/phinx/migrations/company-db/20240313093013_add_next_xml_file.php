<?php


use Phinx\Migration\AbstractMigration;

class AddNextXmlFile extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_productLabelImposition add column hotFolderJobXmlFile varchar(255) not null');
    }
    public function down()
    {
        $this->query('alter table dp_productLabelImposition drop column hotFolderJobXmlFile');
    }
}
