<?php

/**
 * Kontroler konfiguracyjny
 * @class Config
 */

include_once(BASE_DIR . 'libs/SuperAdmin.php');
include_once BASE_DIR . 'libs/PHPExcel.php';
include_once BASE_DIR . 'libs/PHPExcel/IOFactory.php';

use DreamSoft\Libs\ConnectionSwitchFactory;
use DreamSoft\Libs\ConnectionUserFactory;
use DreamSoft\Models\Address\OldAddress;
use DreamSoft\Models\Group\Group;
use DreamSoft\Models\Module\Module;
use DreamSoft\Models\Module\ModuleKey;
use DreamSoft\Models\Module\ModuleValue;
use DreamSoft\Models\Payment\Payment;
use DreamSoft\Models\Currency\Currency;
use DreamSoft\Core\Controller;
use DreamSoft\Models\Setting\Setting;
use DreamSoft\Models\Template\Template;
use DreamSoft\Models\Template\TemplateSetting;
use DreamSoft\Models\Template\View;
use DreamSoft\Models\User\User;
use DreamSoft\Models\Domain\Domain;
use DreamSoft\Models\Domain\DomainRoot;
use DreamSoft\Models\Route\RouteLang;
use DreamSoft\Models\Route\Route;
use DreamSoft\Models\User\UserGroup;
use DreamSoft\Models\User\UserOption;
use DreamSoft\Models\Address\Address;
use DreamSoft\Models\Address\AddressUser;

class ConfigController extends Controller
{
    public $useModels = array();

    private $ssh;
    protected User $User;
    protected DomainRoot $DomainRoot;
    protected Domain $Domain;
    protected Route $Route;
    protected Route $RouteRemote;
    protected RouteLang $RouteLang;
    protected RouteLang $RouteLangRemote;
    protected View $View;
    protected View $ViewRemote;
    protected Setting $Setting;
    protected UserGroup $UserGroup;
    protected Group $Group;
    protected Template $Template;
    protected Module $Module;
    protected ModuleKey $ModuleKey;
    protected ModuleValue $ModuleValue;
    protected Payment $Payment;
    protected TemplateSetting $TemplateSetting;
    protected TemplateSetting $TemplateSettingRemote;
    protected SuperAdmin $SuperAdmin;
    protected ConnectionSwitchFactory $ConnectionSwitchFactory;
    protected Currency $Currency;
    protected Address $Address;
    protected AddressUser $AddressUser;
    protected UserOption $UserOption;
    protected OldAddress $OldAddress;
    protected $ExcelFile;

    public function __construct($params)
    {
        parent::__construct($params);
        $this->User = User::getInstance();
        $this->DomainRoot = DomainRoot::getInstance();
        $this->Domain = Domain::getInstance();
        $this->Route = Route::getInstance();
        $this->RouteRemote = new Route();
        $this->RouteLang = RouteLang::getInstance();
        $this->RouteLangRemote = new RouteLang();
        $this->View = View::getInstance();
        $this->ViewRemote = new View();
        $this->Setting = Setting::getInstance();
        $this->Setting->setModule('acl');
        $this->UserGroup = UserGroup::getInstance();
        $this->Group = Group::getInstance();
        $this->Template = Template::getInstance();
        $this->Module = Module::getInstance();
        $this->ModuleKey = ModuleKey::getInstance();
        $this->ModuleValue = ModuleValue::getInstance();
        $this->Payment = Payment::getInstance();
        $this->TemplateSetting = TemplateSetting::getInstance();
        $this->TemplateSettingRemote = new TemplateSetting();
        $this->SuperAdmin = new SuperAdmin();
        $this->ConnectionSwitchFactory = new ConnectionSwitchFactory(true);
        $this->Address = Address::getInstance();
        $this->AddressUser = AddressUser::getInstance();
        $this->UserOption = UserOption::getInstance();
        $this->OldAddress = OldAddress::getInstance();
        $this->Currency = Currency::getInstance();
    }

