<?php

namespace DreamSoft\Models\Margin;

use DreamSoft\Core\Model;

class MarginSupplier extends Model
{
    public function __construct($root = false, $companyID = NULL)
    {
        $this->setTableName('margins_supplier', true);
        parent::__construct($root, $companyID);
    }

    public function findMargin($suppliers)
    {
        $suppliers = array_filter($suppliers, function ($item) {
            return !empty(trim($item));
        });

        if (empty($suppliers)) {
            return 0;
        }

        $suppliers = array_map(function ($item) {
            return '"' . trim($item) . '"';
        }, $suppliers);

        $suppliers = join(',', $suppliers);
        $query = "select percentage from dp_margins_supplier where supplierName in ($suppliers) limit 1;";
        $this->db->exec($query);
        return $this->db->getOne();
    }
}
