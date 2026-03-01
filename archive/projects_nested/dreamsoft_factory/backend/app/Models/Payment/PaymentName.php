<?php


namespace DreamSoft\Models\Payment;

use DreamSoft\Core\Model;

/**
 * Class PaymentName
 */
class PaymentName extends Model
{

    /**
     * PaymentName constructor.
     */
    public function __construct()
    {
        parent::__construct();
        $this->prefix = 'dp_config_';
        $this->setTableName('paymentNames', true);
    }

    public function getByPaymentIDAndLang($paymentID, $lang)
    {
        $query = 'SELECT name 
		    FROM `' . $this->getTableName() . '`
    		WHERE paymentID = :paymentID AND lang = :lang';
            

        $binds['paymentID'] = $paymentID;
        $binds['lang'] = $lang;

        if (!$this->db->exec($query, $binds)) {
            return false;
        }

        return $this->db->getAll();
    }
}