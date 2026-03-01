<?php

use DreamSoft\Models\PrintShopConfig\PrintShopConfigEfficiencySideRelations;
use DreamSoft\Models\PrintShopConfig\PrintShopConfigEfficiencySpeedChanges;
use DreamSoft\Models\ProductionPath\DeviceSideRelations;
use DreamSoft\Models\ProductionPath\DeviceSpeedChange;
use PHPUnit\Framework\TestCase;
use DreamSoft\Controllers\Components\CalculatorDevices;

require_once 'helpers.php';

class CalculatorDevicesTest extends TestCase
{
    /**
     * @var CalculatorDevices
     */
    public $instance;

    public function setUp(): void
    {

        $this->instance = CalculatorDevices::getInstance();

    }

    function deviceData(): array
    {
        return [
            [['sheets' => 1000, 'speedForVolume' => 6000, 'priceForWork' => 300, 'deviceTime' => 10, 'thickness' => 0.09, 'stackHeight' => null, 'printedStackHeight' => 0, 'transportTime' => null],
                ['devicePrice' => 10000, 'deviceExpense' => 0, 'deviceTime' => 1200]]
            , [['sheets' => 1000, 'speedForVolume' => 6000, 'priceForWork' => 300, 'deviceTime' => 10, 'thickness' => 0.09, 'stackHeight' => 10, 'printedStackHeight' => 20, 'transportTime' => 10],
                ['devicePrice' => 15000, 'deviceExpense' => 0, 'deviceTime' => 1800]
                , ['name' => 'speedChange', 'sheets' => 1000, 'speedForVolume' => 6000, 'priceForWork' => 300,
                    'deviceTime' => 10, 'thickness' => 0.09, 'stackHeight' => null, 'printedStackHeight' => 0, 'transportTime' => null],
                ['devicePrice' => 10000, 'deviceExpense' => 0, 'deviceTime' => 1200]]
        ];
    }



