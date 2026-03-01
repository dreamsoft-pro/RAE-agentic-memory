<?php

namespace DreamSoft\Tests;

require_once 'helpers.php';

use DreamSoft\Controllers\Components\CalculateAdapter;
use PHPUnit\Framework\TestCase;

class CalculateAdapterTest extends TestCase
{
    /**
     * @var CalculateAdapter
     */
    private $CalculateAdapter;

    function getAreaPerSheetForStandardProvider()
    {
        return [
            [100, 200, 100, 200, 'none', ['max' => 1, 'shortSide' => 1, 'longSide' => 1, 'isHorizontalWidth' => true, 'formatWidth'=>100, 'formatHeight'=>200]],
            [100, 200, 100, 200, '', ['max' => 1, 'shortSide' => 1, 'longSide' => 1, 'isHorizontalWidth' => true, 'formatWidth'=>100, 'formatHeight'=>200]],
            [100, 200, 100, 100, '', ['max' => 2, 'shortSide' => 1, 'longSide' => 2, 'isHorizontalWidth' => true, 'formatWidth'=>100, 'formatHeight'=>100]],
            [200, 100, 100, 100, '', ['max' => 2, 'shortSide' => 1, 'longSide' => 2, 'isHorizontalWidth' => true, 'formatWidth'=>100, 'formatHeight'=>100]],
            [200, 100, 50, 100, '', ['max' => 4, 'shortSide' => 1, 'longSide' => 4, 'isHorizontalWidth' => true, 'formatWidth'=>50, 'formatHeight'=>100]],
            [200, 100, 55, 100, '', ['max' => 3, 'shortSide' => 1, 'longSide' => 3, 'isHorizontalWidth' => true, 'formatWidth'=>55, 'formatHeight'=>100]],
            [200, 100, 50, 100, 'glue', ['max' => 4, 'shortSide' => 1, 'longSide' => 4, 'isHorizontalWidth' => true, 'formatWidth'=>50, 'formatHeight'=>100]],
            [250, 100, 50, 100, 'spiral', ['max' => 5, 'shortSide' => 1, 'longSide' => 5, 'isHorizontalWidth' => true, 'formatWidth'=>50, 'formatHeight'=>100]],
            [250, 100, 45, 100, 'glue', ['max' => 5, 'shortSide' => 1, 'longSide' => 5, 'isHorizontalWidth' => true, 'formatWidth'=>45, 'formatHeight'=>100]],
            [250, 100, 45, 100, 'sewn', ['max' => 5, 'shortSide' => 1, 'longSide' => 5, 'isHorizontalWidth' => true, 'formatWidth'=>45, 'formatHeight'=>100]],
            [250, 100, 45, 100, 'sewn', ['max' => 5, 'shortSide' => 1, 'longSide' => 5, 'isHorizontalWidth' => true, 'formatWidth'=>45, 'formatHeight'=>100]],
            [320, 480, 214, 301, 'sewn', ['max' => 2, 'shortSide' => 1, 'longSide' => 2, 'isHorizontalWidth' => false, 'formatWidth'=>214, 'formatHeight'=>301]],
        ];
    }

    /**
     * @dataProvider getAreaPerSheetForStandardProvider
     */
    public function testgetAreaPerSheetForStandard($workspaceWidth,
                                                   $workspaceHeight,
                                                   $formatWidth,
                                                   $formatHeight,
                                                   $binding,
                                                   $expected)
    {
        $result = $this->CalculateAdapter->getAreaPerSheetForStandard($workspaceWidth, $workspaceHeight, $formatWidth,
            $formatHeight, ['binding'=>$binding]);
        self::assertEquals($expected, $result, "For binding {$binding}");
    }

    protected function setUp(): void
    {
        $this->CalculateAdapter = new CalculateAdapter();
    }
}

