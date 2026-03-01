<?php

namespace DreamSoft\Models\PrintShop;

use DreamSoft\Core\Model;

/**
 * Class PrintShop
 * @package DreamSoft\Controllers\PrintShop
 */
class PrintShop extends Model
{
    /**
     * @var int|null
     */
    protected $groupID = null;
    /**
     * @var int|null
     */
    protected $typeID = null;
    /**
     * @var int|null
     */
    protected $formatID = null;
    /**
     * @var int|null
     */
    protected $attrID = null;
    /**
     * @var int|null
     */
    protected $optID = null;
    /**
     * @var int|null
     */
    protected $controllerID = null;
    /**
     * @var int|null
     */
    public $volume = null;
    /**
     * @var
     */
    public $calcInfo;

    protected $domainID;

    /**
     * PrintShop constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->prefix = 'ps_';
    }

    /**
     * @param int $id
     * @return void
     */
    public function setGroupID($id): void
    {
        $this->groupID = $id;
    }

    /**
     * @return int|null
     */
    public function getGroupID(): ?int
    {
        return $this->groupID;
    }

    /**
     * @param int $ID
     * @return void
     */
    public function setTypeID($ID): void
    {
        $this->typeID = $ID;
    }

    /**
     * @return int|null
     */
    public function getTypeID(): ?int
    {
        return $this->typeID;
    }

    /**
     * @param int $volume
     * @return void
     */
    public function setVolume($volume): void
    {
        $this->volume = $volume;
    }

    /**
     * @return int|null
     */
    public function getVolume(): ?int
    {
        return $this->volume;
    }

    /**
     * @param int $id
     * @return void
     */
    public function setAttrID($id): void
    {
        $this->attrID = $id;
    }

    /**
     * @return int|null
     */
    public function getAttrID(): ?int
    {
        return $this->attrID;
    }

    /**
     * @param int $id
     * @return void
     */
    public function setOptID($id): void
    {
        $this->optID = $id;
    }

    /**
     * @return int|null
     */
    public function getOptID(): ?int
    {
        return $this->optID;
    }

    /**
     * @param int $id
     * @return void
     */
    public function setControllerID($id): void
    {
        $this->controllerID = $id;
    }

    /**
     * @return int|null
     */
    public function getControllerID(): ?int
    {
        return $this->controllerID;
    }

    /**
     * @param int $id
     * @return void
     */
    public function setFormatID($id): void
    {
        $this->formatID = $id;
    }

    /**
     * @return int|null
     */
    public function getFormatID(): ?int
    {
        return $this->formatID;
    }

    /**
     * @return int|null
     */
    public function getDomainID(): ?int
    {
        return $this->domainID;
    }

    /**
     * @param int $domainID
     * @return void
     */
    public function setDomainID($domainID): void
    {
        $this->domainID = $domainID;
    }
}
