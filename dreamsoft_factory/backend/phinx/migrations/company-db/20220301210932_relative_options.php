<?php


use Phinx\Migration\AbstractMigration;

class RelativeOptions extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_products_types
            add column useAlternatives tinyint unsigned');

        $this->query('create table ps_alternative_options_filter(
            attrID int,
            optID int,
            descriptionTypeID int,
            `name` varchar(512),
            valueType enum("min", "max", "exact"),
            `value` varchar(512),
            foreign key(attrID) references ps_config_attributes(ID),
            foreign key(optID) references ps_config_options (ID),
            foreign key(descriptionTypeID) references ps_config_option_description_type (ID)
        )');
    }

    public function down()
    {
        $this->query('drop table if exists ps_alternative_options_filter');
        $this->query('alter table ps_products_types drop column useAlternatives');
    }
}
