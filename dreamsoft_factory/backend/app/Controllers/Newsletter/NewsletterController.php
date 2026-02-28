<?php
namespace DreamSoft\Controllers\Newsletter;


use DreamSoft\Core\Controller;
use DreamSoft\Controllers\Components\QueryFilter;
use DreamSoft\Models\Newsletter\NewsletterRecipient;
use DreamSoft\Controllers\Components\ExportImport;

class NewsletterController extends Controller
{

    public $useModels = array();

    /**
     * @var NewsletterRecipient
     */
    protected $NewsletterRecipient;
    /**
     * @var ExportImport
     */
    protected $ExportImport;
    /**
     * @var QueryFilter
     */
    protected $QueryFilter;
    /**
     * @var array
     */
    protected $configs;

    /**
     * CouponsController constructor.
     * @param array $params
     */
    public function __construct($params)
    {
        parent::__construct($params);
        $this->NewsletterRecipient = NewsletterRecipient::getInstance();
        $this->ExportImport = ExportImport::getInstance();
    }

    /**
     * @return mixed
     */
    public function index()
    {        

        return $this->NewsletterRecipient->getAll();
    }

    public function export()
    {
        $exportData = $this->NewsletterRecipient->getAll();

        $exportDataHead[0]['ID'] = 'ID';
        $exportDataHead[0]['email'] = 'E-mail';
        $exportDataHead[0]['agreement'] = 'Zgoda';
        $exportDataHead[0]['domainID'] = 'ID domeny';
        $exportDataHead[0]['created'] = 'Wpisano';
        $exportDataHead[0]['modified'] = 'Zmodyfikowano';

        $exportArrayData = array_merge($exportDataHead, $exportData);
        //exporting $data data to file and download
        $dir = companyID . '/download/';
        if (!is_dir(STATIC_PATH . $dir)) {
            mkdir(STATIC_PATH . $dir, 0777, true);
        }
        $path1 = $dir . 'newsletter__' . date('Y-m-d_G-i') . '.xls';
        $this->getExportImport()->newSheet('Newsletter');
        $this->getExportImport()->setFromArray($exportArrayData);
        $this->getExportImport()->path = STATIC_PATH . $path1;
        $this->getExportImport()->saveFile();
		
        return array('response' => true, 'url' => STATIC_URL . $path1);
    }

    protected function getExportImport()
    {
        return $this->ExportImport;
    }
}