<?php


use Phinx\Migration\AbstractMigration;

class SortPriceTypes extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_priceTypes 
    add column `order` int unsigned not null after ID,
    add column unit varchar(10) not null after `function`;');
        $this->query("update ps_config_priceTypes set `order`=1, name='Przeloty (wszystkie arkusze)', unit='ark.' where `function`='sheet';
update ps_config_priceTypes set `order`=2, name='Przeloty (każdy arkusz osobno)', unit='ark.' where `function`='every_sheet_separate';
update ps_config_priceTypes set `order`=3, name='Przeloty (wszystkie arkusze – przedział cenowy dla nakładu)', unit='ark.' where `function`='allSheetsRangeVolume';
update ps_config_priceTypes set `order`=4, name='Przeloty (wszystkie arkusze - cena dla nakładu)', unit='ark.' where `function`='allSheetsVolumes';
update ps_config_priceTypes set `order`=5, name='Komplety blach (ilość arkuszy drukarskich)', unit='szt.' where `function`='projectSheets';
update ps_config_priceTypes set `order`=6, name='Wszystkie strony', unit='str.' where `function`='allPages';
update ps_config_priceTypes set `order`=7, name='Wszystkie strony (przedział cenowy dla nakładu)', unit='str.' where `function`='allPagesRangeVolume';
update ps_config_priceTypes set `order`=8, name='Sztuki produktu (cena dla jednostki)', unit='szt.' where `function`='set';
update ps_config_priceTypes set `order`=9, name='Sztuki produktu (przedział cenowy dla arkuszy)', unit='szt.' where `function`='setRangeSheet';
update ps_config_priceTypes set `order`=10, name='Sztuki produktu (przedział dla objętości w mm)', unit='szt.' where `function`='setRangeSize';
update ps_config_priceTypes set `order`=11, name='Sztuki produktu (cena procentowa)', unit='szt.' where `function`='setMultiplication';
update ps_config_priceTypes set `order`=12, name='Sztuki produktu (przedział cenowy dla ilości stron)', unit='szt.' where `function`='setRangePages';
update ps_config_priceTypes set `order`=13, name='Sztuki produktu (cena dla nakładu)', unit='szt.' where `function`='setVolumes';
update ps_config_priceTypes set `order`=14, name='Ilość wszystkich użytków', unit='szt.' where `function`='alluzytki';
update ps_config_priceTypes set `order`=15, name='Metry kwadratowe', unit='m²' where `function`='squareMeter';
update ps_config_priceTypes set `order`=16, name='Metry kwadratowe zużytego materiału', unit='m²' where `function`='totalArea';
update ps_config_priceTypes set `order`=17, name='Metry kwadratowe dla formatu netto', unit='m²' where `function`='squareMeterNet';
update ps_config_priceTypes set `order`=18, name='Metry kwadratowe dla stron', unit='m²' where `function`='squareMetersForPages';
update ps_config_priceTypes set `order`=19, name='Powierzchnia zużytych arkuszy', unit='m²' where `function`='totalSheetsArea';
update ps_config_priceTypes set `order`=20, name='Powierzchnia zużytych arkuszy (przedział dla arkuszy)', unit='m²' where `function`='totalSheetsAreaRangeSheets';
update ps_config_priceTypes set `order`=21, name='Obwód w metrach', unit='mb' where `function`='perimeter';
update ps_config_priceTypes set `order`=22, name='Obwód netto w metrach', unit='mb' where `function`='net_perimeter';
update ps_config_priceTypes set `order`=23, name='Długość w m po dłuższym boku', unit='mb' where `function`='longSide';
update ps_config_priceTypes set `order`=24, name='Długość w m po krótszym boku', unit='mb' where `function`='shortSide';
update ps_config_priceTypes set `order`=25, name='Długość wszystkich użytków w metrach', unit='mb' where `function`='allAreasLength';
update ps_config_priceTypes set `order`=26, name='Długość w metrach dla szerokości', unit='mb' where `function`='lengthForWidth';
update ps_config_priceTypes set `order`=27, name='Długość w metrach dla wysokości', unit='mb' where `function`='lengthForHeight';
update ps_config_priceTypes set `order`=28, name='Ilość farby w litrach (przedział cenowy dla nakładu)', unit='l' where `function`='paintRangeVolume';
update ps_config_priceTypes set `order`=29, name='Ilość wszystkich falców', unit='szt.' where `function`='folds';
update ps_config_priceTypes set `order`=30, name='Zbieranie po falcowaniu', unit='ark.' where `function`='collectingFolds';
update ps_config_priceTypes set `order`=31, name='Ilość wzorów (suma)', unit='szt.' where `function`='amount_patterns_sum';
update ps_config_priceTypes set `order`=32, name='Ilość wzorów (wartość)', unit='szt.' where `function`='amount_patterns_value';
update ps_config_priceTypes set `order`=33, name='Cena procentowa', unit='%' where `function`='setPercentage';
update ps_config_priceTypes set `order`=34, name='Pakiet', unit='szt.' where `function`='bundle';
update ps_config_priceTypes set `order`=35, name='Paczka', unit='szt.' where `function`='package';
update ps_config_priceTypes set `order`=36, name='Cięcie na ostro', unit='ark.' where `function`='cutSharp';
update ps_config_priceTypes set `order`=37, name='Cięcie z wycinką', unit='ark.' where `function`='cutClipping';

");
    }
    public function down()
    {
        $this->query('alter table ps_config_priceTypes drop column `order`, drop column unit;');
    }
}