    /**
     * @dataProvider deviceData
     */
    public function testgetDeviceDetails($data, $expected): void
    {
        $sheets = $data['sheets'];
        $speedForVolume = $data['speedForVolume'];
        $priceForAmount = $data['priceForWork'] * $sheets / $speedForVolume;
        $deviceTime = $data['deviceTime'];

        $OperationOptionStub = $this->createMock(\DreamSoft\Models\ProductionPath\OperationOption::class);
        $OperationOptionStub->method('getSelectedOperations')
            ->willReturn(['12' => ['operationID' => '12']]);
        setNotPubField($this->instance, 'OperationOption', $OperationOptionStub);

        $OperationDeviceStub = $this->createMock(\DreamSoft\Models\ProductionPath\OperationDevice::class);
        $OperationDeviceStub->method('getSelectedDevices')
            ->willReturn(['1']);
        setNotPubField($this->instance, 'OperationDevice', $OperationDeviceStub);

        $DeviceSpeedStub = $this->createMock(\DreamSoft\Models\ProductionPath\DeviceSpeed::class);
        $DeviceSpeedStub->method('getSpeedForVolume')
            ->willReturn($speedForVolume);
        setNotPubField($this->instance, 'DeviceSpeed', $DeviceSpeedStub);

        $DevicePriceStub = $this->createMock(\DreamSoft\Models\ProductionPath\DevicePrice::class);
        $DevicePriceStub->method('getPriceForAmount')
            ->willReturn($priceForAmount);
        $DevicePriceStub->method('getExpenseForAmount')
            ->willReturn(0);
        setNotPubField($this->instance, 'DevicePrice', $DevicePriceStub);

        $DeviceStub = $this->createMock(\DreamSoft\Models\ProductionPath\Device::class);
        $DeviceStub->method('get')
            ->willReturn(['deviceTime' => $deviceTime, 'workUnit' => 'sheet', 'stackHeight' => $data['stackHeight'], 'printedStackHeight' => $data['printedStackHeight'], 'transportTime' => $data['transportTime']]);
        setNotPubField($this->instance, 'Device', $DeviceStub);

        $DeviceSpeedChangeStub = $this->createMock(DeviceSpeedChange::class);
        $DeviceSpeedChangeStub->method('getOrderedList')
            ->willReturn([]);
        setNotPubField($this->instance, 'DeviceSpeedChange', $DeviceSpeedChangeStub);

        $PrintShopConfigEfficiencySpeedChangesStub = $this->createMock(PrintShopConfigEfficiencySpeedChanges::class);
        $PrintShopConfigEfficiencySpeedChangesStub->method('getOrderedList')
            ->willReturn([]);
        setNotPubField($this->instance, 'PrintShopConfigEfficiencySpeedChanges', $PrintShopConfigEfficiencySpeedChangesStub);

        $DeviceSpeedChangeStub = $this->createMock(DeviceSpeedChange::class);
        $DeviceSpeedChangeStub->method('getOrderedList')
            ->willReturn([]);
        setNotPubField($this->instance, 'DeviceSpeedChange', $DeviceSpeedChangeStub);

        $DeviceSideRelationsStub = $this->createMock(DeviceSideRelations::class);
        $DeviceSideRelationsStub->method('getOrderedList')
            ->willReturn([]);
        setNotPubField($this->instance, 'DeviceSideRelations', $DeviceSideRelationsStub);

        $PrintShopConfigEfficiencySideRelationsStub = $this->createMock(PrintShopConfigEfficiencySideRelations::class);
        $PrintShopConfigEfficiencySideRelationsStub->method('getOrderedList')
            ->willReturn([]);
        setNotPubField($this->instance, 'PrintShopConfigEfficiencySideRelations', $PrintShopConfigEfficiencySideRelationsStub);

        $result = $this->instance->calculateDeviceDetails(1, 2, 1, $sheets, $sheets, $sheets, $sheets, $data['thickness'], 0, 0, 1, 1, , , , , , , ,);// TODO Not mantained

        self::assertEquals($expected['devicePrice'], $result['devicePrice']);
        self::assertEquals($expected['deviceExpense'], $result['deviceExpense']);
        self::assertEquals($expected['deviceTime'], $result['deviceTime']);
    }
    function speedChangeData()
    {
        return [
            [
                [
                    [
                        ['grammageMin' => 1, 'grammageMax'=>2, 'efficiencyChange' => '-10']
                    ],
                    []
                ],
                ['grammage' => 1],
                ['factor' => 0.9]
            ],
            [
                [
                    [
                        ['grammageMin' => 1, 'grammageMax'=>2, 'stiffnessMin' => 1, 'stiffnessMax'=>2, 'thicknessMin' => 1, 'thicknessMax'=>2, 'efficiencyChange' => '-10']
                    ],
                    []
                ],
                ['grammage' => 1,'stiffness' => 1,'thickness' => 1],
                ['factor' => 0.729]
            ],
            [
                [
                    [
                        ['grammageMin' => 1, 'grammageMax'=>2, 'stiffnessMin' => 1, 'stiffnessMax'=>2, 'thicknessMin' => 1, 'thicknessMax'=>2, 'efficiencyChange' => '-10'],
                        ['thicknessMin' => 1, 'thicknessMax'=>2, 'efficiencyChange' => '-20']
                    ],
                    []
                ],
                ['grammage' => 1,'stiffness' => 1,'thickness' => 1],
                ['factor' => 0.648]
            ],
        [
                [
                    [
                        ['grammageMin' => 1, 'grammageMax'=>2, 'efficiencyChange' => '-10']
                    ],
                    [
                        ['grammageMin' => 1, 'grammageMax'=>2, 'efficiencyChange' => '-20']
                    ]
                ],
                ['grammage' => 1],
                ['factor' => 0.8]
            ],
        ];
    }
    /**
     * @dataProvider speedChangeData
     */
    public function testSpeedChange($config, $data, $expected){
        $DeviceSpeedChangeStub = $this->createMock(DeviceSpeedChange::class);
        $DeviceSpeedChangeStub->method('getOrderedList')
            ->willReturn($config[0]);
        setNotPubField($this->instance, 'DeviceSpeedChange', $DeviceSpeedChangeStub);

        $PrintShopConfigEfficiencySpeedChangesStub = $this->createMock(PrintShopConfigEfficiencySpeedChanges::class);
        $PrintShopConfigEfficiencySpeedChangesStub->method('getOrderedList')
            ->willReturn($config[1]);
        setNotPubField($this->instance, 'PrintShopConfigEfficiencySpeedChanges', $PrintShopConfigEfficiencySpeedChangesStub);

        $result = invokeNotPubMethod($this->instance, 'getSpeedChange', [$data['grammage'], $data['thickness'], $data['stiffness'], 0, 0, 0,0]);
        self::assertEqualsWithDelta($expected['factor'], $result,0.001);
    }
    function relationData()
    {
        return [
            [
                [
                    [
                        ['relation' => 1, 'efficiencyChange' => '-10']
                    ],
                    []
                ],
                ['width' => 1, 'height' => 1],
                ['factor' => 0.9]
            ],
            [
                [
                    [
                        ['relation' => 2, 'efficiencyChange' => '-10']
                    ],
                    []
                ],
                ['width' => 1, 'height' => 1],
                ['factor' => 1]
            ],
            [
                [
                    [
                        ['relation' => 2, 'efficiencyChange' => '-20'],
                        ['relation' => 1, 'efficiencyChange' => '-10']
                    ],
                    []
                ],
                ['width' => 1, 'height' => 2],
                ['factor' => .8]
            ]
        ];
    }
    /**
     * @dataProvider relationData
     */
    public function testSpeedChangeByRelation($config, $data, $expected)
    {
        $DeviceSideRelationsStub = $this->createMock(DeviceSideRelations::class);
        $DeviceSideRelationsStub->method('getOrderedListByRelation')
            ->willReturn($config[0]);
        setNotPubField($this->instance, 'DeviceSideRelations', $DeviceSideRelationsStub);

        $PrintShopConfigEfficiencySideRelationsStub = $this->createMock(PrintShopConfigEfficiencySideRelations::class);
        $PrintShopConfigEfficiencySideRelationsStub->method('getOrderedListByRelation')
            ->willReturn($config[1]);
        setNotPubField($this->instance, 'PrintShopConfigEfficiencySideRelations', $PrintShopConfigEfficiencySideRelationsStub);

        $result = invokeNotPubMethod($this->instance, 'getSpeedChangeByRelation', [$data['width'], $data['height'], 0, 0, 0, 0]);
        self::assertEquals($expected['factor'], $result);
    }
}
