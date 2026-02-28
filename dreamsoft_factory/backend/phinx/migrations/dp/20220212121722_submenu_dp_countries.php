<?php


use Phinx\Migration\AbstractMigration;

class SubmenuDpCountries extends AbstractMigration
{

    public function up()
    {
        $this->query("INSERT INTO `dp_subMenu` (`menuID`, `key`, `controller`, `action`, `package`, `path`, `title`, `active`) VALUES
            (2, 'supported-countries', 'Menu', 'shopSupportedCountries', NULL, 'shop/supportedCountries/', 'supported-countries', 1);");        
    }
    public function down()
    {
        //can be rolled back manually
    }
}
