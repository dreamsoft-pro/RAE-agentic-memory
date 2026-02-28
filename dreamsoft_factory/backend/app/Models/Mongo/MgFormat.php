<?php

namespace DreamSoft\Models\Mongo;

use DreamSoft\Core\MongoModel;
use Exception;
use MongoCollection;
class MgFormat extends MongoModel {

    /**
     * @var MongoCollection
     */
    private $collection;
    public function __construct() {
        parent::__construct();
        try {
            $this->collection = $this->db->selectCollection('Format');
        } catch (Exception $e) {
            $this->debug('Collection Format problem!', $e->getMessage());
        }

    }

    /**
     * @return MongoCollection
     */
    public function getAdapter()
    {
        return $this->collection;
    }

}
