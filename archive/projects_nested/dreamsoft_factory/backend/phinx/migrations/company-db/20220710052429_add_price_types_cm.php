<?php


use Phinx\Migration\AbstractMigration;

class AddPriceTypesCm extends AbstractMigration
{

    public function up()
    {
        $this->query('alter table ps_config_priceTypes change column name name varchar(120) not null');

        $names0 = preg_split("/\n/", 'Powierzchnia - metry kwadratowe,squareMeter
Powierzchnia - metry kwadratowe zużytego materiału,totalArea
Powierzchnia - metry kwadratowe dla formatu netto,squareMeterNet
Powierzchnia - metry kwadratowe dla stron,squareMetersForPages
Powierzchnia zużytych arkuszy w metrach kwadratowych,totalSheetsArea
Powierzchnia zużytych arkuszy w metrach kwadratowych (przedział dla arkuszy),totalSheetsAreaRangeSheets
Obwód w metrach,perimeter
Obwód netto w metrach,net_perimeter
Długość w m po dłuższym boku,longSide
Długość w m po krótszym boku,shortSide
Długość wszystkich użytków w metrach,allAreasLength
Długość w metrach dla szerokości,lengthForWidth
Długość w metrach dla wysokości,lengthForHeight');
        foreach ($names0 as $name) {
            $parts = preg_split('/,/', $name);
            $this->query("update ps_config_priceTypes set `name`='{$parts[0]}'  where `function`  = '{$parts[1]}'");
        }

        $names1 = preg_split("/\n/", 'Powierzchnia - centymetry kwadratowe,squareMeter
Powierzchnia - centymetry kwadratowe zużytego materiału,totalArea
Powierzchnia - centymetry kwadratowe dla formatu netto,squareMeterNet
Powierzchnia - centymetry kwadratowe dla stron,squareMetersForPages
Powierzchnia zużytych arkuszy w centymetrach kwadratowych,totalSheetsArea
Powierzchnia zużytych arkuszy w centymetrach kwadratowych (przedział dla arkuszy),totalSheetsAreaRangeSheets
Obwód w centymetrach,perimeter
Obwód netto w centymetrach,net_perimeter
Długość w cm po dłuższym boku,longSide
Długość w cm po krótszym boku,shortSide
Długość wszystkich użytków w centymetrach,allAreasLength
Długość w centymetrach dla szerokości,lengthForWidth
Długość w centymetrach dla wysokości,lengthForHeight');
        $names = [];
        foreach ($names1 as $name) {
            $parts = preg_split('/,/', $name);
            $names[$parts[1]] = $parts[0];
        }
        $existing = $this->fetchAll("select * from ps_config_priceTypes where `function`
            in ('squareMeter','perimeter','net_perimeter', 'longSide','shortSide','allAreasLength','totalArea','totalSheetsArea','totalSheetsAreaRangeSheets','lengthForWidth', 'lengthForHeight','squareMeterNet','squareMetersForPages') order by `order`");
        foreach ($existing as $current) {
            try {
                $orderQ = $this->fetchRow("select `order` from ps_config_priceTypes where `function`='{$current['function']}'");
                $this->query('update ps_config_priceTypes set `order`=`order` + 1 where `order` > ' . $orderQ['order']);
                $unit = $current['unit'] == 'm²' ? 'cm²' : 'cm';
                $this->query("insert into ps_config_priceTypes (name, `function`, `order`,unit) values
                                ('{$names[$current['function']]}','{$current['function']}_cm'," . ($orderQ['order'] + 1) . ",'{$unit}')");

            } catch (Exception $e) {
                echo "Processing {$current['function']}";
                throw $e;
            }

        }
    }

    public function down()
    {
    }
}
