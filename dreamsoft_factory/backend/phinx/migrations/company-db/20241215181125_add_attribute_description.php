<?php

use Phinx\Migration\AbstractMigration;

class AddAttributeDescription extends AbstractMigration
{
    public function up()
    {
        $this->table('ps_config_attribute_description_lang')
            ->addColumn('attributeID', 'integer', [
                'null' => false,
            ])
            ->addColumn('lang', 'string', [
                'limit' => 3,
                'null' => false
            ])
            ->addColumn('description', 'text', [
                'null' => true
            ])
            ->addForeignKey('attributeID', 'ps_config_attributes', 'ID', [
                'delete' => 'cascade',
                'update' => 'NO_ACTION'
            ])
            ->addIndex(['attributeID', 'lang'], [
                'unique' => true,
                'name' => 'unique_attrID_lang'
            ])
            ->create();
    }

    public function down()
    {
        $this->query('drop table if exists ps_config_attribute_description_lang');
    }
}
