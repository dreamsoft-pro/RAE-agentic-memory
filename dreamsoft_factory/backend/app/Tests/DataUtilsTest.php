<?php
use PHPUnit\Framework\TestCase;
use DreamSoft\Libs\DataUtils;
class DataUtilsTest extends TestCase{
    function linearApproximationData(){
        return [
            [[],1,0],
            [false,1,0],
            [[['value'=>1, 'volume'=>1],['value'=>3, 'volume'=>3]],2,2],
            [[['value'=>2, 'volume'=>1],['value'=>3, 'volume'=>3]],0,0],
            [[['value'=>1, 'volume'=>1],['value'=>3, 'volume'=>3]],1,1],
            [[['value'=>1, 'volume'=>1],['value'=>3, 'volume'=>3]],4,3],
            [[['value'=>1, 'volume'=>1],['value'=>3, 'volume'=>3],['value'=>4, 'volume'=>4]],4,4],
            [[['value'=>1, 'volume'=>1],['value'=>3, 'volume'=>3],['value'=>4, 'volume'=>4]],0,0],
        ];
    }

    /**
     * @dataProvider linearApproximationData
     */
    public function testLinearApproximation($array,$volume, $expected){
        $result= DataUtils:: linearApproximation($array,$volume);
        self::assertEquals($expected, $result);
    }
    function uniqueRecordsData(){
        return [
            [[['id'=>1],['id'=>1]],'id',[1]],
            [[['id'=>1,'key'=>1],['id'=>1,'key'=>1]],['id','key'],[1]],
            [[],'id',[]],
        ];
    }
    /**
     * @dataProvider uniqueRecordsData
     */
    public function testUniqueRecords($input,$onField, $result){
        $records=DataUtils::uniqueRecords($input,$onField);
        $records=array_map(function($item){
            return $item['id'];
        },$records);
        self::assertEquals($result,$records);
    }
}
