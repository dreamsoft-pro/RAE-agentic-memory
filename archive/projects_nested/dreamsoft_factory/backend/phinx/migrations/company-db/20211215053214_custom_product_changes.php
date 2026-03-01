<?php


use Phinx\Migration\AbstractMigration;

class CustomProductChanges extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table  dp_customProducts 
                            add column calcID int null after orderID,
                            add constraint fk_ps_user_calc_ID foreign key (calcID) references  ps_user_calc(ID)');
    }

    public function down()
    {
        $this->query('alter table  dp_customProducts 
                            drop foreign key fk_ps_user_calc_ID,
                            drop column calcID');
    }
}
