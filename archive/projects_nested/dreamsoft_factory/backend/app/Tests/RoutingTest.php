<?php

use PHPUnit\Framework\TestCase;
class RoutingTest extends TestCase
{

    private $instance;

    public function setUp():void
    {
        global $_SERVER;
        $_SERVER['REQUEST_URI']='/';
        $_SERVER['REQUEST_METHOD']='get';
        $this->instance = new \DreamSoft\Libs\Routing();
    }

    /**
     * @dataProvider parseUriData
     */
    public function testParseUri($uri,$package,$controller,$action=null)
    {
        $_SERVER['REQUEST_URI']=$uri;
        $this->instance->parseUri();
        $this->assertSame($package,$this->instance->getPackage());
        $this->assertSame($controller,$this->instance->getController());
        if($action){
            $this->assertSame($action,$this->instance->getAction());
        }
    }

    /**
     * @return array of [url, resolved package, resolved controller]
     */
    public function parseUriData()
    {
        return [
            ['/ps_attributes/1/ps_options/514/increaseControllers/1/ps_config_increases','printshop_config','IncreasesConfigController']
            ,['/ps_attributes/1/ps_options/514/increaseControllers/0/ps_config_related_increases_count', 'printshop_config','IncreasesConfigController']
            ,['/ps_attributes/1/ps_options/514/efficiency/1', 'printshop_config','EfficiencyConfigController','index']
            ,['/ps_attributes/1/ps_options/514/efficiency/1/speeds', 'printshop_config','EfficiencyConfigController','speeds']
            ,['/ps_attributes/1/ps_options/514/efficiency/1/speeds/1', 'printshop_config','EfficiencyConfigController','speeds']
            ,['/ps_attributes/1/ps_options/514/efficiency//speeds/1', 'printshop_config','EfficiencyConfigController','speeds']
        ];
    }
}
