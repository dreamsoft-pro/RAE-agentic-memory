<?php


use Phinx\Migration\AbstractMigration;

class AddReportAcceptUser extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table dp_product_report_files
                            add column acceptRejectUserID int null,
                            add column acceptRejectUserName char(30) null');
    }

    public function down()
    {
        $this->query('alter table dp_product_report_files 
                            drop column acceptRejectUserID, 
                            drop column acceptRejectUserName');
    }
}
