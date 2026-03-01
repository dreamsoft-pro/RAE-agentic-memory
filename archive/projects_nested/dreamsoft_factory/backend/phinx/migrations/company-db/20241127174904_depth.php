<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class Depth extends AbstractMigration
{
    /**
     * Change Method.
     *
     * Write your reversible migrations using this method.
     *
     * More information on writing migrations is available here:
     * https://book.cakephp.org/phinx/0/en/migrations.html#the-change-method
     *
     * Remember to call "create()" or "update()" and NOT "save()" when working
     * with the Table class.
     */
    public function change(): void
    {
        $table = $this->table('ps_products_formats');

        // Renaming columns
        if ($table->hasColumn('slopeExternalFront')) {
            $table->renameColumn('slopeExternalFront', 'slopeExternalLeft');
        }

        if ($table->hasColumn('slopeExternalBack')) {
            $table->renameColumn('slopeExternalBack', 'slopeExternalRight');
        }

        $table->update();
        // add 'slopeExternalFront'
        $table->addColumn('slopeExternalFront', 'integer', ['null' => true, 'default' => Null, 'signed' => false])
            ->update();
        $table->addColumn('slopeExternalBack', 'integer', ['null' => true, 'default' => Null, 'signed' => false])
            ->update();
    }
}
