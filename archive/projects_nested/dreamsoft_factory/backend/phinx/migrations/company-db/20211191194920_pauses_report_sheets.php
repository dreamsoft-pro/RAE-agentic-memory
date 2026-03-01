<?php


use Phinx\Migration\AbstractMigration;

class PausesReportSheets extends AbstractMigration
{

    public function up()
    {
        $this->query("alter table dp_pauses add column report_sheets tinyint(1) NOT NULL DEFAULT '0';");

    }
    public function down()
    {
        $this->query("alter table dp_pauses drop column if exists report_sheets");
    }
}
