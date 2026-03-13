<?php


use Phinx\Migration\AbstractMigration;

class AddOptionTooltip extends AbstractMigration
{

    public function up()
    {
        $this->query('create table ps_config_option_tooltip_lang(
                                              ID int not null,
                                              optionID int not null,
                                              lang varchar(3) not null,
                                              tooltip text,
                                              primary key (ID),
                                              foreign key (optionID) references ps_config_options(ID) on delete cascade,
                                              unique key `unique-optionID-lang`(optionID, lang)

)');
    }
    public function down()
    {
        $this->query('drop table if exists ps_config_option_tooltip_lang');
    }
}
