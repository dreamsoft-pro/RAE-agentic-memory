<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class CreateMainMetaTags extends AbstractMigration
{
    public function change()
    {
        $tableName = 'dp_mainMetaTagLanguages';
        $ogColumns = [
            'og_title' => ['type' => 'string', 'limit' => 255, 'null' => true],
            'og_url' => ['type' => 'string', 'limit' => 255, 'null' => true],
            'og_site_name' => ['type' => 'string', 'limit' => 255, 'null' => true],
            'og_description' => ['type' => 'text', 'limit' => 2048, 'null' => true],
            'og_locale' => ['type' => 'string', 'limit' => 10, 'null' => true],
            'imageID' => ['type' => 'integer', 'limit' => 11, 'null' => true],
            'og_image_width' => ['type' => 'integer', 'limit' => 11, 'null' => true],
            'og_image_height' => ['type' => 'integer', 'limit' => 11, 'null' => true],
            'og_image_alt' => ['type' => 'string', 'limit' => 255, 'null' => true],
            'twitter_card' => ['type' => 'string', 'limit' => 64, 'null' => true],
            'twitter_site' => ['type' => 'string', 'limit' => 255, 'null' => true],
            'twitter_creator' => ['type' => 'string', 'limit' => 64, 'null' => true],
        ];

        if ($this->hasTable($tableName)) {
            $table = $this->table($tableName);

            foreach ($ogColumns as $columnName => $options) {
                if (!$table->hasColumn($columnName)) {
                    $table->addColumn($columnName, $options['type'], [
                        'limit' => $options['limit'],
                        'null' => $options['null'],
                        'default' => $options['default'] ?? null,
                    ]);
                }
            }

            // Apply the changes to the existing table
            $table->update();
        } else {
            $table = $this->table($tableName, [
                'id' => false,
                'primary_key' => ['ID'],
                'engine' => 'InnoDB',
                'charset' => 'utf8',
            ]);

            // Original columns
            $table->addColumn('ID', 'integer', ['identity' => true, 'null' => false])
                ->addColumn('mainMetaTagID', 'integer', ['limit' => 11, 'null' => false])
                ->addColumn('lang', 'string', ['limit' => 4, 'null' => false])
                ->addColumn('title', 'string', ['limit' => 400, 'null' => false])
                ->addColumn('description', 'text', ['null' => true])
                ->addColumn('keywords', 'string', ['limit' => 400, 'null' => true]);

            foreach ($ogColumns as $columnName => $options) {
                $table->addColumn($columnName, $options['type'], [
                    'limit' => $options['limit'],
                    'null' => $options['null'],
                    'default' => $options['default'] ?? null,
                ]);
            }

            $table->addIndex(['ID'], ['unique' => true])
                ->addIndex(['mainMetaTagID']);

            $table->create();
        }
    }
}
