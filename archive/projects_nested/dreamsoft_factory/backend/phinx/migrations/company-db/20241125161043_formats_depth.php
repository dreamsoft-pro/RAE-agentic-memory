<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class FormatsDepth extends AbstractMigration
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
        $tableName = 'ps_products_formats';
        $table = $this->table($tableName);
        $table->addColumn('depth', 'integer', ['null' => true, 'default' => 0, 'signed' => false])
            ->update();


        //add custom format
        $tableName = 'ps_products_customFormat';

        $table = $this->table($tableName);




        $table->addColumn('minDepth', 'integer', ['null' => true, 'default' => Null, 'signed' => false])
            ->update();
        $table->addColumn('maxDepth', 'integer', ['null' => true, 'default' => Null, 'signed' => false])
            ->update();
        $table->addColumn('depthStep', 'integer', ['null' => false, 'default' => 1, 'signed' => false])
            ->update();
        $table->addColumn('widthStep', 'integer', ['null' => false, 'default' => 1, 'signed' => false])
            ->update();
        $table->addColumn('heightStep', 'integer', ['null' => false, 'default' => 1, 'signed' => false])
            ->update();
    }
}
