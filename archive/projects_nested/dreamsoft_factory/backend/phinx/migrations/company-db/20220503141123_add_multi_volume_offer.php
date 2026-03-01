<?php


use Phinx\Migration\AbstractMigration;

class AddMultiVolumeOffer extends AbstractMigration
{

    public function up()
    {
        $this->query('create table dp_multi_volume_offer(
                        ID int primary key,
                        productID int,
                        foreign key(productID) references dp_products(ID)
        )');

        $this->query('create table dp_multi_volume_offer_calc(
            ID int primary key,
            multiVolumeOfferID int,
            calcID int,
            foreign key(calcID) references ps_user_calc(ID),
            foreign key(multiVolumeOfferID) references dp_multi_volume_offer(ID)
        )');
    }

    public function down()
    {
        $this->query('drop table if exists dp_multi_volume_offer');
        $this->query('drop table if exists dp_multi_volume_offer_calc');
    }
}