    public function setDomainID($domainID): void
    {
        parent::setDomainID($domainID);
        $this->Route->setDomainID($domainID);
        $this->Setting->setDomainID(null);
        $this->Currency->setDomainID($domainID);
        $this->RouteLang->setDomainID($domainID);
    }

    public function test(): void
    {
        phpinfo();
        die;
    }

    public function updateUserOption(): array
    {
        $newLang = 'ru';
        $newCurrency = 'RUB';
        $data['response'] = false;

        $saved = 0;
        $edited = 0;

        try {
            $users = $this->User->getAll();
            foreach ($users as $user) {
                $lastID = false;
                $one = $this->UserOption->get('uID', $user['ID']);
                if ($one) {
                    if ($this->UserOption->update($one['ID'], 'lang', $newLang) &&
                        $this->UserOption->update($one['ID'], 'currency', $newCurrency)) {
                        $edited++;
                    }
                } else {
                    $params = [
                        'currency' => $newCurrency,
                        'lang' => $newLang,
                        'uID' => $user['ID'],
                        'userTypeID' => 1
                    ];
                    $lastID = $this->UserOption->create($params);
                    if ($lastID) {
                        $saved++;
                    }
                }
            }

            if ($saved > 0 || $edited > 0) {
                return [
                    'response' => true,
                    'saved' => $saved,
                    'edited' => $edited
                ];
            }
        } catch (Exception $e) {
            $data['response'] = false;
            $data['info'] = $e->getMessage();
        }

        return $data;
    }

    public function post_test(): array
    {
        return [];
    }

