<?php

namespace DreamSoft\Models\Offer;

use DreamSoft\Core\Model;

class MultiVolumeOffer extends Model
{

    /**
     * MultiVolumeOffer constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->prefix = 'dp_';
        $this->setTableName('multi_volume_offer', true);
    }

}
