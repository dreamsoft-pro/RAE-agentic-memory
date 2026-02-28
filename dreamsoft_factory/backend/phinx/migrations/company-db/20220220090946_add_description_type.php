<?php


use Phinx\Migration\AbstractMigration;

class AddDescriptionType extends AbstractMigration
{

    public function up()
    {
        $this->query("insert into ps_config_option_description_type(`name`,`group`,`editor`)
                            values('paper_type','paper','default'),('paper_type_description','paper','default'),('paper_type_image','paper','default'),('color_hex','paper','default')");
        $this->query("insert into dp_settings(`module`,`key`,`value`)
                            values('additionalSettings','filteredAttribute','2')");
        $this->query("alter table ps_config_option_description
                            add index `attributeID-optionID-domainID` (`attributeID`,`optionID`,`domainID`)");


    }

    public function down()
    {
        $this->query("delete from ps_config_option_description_type where name in ('type', 'type_description', 'type_image')");
        $this->query("delete from dp_settings where `key` = 'filteredAttribute'");
    }
}