    public function patch_createCompany(): array
    {
        $post = $this->Data->getAllPost();
        $settings = $post['settings'];
        $settings['database'] = $settings['name'] = $settings['user'];

        try {
            $this->SuperAdmin->newSuperUser($settings['user'], $settings['dbpass'], 4, $settings['name']);
        } catch (Exception $e) {
            return [
                'info' => $e->getMessage(),
                'response' => false
            ];
        }

        $this->SuperAdmin->newSuperUserSettings($settings['user'], $settings['database']);
        $companyID = $this->SuperAdmin->getUserID($settings['user']);
        $data['response'] = false;

        $tableList = [
            'address',
            'address_users',
            // inne tabelki
        ];

        $copyList = [
            'dp_groups',
            'dp_groupRoles',
            // inne tabelki do skopiowania
        ];

        $patternDatabase = '25piekny_druk';

        $ConnectionUserFactory = ConnectionUserFactory::getInstance();
        $companyDatabase = $ConnectionUserFactory->selectDatabase(false, $companyID);

        try {
            $pdo = new PDO('mysql:host=' . DB_DEVELOPER_HOST, DB_DEVELOPER_USER, DB_DEVELOPER_PASSWORD, [PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"]);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

            $userSettings = $this->SuperAdmin->getSettings($companyID);
            $settings['database'] = $userSettings['database'];
            $settings['dbpass'] = $userSettings['dbpass'];

            $pdo->exec("CREATE DATABASE `" . $settings['database'] . "`");
            $pdo->exec("CREATE USER 'v_" . $settings['user'] . "'@'localhost' IDENTIFIED BY '" . $settings['dbpass'] . "' ");
            $pdo->exec("GRANT SELECT , INSERT , UPDATE , DELETE ON `" . addcslashes($settings['database'], '_%') . "`.* TO 'v_" . $settings['user'] . "'@'localhost' IDENTIFIED BY '" . $settings['dbpass'] . "' ");
            $pdo->exec("FLUSH PRIVILEGES");

            foreach ($tableList as $tl) {
                $pdo->exec(' USE `' . $companyDatabase['dbname'] . '`; ');
                $query = "SHOW TABLES LIKE '$tl' ";

                $exist = $pdo->query($query)->rowCount();
                if ($exist > 0) {
                    continue;
                }

                $pdo->exec(' USE `' . $companyDatabase['dbname'] . '`; ');

                $qCreate = ' CREATE TABLE IF NOT EXISTS `' . $tl . '` LIKE `' . $patternDatabase . '`.`' . $tl . '`; ';
                $pdo->exec($qCreate);
                if (in_array($tl, $copyList)) {
                    $qCopy = ' INSERT `' . $tl . '` SELECT * FROM `' . $patternDatabase . '`.`' . $tl . '`; ';
                    $pdo->exec($qCopy);
                }
                if ($tl == 'dp_domains') {
                    $qInsert = " INSERT INTO `$tl` (
                                `ID`,
                                `name`,
                                `desc`,
                                `host`,
                                `active`
                                )
                                VALUES (
                                NULL , '" . $companyID . "." . ROOT_DOMAIN . "', NULL , '" . $companyID . "." . ROOT_DOMAIN . "', '1'
                                ); ";
                    $pdo->exec($qInsert);
                    $domainID = $pdo->lastInsertId();
                }
                if ($tl == 'dp_langSettings' && $domainID) {
                    $qInsert2 = "INSERT INTO `$tl` (
                                `ID` ,
                                `code`,
                                `domainID`,
                                `active`
                                )
                                VALUES (
                                NULL , 'pl', '" . $domainID . "', '1'
                                );
                                ";
                    $pdo->exec($qInsert2);
                }
                if ($tl == 'dp_settings') {
                    $qInsert3 = "INSERT INTO `dp_settings` (`ID`, `module`, `key`, `value`, `lang`, `domainID`) VALUES
                                (NULL, 'skins', 'bootswatch-cosmo', 'bootswatch-cosmo', NULL, NULL),
                                (NULL, 'skins', 'bootswatch-united', 'bootswatch-united', NULL, NULL),
                                (NULL, 'skins', 'bootswatch-yeti', 'bootswatch-yeti', NULL, NULL),
                                (NULL, 'skins', 'clean', 'clean', NULL, NULL),
                                (NULL, 'skins', 'demo', 'demo', NULL, NULL),
                                (NULL, 'skins', 'sample-first', 'sample-first', NULL, NULL),
                                (NULL, 'skins', 'simple-blue', 'simple-blue', NULL, NULL),
                                (NULL, 'skins', 'simple', 'simple', NULL, NULL);";
                    $pdo->exec($qInsert3);
                }
            }

            $this->createFolders($companyID);
            $this->createRootDomain($pdo, $companyID);
        } catch (Exception $e) {
            $data['error'] = $e->getMessage();
            $data['response'] = false;
        }

        if (!isset($data['error'])) {
            return ['response' => true];
        }
        return $data;
    }

    private function createFolders($companyID): bool
    {
        $rootDir = BASE_DIR . 'data/' . $companyID;
        if (!is_dir($rootDir)) {
            mkdir($rootDir, 0777, true);
            chmod($rootDir, 0774);
        }
        $commonFolders = [
            'images',
            'orderInvoices',
            'productCards',
            // inne foldery
        ];
        foreach ($commonFolders as $folder) {
            $fullPathFolder = $rootDir . '/' . $folder;
            if (!is_dir($fullPathFolder)) {
                mkdir($fullPathFolder, 0777, true);
                chmod($fullPathFolder, 0774);
            }
        }

        $uploadFolder = BASE_DIR . 'data/uploadedFiles/' . $companyID;
        if (!is_dir($uploadFolder)) {
            mkdir($uploadFolder, 0777, true);
            chmod($uploadFolder, 0774);
        }

        return is_dir($rootDir) && is_dir($uploadFolder);
    }

    private function createRootDomain($pdo, $companyID): bool
    {
        $pdo->exec(' USE `dp`; ');

        $query = "INSERT INTO `dp_domains` (
                                `companyID`,
                                `name`,
                                `port`,
                                `active`
                                )
                                VALUES (
                                :companyID,
                                :name,
                                :port,
                                :active
                                );
                                ";
        try {
            $stmt = $pdo->prepare($query);
            $stmt->bindValue('companyID', $companyID, PDO::PARAM_INT);
            $stmt->bindValue('name', $companyID . '.' . ROOT_DOMAIN, PDO::PARAM_STR);
            $stmt->bindValue('port', null, PDO::PARAM_NULL);
            $stmt->bindValue('active', 1, PDO::PARAM_INT);
            $stmt->execute();

            return $pdo->lastInsertId();
        } catch (PDOException $e) {
            $this->debug($e->getMessage());
        }

