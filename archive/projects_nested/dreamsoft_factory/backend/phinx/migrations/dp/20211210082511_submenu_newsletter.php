<?php


use Phinx\Migration\AbstractMigration;

class SubmenuNewsletter extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_subMenu` (`menuID`, `key`, `controller`, `action`, `package`, `path`, `title`, `active`) VALUES
            (5, 'newsletter', 'Menu', 'customerServiceNewsletter', NULL, NULL, 'newsletter', 1);");        
    }
    public function down()
    {
        //can be rolled back manually
    }
}
