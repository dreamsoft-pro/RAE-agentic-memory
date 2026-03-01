<?php


use Phinx\Migration\AbstractMigration;

class SubmenuMargins extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_subMenu` (`menuID`, `key`, `controller`, `action`, `package`, `path`, `title`, `active`) VALUES
            (3, 'margins', 'Menu', 'printshopMargins', NULL, 'printshop/margins/', 'margins', 1);");        
    }
    public function down()
    {
        //can be rolled back manually
    }
}