        return false;
    }

    public function post_createDomain(): array
    {
        $post = $this->Data->getAllPost();
        $domainName = $post['domainName'];

        $this->RouteRemote->setDomainID(SOURCE_DOMAIN_ID);
        $currentDomainName = $this->DomainRoot->get('name', $domainName);

        if ($currentDomainName) {
            return [
                'info' => 'Domena ' . $currentDomainName['name'] . ' już istnieje.',
                'response' => false
            ];
        }

        $currentCompany = $this->DomainRoot->get('companyID', companyID);

        $params = [
            'companyID' => companyID,
            'name' => $domainName,
            'active' => 1
        ];
        $this->DomainRoot->create($params);

        $createParams = [
            'name' => $domainName,
            'host' => $domainName
        ];
        $lastDomainID = $this->Domain->create($createParams);

        $newDomain = $this->Domain->get('ID', $lastDomainID);
        $this->RouteRemote->setRemote(companyID);
        $routes = $this->RouteRemote->getFullTree('main');

        $this->RouteLang->setDomainID($lastDomainID);
        $this->Route->setDomainID($lastDomainID);

        $newViews = [];
        $newLangs = [];
        foreach ($routes as $oneRoute) {
            $this->RouteRemote->setRemote(companyID);
            $parent = $oneRoute['parentID'] > 0 ? $this->RouteRemote->get('ID', $oneRoute['parentID']) : null;

            if ($parent) {
                $lastRouteID = $this->Route->add($oneRoute['state'], $parent['state']);
            } else {
                $lastRouteID = $this->Route->add($oneRoute['state']);
            }

            $this->Route->update($lastRouteID, 'abstract', $oneRoute['abstract']);
            $this->Route->update($lastRouteID, 'name', $oneRoute['name']);
            $this->Route->update($lastRouteID, 'controller', $oneRoute['controller']);

            $this->RouteLangRemote->setRemote(companyID);
            $remoteLangs = $this->RouteLangRemote->get('routeID', $oneRoute['ID'], true);

            if (!empty($remoteLangs)) {
                foreach ($remoteLangs as $rl) {
                    $this->RouteLang->setRemote(companyID);
                    $newLangs[] = $this->RouteLang->set($lastRouteID, $rl['lang'], $rl['url'], $rl['name']);
                }
            }

            $this->ViewRemote->setRemote(companyID);
            $remoteViews = $this->ViewRemote->get('routeID', $oneRoute['ID'], true);

            if (!empty($remoteViews)) {
                foreach ($remoteViews as $rv) {
                    $params = [
                        'name' => $rv['name'],
                        'routeID' => $lastRouteID,
                        'replaceID' => $rv['replaceID'],
                        'templateID' => $rv['templateID'],
                        'isMain' => $rv['isMain'],
                        'controller' => $rv['controller'],
                        'parentViewID' => $rv['parentViewID']
                    ];
                    $newViews[] = $this->View->create($params);
                }
            }

            $this->TemplateSettingRemote->setRemote(companyID);
            $templateSettings = $this->TemplateSettingRemote->getByDomain();

            $newTemplateSettings = [];

            if (!empty($templateSettings)) {
                foreach ($templateSettings as $ts) {
                    $params = [
                        'templateID' => $ts['templateID'],
                        'source' => $ts['source'],
                        'domainID' => $lastDomainID,
                        'root' => $ts['root']
                    ];
                    $newTemplateSettings[] = $this->TemplateSetting->create($params);
                }
            }
        }

        return [
            'response' => true,
            'routes' => $routes,
            'newViews' => $newViews,
            'newLangs' => $newLangs,
            'newDomain' => $newDomain,
            'newTemplateSettings' => $newTemplateSettings
        ];
    }

    private function makeDomain(): array
    {
        $this->RouteRemote->setDomainID(SOURCE_DOMAIN_ID);
        $activeDomainID = $this->getDomainID();
        $activeDomain = $this->Domain->get('ID', $activeDomainID);

        $this->RouteRemote->setRemote(SOURCE_PRINTHOUSE_ID);
        $routes = $this->RouteRemote->getFullTree('main');

        $this->RouteLang->setDomainID($activeDomainID);
        $this->Route->setDomainID($activeDomainID);

        $newViews = [];
        $newLangs = [];
        foreach ($routes as $oneRoute) {
            $this->RouteRemote->setRemote(SOURCE_PRINTHOUSE_ID);
            $parent = $oneRoute['parentID'] > 0 ? $this->RouteRemote->get('ID', $oneRoute['parentID']) : null;

            if ($parent) {
                $lastRouteID = $this->Route->add($oneRoute['state'], $parent['state']);
            } else {
                $lastRouteID = $this->Route->add($oneRoute['state']);
            }

            $this->Route->update($lastRouteID, 'abstract', $oneRoute['abstract']);
            $this->Route->update($lastRouteID, 'name', $oneRoute['name']);
            $this->Route->update($lastRouteID, 'controller', $oneRoute['controller']);

            $this->RouteLangRemote->setRemote(SOURCE_PRINTHOUSE_ID);
            $remoteLangs = $this->RouteLangRemote->get('routeID', $oneRoute['ID'], true);

            if (!empty($remoteLangs)) {
                foreach ($remoteLangs as $rl) {
                    $this->RouteLang->setRemote(companyID);
                    $newLangs[] = $this->RouteLang->set($lastRouteID, $rl['lang'], $rl['url'], $rl['name']);
                }
            }

            $this->ViewRemote->setRemote(SOURCE_PRINTHOUSE_ID);
            $remoteViews = $this->ViewRemote->get('routeID', $oneRoute['ID'], true);

            if (!empty($remoteViews)) {
                foreach ($remoteViews as $rv) {
                    $params = [
                        'name' => $rv['name'],
                        'routeID' => $lastRouteID,
                        'replaceID' => $rv['replaceID'],
                        'templateID' => $rv['templateID'],
                        'isMain' => $rv['isMain'],
                        'controller' => $rv['controller'],
                        'parentViewID' => $rv['parentViewID']
                    ];
                    $newViews[] = $this->View->create($params);
                }
            }

            $this->TemplateSettingRemote->setRemote(SOURCE_PRINTHOUSE_ID);
            $templateSettings = $this->TemplateSettingRemote->getByDomain();

            $newTemplateSettings = [];

            if (!empty($templateSettings)) {
                foreach ($templateSettings as $ts) {
                    $params = [
                        'templateID' => $ts['templateID'],
                        'source' => $ts['source'],
                        'domainID' => $activeDomainID,
                        'root' => $ts['root']
                    ];
                    $newTemplateSettings[] = $this->TemplateSetting->create($params);
                }
            }
        }

        return [
            'response' => true,
            'routes' => $routes,
            'newViews' => $newViews,
            'newLangs' => $newLangs,
            'activeDomain' => $activeDomain,
            'newTemplateSettings' => $newTemplateSettings
        ];
    }

    public function patch_resetDomain(): array
    {
        $domainID = $this->getDomainID();
        $domain = $this->Domain->get('ID', $domainID);

        if ($domain) {
            $this->TemplateSetting->delete('domainID', $domainID);

            $routes = $this->Route->getFullTree('main');
            foreach ($routes as $route) {
                $this->View->delete('routeID', $route['ID']);
                $this->RouteLang->delete('routeID', $route['ID']);
            }

            $this->Route->customDelete('main');
            return $this->makeDomain();
        }

        return ['response' => false];
    }

    public function patch_removeDomain(): array
    {
        $domainID = $this->getDomainID();
        $domain = $this->Domain->get('ID', $domainID);

        if ($domain) {
            $this->TemplateSetting->delete('domainID', $domainID);

            $routes = $this->Route->getFullTree('main');
            foreach ($routes as $route) {
                $this->View->delete('routeID', $route['ID']);
                $this->RouteLang->delete('routeID', $route['ID']);
            }

            $this->Route->customDelete('main');
            return ['response' => true];
        }

        return ['response' => false];
    }

    public function post_executeToAllDb(): array
    {
        $query = $this->Data->getPost('query');

        if (empty($query)) {
            return [
                'info' => 'add a field name query in post',
                'response' => false
            ];
        }

        return $this->ConnectionSwitchFactory->executeForAll($query);
    }

    public function copyUserAddresses(): array
    {
        $this->User->setTableName('users2', false);
        $users = $this->User->getAll();

        $aggregateUsers = [];
        $aggregateInvoices = [];
        foreach ($users as $user) {
            $aggregateUsers[] = $user['ID'];
            if (intval($user['addressID']) > 0) {
                $aggregateInvoices[] = $user['addressID'];
            }
        }

        $defaultAddresses = $this->Address->getDefaultByList($aggregateUsers, 1);
        $defaultInvoiceAddresses = $this->Address->getDefaultByList($aggregateInvoices, 2);

        $createdAddresses = 0;
        $createdInvoiceAddresses = 0;
        $createdAddressJoin = 0;
        $createdInvoiceAddressJoin = 0;

        foreach ($users as $user) {
            if (!isset($defaultAddresses[$user['ID']])) {
                $params = [
                    'name' => $user['name'],
                    'lastname' => $user['lastname'],
                    'street' => $user['street'],
                    'house' => $user['house'],
                    'apartment' => $user['apartment'],
                    'zipcode' => $user['zipcode'],
                    'city' => $user['city'],
                    'areaCode' => $user['areaCode'],
                    'telephone' => $user['telephone'],
                    'companyName' => $user['companyName'],
                    'nip' => $user['nip']
                ];
                $userAddressID = $this->Address->create($params);
                if ($userAddressID > 0) {
                    $createdAddresses++;
                    $params = [
                        'userID' => $user['ID'],
                        'addressID' => $userAddressID,
                        'default' => 1,
                        'type' => 1
                    ];
                    $addressJoinID = $this->AddressUser->create($params);
                    if ($addressJoinID > 0) {
                        $createdAddressJoin++;
                    }
                }
            }

            if (!isset($defaultInvoiceAddresses[$user['ID']]) && $user['addressID'] > 0) {
                $invoiceAddress = $this->Address->get('ID', $user['addressID']);

                if ($invoiceAddress) {
                    $params = [
                        'name' => $invoiceAddress['name'],
                        'lastname' => $invoiceAddress['lastname'],
                        'street' => $invoiceAddress['street'],
                        'house' => $invoiceAddress['house'],
                        'apartment' => $invoiceAddress['apartment'],
                        'zipcode' => $invoiceAddress['zipcode'],
                        'city' => $invoiceAddress['city'],
                        'areaCode' => $invoiceAddress['areaCode'],
                        'telephone' => $invoiceAddress['telephone'],
                        'companyName' => $invoiceAddress['companyName'],
                        'nip' => $invoiceAddress['nip']
                    ];
                    $invoiceAddressID = $this->Address->create($params);
                    if ($invoiceAddressID > 0) {
                        $createdInvoiceAddresses++;
                        $params = [
                            'userID' => $user['ID'],
                            'addressID' => $invoiceAddressID,
                            'default' => 1,
                            'type' => 2
                        ];
                        $invoiceAddressJoinID = $this->AddressUser->create($params);
                        if ($invoiceAddressJoinID > 0) {
                            $createdInvoiceAddressJoin++;
                        }
                    }
                }
            }

            $groupExist = $this->checkUserGroup($user['ID'], 51);

            if (!$groupExist) {
                $this->UserGroup->customCreate(51, $user['ID']);
            }
        }

        return [
            'createdAddresses' => $createdAddresses,
            'createdAddressJoin' => $createdAddressJoin,
            'createdInvoiceAddresses' => $createdInvoiceAddresses,
            'createdInvoiceAddressJoin' => $createdInvoiceAddressJoin,
            'response' => $createdAddresses > 0 || $createdInvoiceAddresses > 0
        ];
    }

    public function post_importUsers(): array
    {
        ini_set('max_execution_time', 720);
        $post = $this->Data->getAllPost();
        $file = $_FILES['file'];
        $dir = STATIC_PATH . companyID . '/export/tmp/';

        if (!is_dir($dir)) {
            mkdir($dir, 0777, true);
        }
        $filename = 'users.xls';
        $path = $dir . $filename;

        if (move_uploaded_file($file['tmp_name'], $path)) {
            if ($post['type'] == 'delivery') {
                $data = $this->importDeliveryAddress($path);
            } elseif ($post['type'] == 'invoice') {
                $data = $this->importInvoiceAddress($path);
            } else {
                $data = $this->import($path);
            }
            $data['response'] = true;
        } else {
            $data['response'] = false;
        }

        return $data;
    }

    private function import($path): array
    {
        $data['response'] = true;

        if (!$this->openFile($path, 0)) {
            $data['response'] = false;
            return $data;
        }
        $sheetArray = $this->sheetToArray();

        $User = new User();
        $User->setDomainID(SOURCE_DOMAIN_ID);
        $UserOption = new UserOption();

        $savedUsers = 0;
        $savedUserOptions = 0;

        foreach ($sheetArray as $key => $row) {
            if ($key == 1) {
                continue;
            }

            if ($row['A'] == null) {
                continue;
            }

            $newUser = [];
            $existUser = $User->getByEmail($row['A']);

            if (!$existUser) {
                $newUser['user'] = $newUser['login'] = $row['A'];
                $newUser['telephone'] = $row['D'];
                $newUser['name'] = strlen($row['B']) == 0 ? '-' : $row['B'];
                $newUser['lastname'] = $row['C'];
                $newUser['domainID'] = SOURCE_DOMAIN_ID;

                $lastID = $User->create($newUser);

                if ($lastID > 0) {
                    $savedUsers++;
                    $userOptionExist = $UserOption->get('uID', $lastID);

                    if (!$userOptionExist) {
                        $newUserOption = [
                            'uID' => $lastID,
                            'userTypeID' => 1
                        ];
                        $lastUserOptionID = $UserOption->create($newUserOption);
                        if ($lastUserOptionID > 0) {
                            $savedUserOptions++;
                        }
                    }
                }
            }
        }

        return compact('savedUsers');
    }

    private function importDeliveryAddress($path): array
    {
        $this->openFile($path, 2);
        $sheetArrayAddresses = $this->sheetToArray();

        $User = new User();
        $User->setDomainID(SOURCE_DOMAIN_ID);
        $Address = new Address();
        $AddressUser = new AddressUser();

        $savedDeliveryJoins = 0;
        $savedDeliveryAddress = 0;

        foreach ($sheetArrayAddresses as $key => $row) {
            if ($key == 1 || $row['A'] == null) {
                continue;
            }

            $existUser = $User->getByEmail($row['A']);
            $newAddress = $this->prepareAddress($row['F']);
            $newAddress['zipcode'] = $row['G'];
            $newAddress['city'] = $row['H'];
            $newAddress['companyName'] = $row['E'];
            $newAddress['name'] = $row['B'];
            $newAddress['lastname'] = $row['C'];
            $newAddress['telephone'] = $row['D'];
            $newAddress['countryCode'] = $this->selectCountryCode($row['I']);
            $newAddress['addressName'] = $newAddress['street'] . ' ' . $newAddress['house'];

            $lastAddressID = $Address->create($newAddress);
            if ($lastAddressID > 0) {
                $savedDeliveryAddress++;
                $newAddressJoin = [
                    'default' => $AddressUser->getOne($existUser['ID'], 1) ? 0 : 1,
                    'userID' => $existUser['ID'],
                    'addressID' => $lastAddressID,
                    'type' => 1
                ];
                $lastAddressUserID = $AddressUser->create($newAddressJoin);
                if ($lastAddressUserID > 0) {
                    $savedDeliveryJoins++;
                }
            }
        }

        return compact('savedDeliveryAddress', 'savedDeliveryJoins');
    }

    private function importInvoiceAddress($path): array
    {
        $this->openFile($path, 1);
        $sheetArrayInvoices = $this->sheetToArray();

        $User = new User();
        $User->setDomainID(SOURCE_DOMAIN_ID);
        $Address = new Address();
        $AddressUser = new AddressUser();

        $savedJoins = 0;
        $savedAddress = 0;

        foreach ($sheetArrayInvoices as $key => $row) {
            if ($key == 1 || $row['A'] == null) {
                continue;
            }

            $existUser = $User->getByEmail($row['A']);
            $newAddress = $this->prepareAddress($row['E']);
            $newAddress['zipcode'] = $row['F'];
            $newAddress['city'] = $row['G'];
            $newAddress['companyName'] = $row['B'];
            $newAddress['countryCode'] = $this->selectCountryCode($row['H']);
            $newAddress['addressName'] = $newAddress['street'] . ' ' . $newAddress['house'];

            $lastAddressID = $Address->create($newAddress);
            if ($lastAddressID > 0) {
                $savedAddress++;
                $newAddressJoin = [
                    'default' => $AddressUser->getOne($existUser['ID'], 2) ? 0 : 1,
                    'userID' => $existUser['ID'],
                    'addressID' => $lastAddressID,
                    'type' => 2
                ];
                $lastAddressUserID = $AddressUser->create($newAddressJoin);
                if ($lastAddressUserID > 0) {
                    $savedJoins++;
                }
            }
        }

        return compact('savedJoins', 'savedAddress');
    }

    private function prepareAddress($rowAddress): array
    {
        $rowAddress = str_replace(',', '', $rowAddress);
        $rowAddress = str_replace([' Lok. ', ' Lok.', '/Lok.'], '/', $rowAddress);

        $newAddress = [];
        if (strstr($rowAddress, ' ')) {
            $expAddress = explode(' ', $rowAddress);
            $addressNumber = end($expAddress);
            if (strstr($addressNumber, '/')) {
                $addressNumberExplode = explode('/', $addressNumber);
                $newAddress['house'] = $addressNumberExplode[0];
                $newAddress['apartment'] = $addressNumberExplode[1];
            } else {
                $newAddress['house'] = $addressNumber;
            }
            array_pop($expAddress);
            $newAddress['street'] = implode(' ', $expAddress);
        } else {
            $newAddress['street'] = $rowAddress;
            $newAddress['house'] = '-';
        }

        return $newAddress;
    }

    private function selectCountryCode($name): string
    {
        return match ($name) {
            'Polska' => 'PL',
            '1Niemcy' => 'DE',
            'Wielka Brytania' => 'GB',
            'Holandia' => 'NL',
            'Austria' => 'AT',
            default => 'PL',
        };
    }

    private function openFile($path, $sheetIndex = 1): bool
    {
        if (!file_exists($path)) {
            return false;
        }
        $inputFileType = PHPExcel_IOFactory::identify($path);
        $ExcelReader = PHPExcel_IOFactory::createReader($inputFileType);
        $this->ExcelFile = $ExcelReader->load($path);
        $this->ExcelFile->setActiveSheetIndex($sheetIndex);
        return true;
    }

    private function sheetToArray(): array
    {
        return $this->ExcelFile->getActiveSheet()->toArray(null, true, true, true);
    }

    private function checkUserGroup($userID, $groupID): bool
    {
        $userGroups = $this->UserGroup->getUserGroups($userID);
        foreach ($userGroups as $userGroup) {
            if ($userGroup['groupID'] == $groupID) {
                return true;
            }
        }
        return false;
    }
}
