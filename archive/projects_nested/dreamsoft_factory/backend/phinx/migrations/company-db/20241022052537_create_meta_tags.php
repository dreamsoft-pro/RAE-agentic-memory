<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class CreateMetaTags extends AbstractMigration
{
    public function change()
    {
        $tableName = 'dp_metatags';

        $existingColumns = [
            'ID' => ['type' => 'integer', 'limit' => 11, 'null' => false, 'identity' => true],
            'groupID' => ['type' => 'integer', 'limit' => 11, 'null' => true],
            'typeID' => ['type' => 'integer', 'limit' => 11, 'null' => true],
            'catID' => ['type' => 'integer', 'limit' => 11, 'null' => true],
            'subcatID' => ['type' => 'integer', 'limit' => 11, 'null' => true],
            'title' => ['type' => 'string', 'limit' => 255, 'null' => true],
            'description' => ['type' => 'text', 'null' => true],
            'keywords' => ['type' => 'string', 'limit' => 255, 'null' => true],
            'lang' => ['type' => 'string', 'limit' => 4, 'null' => false],
        ];

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
                        'null'  => $options['null'],
                        'default' => $options['default'] ?? null,
                    ]);
                }
            }

            $table->update();
        } else {
            // Define table options
            $table = $this->table($tableName, [
                'id' => false,
                'primary_key' => ['ID'],
                'engine' => 'InnoDB',
                'charset' => 'utf8',
            ]);

            foreach ($existingColumns as $columnName => $options) {
                $columnOptions = [
                    'limit' => $options['limit'],
                    'null'  => $options['null'],
                ];

                // Include 'identity' option for primary key
                if (isset($options['identity']) && $options['identity'] === true) {
                    $columnOptions['identity'] = true;
                }

                $table->addColumn($columnName, $options['type'], $columnOptions);
            }

            // Add OG and Twitter columns
            foreach ($ogColumns as $columnName => $options) {
                $table->addColumn($columnName, $options['type'], [
                    'limit'   => $options['limit'],
                    'null'    => $options['null'],
                    'default' => $options['default'] ?? null,
                ]);
            }

            // Add indexes
            $table->addIndex(['ID'], ['unique' => true]);

            // Create the table
            $table->create();
        }
    }
}
