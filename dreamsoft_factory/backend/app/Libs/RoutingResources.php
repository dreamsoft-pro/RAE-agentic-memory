<?php

namespace DreamSoft\Libs;

class RoutingResources
{

    const resources = array(
        'auth' => array('controller' => 'Auth',
            'action' => 'auth',
            'custom' => array('login', 'logout', 'check', 'token', 'resource', 'isAdminEditor')
        ),
        'users' => array(
            'controller' => 'Users',
            'action' => 'index',
            'childs' => array('userRoles', 'userGroups', 'userOptions', 'address'),
            'custom' => array(
                'count',
                'changePass',
                'userRegister',
                'passForget',
                'searchAll',
                'special',
                'getUser',
                'canEditOtherAddress',
                'canRemoveOtherAddress',
                'canAddOtherAddress',
                'getMyAccount',
                'checkOneTimeUser',
                'canEditOtherOptions',
                'getCurrency',
                'userSimpleRegister',
                'getUsersByType',
                'getLoggedUserData',
                'canEditOtherPassword',
                'changePassword',
                'importantData'
            )
        ),
        'address' => array(
            'controller' => 'Users',
            'action' => 'address',
            'custom' => array('addressPublic', 'getUserAddresses', 'setAddressToUser')
        ),
        'userOptions' => array(
            'controller' => 'Users',
            'action' => 'userOptions',
            'custom' => array('userType')
        ),
        'userRoles' => array('controller' => 'Users', 'action' => 'userRoles'),
        'userGroups' => array('controller' => 'Users', 'action' => 'userGroups'),
        'domains' => array('controller' => 'Domains', 'action' => 'index'),
        'settings' => array(
            'package' => 'config',
            'controller' => 'Settings',
            'action' => 'index',
            'module' => true,
            'custom' => array(
                'getSkinName',
                'getPublicSettings',
                'sendMessage',
                'newsletter',
                'confirmNewsletter',
                'getDateByWorkingDays',
                'generateSiteMap'
            )
        ),
        'contents' => array('package' => 'config',
            'controller' => 'Contents',
            'action' => 'index',
            'module' => true),
        'lang' => array('package' => 'lang',
            'controller' => 'Lang',
            'action' => 'index',
            'custom' => array('import', 'export')),
        'langroot' => array('package' => 'lang',
            'controller' => 'LangRoot',
            'action' => 'index',
            'custom' => array('import', 'showEmpty', 'export')),
        'langsettings' => array('package' => 'lang',
            'controller' => 'LangSettings',
            'action' => 'index'),
        'langsettingsroot' => array('package' => 'lang',
            'controller' => 'LangSettingsRoot',
            'action' => 'index'),
        'aclPermissions' => array('controller' => 'Acl', 'action' => 'index'),
        'adminmenu' => array(
            'package' => 'Others',
            'controller' => 'Menu',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'superAdminAcl',
                'superAdminRequestTester',
                'superAdminModules',
                'superAdminHelp',
                'superAdminEmails',
                'superAdminTemplates',
                'shopDomainSettings',
                'shopModules',
                'shopLanguages',
                'shopSpecialUsers',
                'shopUserPermissions',
                'printShopConfigProducts',
                'printShopRealisationTimes',
                'printShopConfigAttributes',
                'printShopWorkspaces',
                'printShopProductionPath',
                'ordersProductionPath',
                'ordersProductionPlanned',
                'ordersProductionPanel',
                'ordersAcceptFiles',
                'ordersOperators',
                'ordersOrders',
                'ordersProducts',
                'ordersStatuses',
                'ordersShipment',
                'ordersReclamationStatuses',
                'ordersCustomProducts',
                'customerServiceRegister',
                'customerServiceUserList',
                'customerServiceOfferList',
                'customerServiceCreateOrder',
                'customerServiceCreateOffer',
                'customerServiceCalculations',
                'customerServiceOrderList',
                'customerServiceDiscounts',
                'customerServicePromotions',
                'customerServiceCoupons',
                'customerServiceReclamations',
                'contentsMails',
                'contentsSeo',
                'contentsCategories',
                'contentsGraphics',
                'contentsViewSettings',
                'contentsTemplates',
                'contentsStaticContents',
                'contentsRoutes'
            )
        ),
        'roles' => array('controller' => 'Acl', 'action' => 'roles', 'childs' => array('rolePerms')),
        'rolePerms' => array('controller' => 'Acl', 'action' => 'rolePerms'),
        'groups' => array('controller' => 'Groups', 'action' => 'index', 'childs' => array('groupRoles')),
        'groupRoles' => array('controller' => 'Groups', 'action' => 'groupRoles'),
        'initPerms' => array('controller' => 'Acl', 'action' => 'initPerms'),
        'currency' => array(
            'controller' => 'Currency',
            'action' => 'index',
            'custom' => array('getDefault')
        ),
        'currencyroot' => array('controller' => 'CurrencyRoot', 'action' => 'index'),
        'tax' => array(
            'controller' => 'Tax',
            'action' => 'index',
            'custom' => array(
                'getBy',
                'taxForProduct'
            )
        ),
        'ps_priceLists' => array(
            'package' => 'printshop_config',
            'controller' => 'PriceLists',
            'action' => 'priceList',
            'custom' => array(
                'uploadIcon'
            ),
            'childs'=>array('ps_priceListDevices')
        ),
        'ps_priceListDevices' => array(
            'package' => 'printshop_config',
            'controller' => 'PriceLists',
            'action' => 'priceListDevices',
        ),
        'ps_workspaces' => array(
            'package' => 'printshop_config',
            'controller' => 'Workspaces',
            'action' => 'workspace',
            'custom' => array(
                'getByPrintType'
            ),
            'childs'=>array('ps_workspaceDevices')
        ),
        'ps_workspaceDevices' => array(
            'package' => 'printshop_config',
            'controller' => 'Workspaces',
            'action' => 'workspaceDevices',
        ),
        'ps_printtypeDevices' => array(
            'package' => 'printshop_config',
            'controller' => 'PrintType',
            'action' => 'printTypeDevices',
        ),
        'ps_attributes' => array(
            'package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'attribute',
            'custom' => array(
                'sortAttr',
                'copy',
                'checkCustomNames',
                'getAttributeSettings',
                'uploadIcon'
            ),
            'childs' => array('ps_options')),
        'ps_printtypes' => array('package' => 'printshop_config',
            'controller' => 'PrintType',
            'action' => 'printType',
            'childs' => array('ps_printtypeDevices')),
        'ps_attributetypes' => array('package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'attributeType'),
        'ps_attributenatures' => array('package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'attributeNature'),
        'attributeFilters' => array('package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'attributeFilters',),
        'getRelativePapers' => array('package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'getRelativePapers',),
        'attributeOptions' => array('package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'attributeOptions'),
        'attributeOption' => array('package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'attributeOption'),
        'attributeOptionPDF' => array('package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'attributeOptionPDF'),
        'productsUsingOptions' => array('package' => 'printshop_config',
            'controller' => 'Attributes',
            'action' => 'productsUsingOptions'),
        'ps_specialprinttypes' => array('package' => 'printshop_config',
            'controller' => 'PrintType',
            'action' => 'printTypeSpecial'),
        'price_exporter' => array('package' => 'printshop_config',
            'controller' => 'Prices',
            'action' => 'price_exporter'),
        'price_importer' => array('package' => 'printshop_config',
            'controller' => 'Prices',
            'action' => 'price_importer'),
        'ps_pricetypes' => array('package' => 'printshop_config',
            'controller' => 'Prices',
            'action' => 'priceTypes'),
        'ps_prices' => array('package' => 'printshop_config',
            'controller' => 'Prices',
            'action' => 'prices',
            'custom' => array('export', 'importPriceList', 'removeAll', 'discountPrices'),
            'childs' => array('ps_prices_remove')
        ),
        'ps_prices_remove' => array(
            'package' => 'printshop_config',
            'controller' => 'Prices',
            'action' => 'allDiscount',
        ),
        'ps_config_increases' => array('package' => 'printshop_config',
            'controller' => 'IncreasesConfig',
            'action' => 'increases'),
        'ps_config_related_increases' => array('package' => 'printshop_config',
            'controller' => 'IncreasesConfig',
            'action' => 'increasesList'),
        'ps_config_related_increases_count' => array('package' => 'printshop_config',
            'controller' => 'IncreasesConfig',
            'action' => 'relatedIncreasesCount'),
        'ps_config_related_increases_list' => array('package' => 'printshop_config',
            'controller' => 'IncreasesConfig',
            'action' => 'relatedIncreasesList'),
        'ps_config_increaseTypes' => array('package' => 'printshop_config',
            'controller' => 'IncreasesConfig',
            'action' => 'increaseTypes'),
        'ps_detailPrices' => array('package' => 'printshop_config',
            'controller' => 'DetailPrices',
            'action' => 'detailPrices'
        ),
        'discounts' => array(
            'package' => 'discounts',
            'controller' => 'Discounts',
            'action' => 'discounts',
            'autoload' => true,
            'custom' => array(
                'discountGroups',
                'selectedDiscountGroup',
                'showProcessDiscounts'
            )
        ),
        'discountLangs' => array(
            'package' => 'discounts',
            'controller' => 'Discounts',
            'action' => 'discountLangs'
        ),
        'promotions' => array(
            'package' => 'promotions',
            'controller' => 'Promotions',
            'action' => 'promotions',
            'custom' => array(
                'count',
                'uploadIcon'
            ),
            'autoload' => true
        ),
        'promotionGroups' => array(
            'package' => 'promotions',
            'controller' => 'Promotions',
            'action' => 'promotionGroups'
        ),
        'promotionLangs' => array(
            'package' => 'promotions',
            'controller' => 'Promotions',
            'action' => 'promotionLangs'
        ),
        'ps_options' => array('package' => 'printshop_config',
            'controller' => 'Options',
            'action' => 'options',
            'custom' => array(
                'sortOptions',
                'copy',
                'uploadIcon'
            ),
            'childs' => array(
                'optionRealizationTimes',
                'optionDescriptions',
                'exclusions',
                'priceControllers',
                'optionOperations',
                'increaseControllers',
                'ps_countPrices',
                'ps_countIncreases',
                'paperPrice',
                'efficiency',
                'relativeOptions'
            ),
        ),
        'efficiency' => array(
            'package' => 'printshop_config',
            'controller' => 'EfficiencyConfig',
            'action' => 'index',
            'childs' => array('speeds', 'speedChanges', 'sideRelations')
        ),
        'relativeOptions' => array(
            'package' => 'printshop_config',
            'controller' => 'RelativeOptions',
            'action' => 'index'
        ),
        'speeds' => array(
            'package' => 'printshop_config',
            'controller' => 'EfficiencyConfig',
            'action' => 'speeds'
        ),
        'speedChanges' => array(
            'package' => 'printshop_config',
            'controller' => 'EfficiencyConfig',
            'action' => 'speedChanges'
        ),
        'sideRelations' => array(
            'package' => 'printshop_config',
            'controller' => 'EfficiencyConfig',
            'action' => 'sideRelations'
        ),
        'paperPrice' => array(
            'package' => 'printshop_config',
            'controller' => 'PaperPrice',
            'action' => 'paperPrice',
        ),
        'ps_countPrices' => array(
            'package' => 'printshop_config',
            'controller' => 'Options',
            'action' => 'countPrices',
        ),
        'ps_countIncreases' => array(
            'package' => 'printshop_config',
            'controller' => 'IncreasesConfig',
            'action' => 'countIncreases',
        ),
        'priceControllers' => array('controller' => 'Printshop', 'action' => 'priceControllers', 'childs' => array('ps_prices', 'ps_detailPrices')),
        'increaseControllers' => array('controller' => 'Printshop', 'action' => 'increaseControllers', 'childs' => array('ps_config_increases', 'ps_config_related_increases', 'ps_config_related_increases_count', 'ps_config_related_increases_list')),
        'optionRealizationTimes' => array('package' => 'printshop_config',
            'controller' => 'OptionRealizationTimes',
            'action' => 'optionRealizationTimes'),
        'optionDescriptions' => array('package' => 'printshop_config',
            'controller' => 'OptionDescriptions',
            'action' => 'optionDescriptions'),
        'exclusions' => array(
            'package' => 'printshop_config',
            'controller' => 'exclusions',
            'action' => 'exclusions'
        ),
        'ps_product_exclusions' => array(
            'package' => 'printshop_config',
            'controller' => 'exclusions',
            'action' => 'productExclusions'
        ),
        'ps_groups' => array(
            'package' => 'printshop',
            'controller' => 'ProductGroups',
            'action' => 'groups',
            'childs' => array(
                'ps_types',
                'ps_rt_details'
            ),
            'custom' => array(
                'offerProducts',
                'getOneForView',
                'uploadIcon',
                'groupsForSelect',
                'getActiveGroups',
                'getActiveGroupsPublic'
            )
        ),
        'ps_types' => array(
            'package' => 'printshop',
            'controller' => 'Types',
            'action' => 'types',
            'childs' => array('ps_volumes',
                'ps_product_options',
                'ps_formats',
                'ps_rt_details',
                'ps_pages',
                'ps_increases',
                'ps_increases_types',
                'ps_tooltips',
                'ps_complex',
                'ps_calculate',
                'ps_product_exclusions',
                'ps_question',
                'ps_use_alternatives'
            ),

            'custom' => array(
                'sort',
                'selectedOptions',
                'forView',
                'selectedOptionsPublic',
                'oneForView',
                'uploadIcon',
                'getTypesData',
                'search',
                'getActiveTypes',
                'copy',
                'searchAll',
                'getActiveTypesPublic'
            )
        ),
        'ps_question'=>array('package' => 'printshop',
            'controller' => 'Types',
            'action' => 'questionOnly'),
        'ps_use_alternatives'=>array('package' => 'printshop',
            'controller' => 'Types',
            'action' => 'useAlternatives'),
        'ps_rt_details' => array(
            'package' => 'printshop',
            'controller' => 'RealizationTime',
            'action' => 'details'
        ),
        'ps_product_options' => array(
            'package' => 'printshop',
            'controller' => 'ProductOptions',
            'action' => 'options',
            'custom' => array('forEditor', 'attrList', 'getAttributeNames')
        ),
        'ps_product_options_count' => array(
            'package' => 'printshop',
            'controller' => 'ProductOptions',
            'action' => 'count'
        ),
        'ps_complex' => array(
            'package' => 'printshop',
            'controller' => 'Complex',
            'action' => 'complex',
            'custom' => array(
                'group',
                'relatedFormat',
                'complexPublic',
                'getByBaseID'
            )
        ),
        'calculations' => array(
            'package' => 'orders',
            'controller' => 'Calculation',
            'action' => 'index',
            'custom' => array('seller', 'history', 'historyMultiOffer', 'deliveriesHistory')
        ),
        'ps_calculate' => array(
            'package' => 'printshop',
            'controller' => 'Calculate',
            'action' => 'calculate',
            'custom' => array(
                'saveCalculation',
                'calculatePublic',
                'saveCalculationPublic',
                'updateName',
                'possibleTechnologies',
                'canChangeAttrPrice',
                'getCurrentMultiOfferVolumes',
                'deleteMultiOffer'
            )
        ),
        'ps_formats' => array('package' => 'printshop',
            'controller' => 'Formats',
            'action' => 'formats',
            'childs' => array('ps_static_prices'),
            'custom' => array('sortFormats', 'formatsPublic', 'customName')),
        'ps_static_prices' => array('package' => 'printshop',
            'controller' => 'StaticPrices',
            'action' => 'staticprices',
            'custom' => array('export', 'import')),

        'ps_volumes' => array('package' => 'printshop',
            'controller' => 'Volumes',
            'action' => 'volumes',
            'childs' => array('ps_rt_details'),
            'custom' => array('customVolume', 'setMaxVolume','setStepVolume')),
        'ps_realizationTimes' => array('package' => 'printshop',
            'controller' => 'RealizationTime',
            'action' => 'index',
            'custom' => array('sort')),
        'ps_pages' => array('package' => 'printshop',
            'controller' => 'Pages',
            'action' => 'pages',
            'custom' => array('pagesPublic', 'customName')
        ),
        'ps_increases' => array('package' => 'printshop',
            'controller' => 'Increases',
            'action' => 'increases'),
        'ps_increase_types' => array('package' => 'printshop',
            'controller' => 'Increases',
            'action' => 'types'),
        'ps_tooltips' => array('package' => 'printshop',
            'controller' => 'Tooltips',
            'action' => 'tooltips'),
        'ps_userData' => array(
            'package' => 'printshop',
            'controller' => 'UserData',
            'action' => 'index'
        ),
        'ps_userFiles' => array(
            'package' => 'printshop',
            'controller' => 'UserFiles',
            'action' => 'index'
        ),
        'statuses' => array('controller' => 'Statuses', 'action' => 'statuses'),

        'dp_statuses' => array('package' => 'orders',
            'controller' => 'OrderStatuses',
            'action' => 'index',
            'autoload' => true,
            'custom' => array('sort', 'forClient')
        ),

        'ssh' => array('package' => 'config',
            'controller' => 'Config',
            'action' => 'ssh'),
        'test' => array(
            'package' => 'config',
            'controller' => 'Config',
            'action' => 'test',
            'custom' => array(
                'importUsers',
                'updateTemplates',
                'updateTemplate',
                'createDomain',
                'setAllUserToGroup',
                'resetDomain',
                'executeToAllDb',
                'copyUserAddresses'
            )
        ),
        'modules' => array('controller' => 'Modules',
            'action' => 'modules',
            'childs' => array('module_keys', 'module_values'),
            'custom' => array('extended')
        ),
        'module_keys' => array('controller' => 'Modules', 'action' => 'keys', 'childs' => array('module_options')),
        'module_options' => array('controller' => 'Modules', 'action' => 'options',),
        'module_values' => array('controller' => 'Modules', 'action' => 'values'),
        'module_types' => array('controller' => 'Modules', 'action' => 'moduleTypes'),
        'deliveries' => array(
            'controller' => 'Deliveries',
            'action' => 'deliveries',
            'custom' => array(
                'deliveriesPublic',
                'findParcelsPublic'
            )
        ),
        'payments' => array(
            'controller' => 'Payments',
            'package' => 'Payments',
            'action' => 'payments',
            'autoload' => true,
            'custom' => array(
                'paymentsPublic',
                'getPaymentTypes',
                'payuVerify',
                'creditLimit'
            )
        ),
        'skills' => array(
            'package' => 'ProductionPath',
            'controller' => 'Skills',
            'action' => 'skills',
            'childs' => array('skillDevices'),
            'autoload' => true
        ),
        'skillDevices' => array(
            'package' => 'ProductionPath',
            'controller' => 'Skills',
            'action' => 'skillDevices',
            'autoload' => true
        ),
        'devices' => array(
            'package' => 'ProductionPath',
            'controller' => 'Devices',
            'action' => 'devices',
            'childs' => array('deviceSkills', 'deviceOngoings', 'deviceSpeeds', 'deviceSpeedChanges', 'deviceSideRelations', 'devicePrices', 'deviceSettings', 'deviceServices'),
            'custom' => array(
                'getWorkUnits',
                'sameDevices',
                'countOngoings',
                'countOngoingsPlanned',
                'countFilteredOngoings',
                'canSeeAllOngoings',
                'sort',
                'deviceEfficiency'
            ),
            'autoload' => true
        ),
        'pauses' => array(
            'package' => 'ProductionPath',
            'controller' => 'Pauses',
            'action' => 'pauses',
            'autoload' => true,
            'custom' => array(
                'sort'
            )
        ),
        'departments' => array(
            'package' => 'ProductionPath',
            'controller' => 'Departments',
            'action' => 'departments',
            'autoload' => true,
            'custom' => array(
                'sort'
            )
        ),
        'shifts' => array(
            'package' => 'ProductionPath',
            'controller' => 'Shifts',
            'action' => 'shifts',
            'autoload' => true,
            'custom' => array(
                'sort'
            )
        ),
        'deviceShift' => array(
            'package' => 'ProductionPath',
            'controller' => 'DeviceShift',
            'action' => 'shifts',
            'autoload' => true,
            'custom' => array(
                'sort',
                'copyFrom'
            )
        ),
        'operations' => array(
            'package' => 'ProductionPath',
            'controller' => 'Operations',
            'action' => 'operations',
            'childs' => array(
                'operationDevices',
                'operationProcesses'
            ),
            'custom' => array('sort'),
            'autoload' => true
        ),
        'operationDevices' => array(
            'package' => 'ProductionPath',
            'controller' => 'Operations',
            'action' => 'operationDevices',
            'autoload' => true
        ),
        'operationProcesses' => array(
            'package' => 'ProductionPath',
            'controller' => 'Operations',
            'action' => 'operationProcesses',
            'autoload' => true
        ),
        'operators' => array(
            'package' => 'ProductionPath',
            'controller' => 'Operators',
            'action' => 'operators',
            'childs' => array('operatorSkills', 'workTimes', 'operatorLogs'),
            'custom' => array(
                'getOperator'
            ),
            'autoload' => true
        ),
        'processes' => array(
            'package' => 'ProductionPath',
            'controller' => 'Processes',
            'action' => 'index',
            'custom' => array(
                'sort'
            ),
            'autoload' => true
        ),
        'workTimes' => array(
            'controller' => 'WorkTimes',
            'action' => 'index',
            'custom' => array('last')
        ),
        'operatorSkills' => array(
            'package' => 'ProductionPath',
            'controller' => 'Operators',
            'action' => 'operatorSkills',
            'autoload' => true
        ),
        'margins' => array(
            'package' => 'PrintShop',
            'controller' => 'Margins',
            'action' => 'index',
            'autoload' => true
        ),
        'margins_supplier' => array(
            'package' => 'PrintShop',
            'controller' => 'MarginsSupplier',
            'action' => 'index',
            'custom' => ['getAllSuppliers'],
            'autoload' => true
        ),
        'labelImposition' => array(
            'package' => 'PrintShop',
            'controller' => 'LabelImposition',
            'action' => 'index',
            'autoload' => true,
            'custom'=>['generate']
        ),
        'ongoings' => array(
            'package' => 'ProductionPath',
            'controller' => 'Ongoings',
            'action' => 'index',
            'custom' => array(
                'path',
                'logs',
                'logsAdditional',
                'operatorLogs',
                'showForItem',
                'progress',
                'sortProd',
                'taskWorkplaces',
                'operator',
                'operatorAdditional',
                'operatorsWithSkills',
                'additionalOperation',
                'alreadyStartedTasks',
                'finishedByOperator',
                'getOperatorLogs',
                'getAllOperatorLogs',
                'getDeviceLogs',
                'getAllDeviceLogs',
                'getOrderLogs',
                'getOperationsLogs',
                'getOperationsLogsCount',
                'ongoingsForCalcProduct',
                'productionSettings',
                'ongoingsOrder'
            ),
            'autoload' => true
        ),
        'sortOngoings' => array(
            'package' => 'ProductionPath',
            'controller' => 'Ongoings',
            'action' => 'sort',
            'autoload' => true
        ),
        'sortbyDevices' => array(
            'package' => 'ProductionPath',
            'controller' => 'Ongoings',
            'action' => 'sortbyDevices',
            'autoload' => true
        ),
        'optionOperations' => array(
            'package' => 'ProductionPath',
            'controller' => 'Operations',
            'action' => 'optionOperations',
            'autoload' => true
        ),
        'deviceSkills' => array(
            'package' => 'ProductionPath',
            'controller' => 'Devices',
            'action' => 'deviceSkills',
            'autoload' => true
        ),
        'deviceOngoingsPlanned' => array(
            'package' => 'ProductionPath',
            'controller' => 'Devices',
            'action' => 'deviceOngoingsPlanned',
            'autoload' => true
        ),
        'deviceOngoings' => array(
            'package' => 'ProductionPath',
            'controller' => 'Devices',
            'action' => 'ongoings',
            'custom' => array('sort'),
            'childs' => array('moveOngoings'),
            'autoload' => true
        ),
        'devicePrices' => array(
            'package' => 'ProductionPath',
            'controller' => 'Prices',
            'action' => 'index',
            'autoload' => true
        ),
        'deviceSettings' => array(
            'package' => 'ProductionPath',
            'controller' => 'DeviceSettings',
            'action' => 'index',
            'autoload' => true
        ),
        'deviceServices' => array(
            'package' => 'ProductionPath',
            'controller' => 'DeviceServices',
            'action' => 'index',
            'autoload' => true
        ),
        'deviceSpeeds' => array(
            'package' => 'ProductionPath',
            'controller' => 'DeviceSpeeds',
            'action' => 'index',
            'autoload' => true
        ),
        'deviceSpeedChanges' => array(
            'package' => 'ProductionPath',
            'controller' => 'DeviceSpeedChanges',
            'action' => 'index',
            'autoload' => true,
            'childs'=>array('efficiencySideRelations')
        ),
        'deviceSideRelations' => array(
            'package' => 'ProductionPath',
            'controller' => 'DeviceSpeedChanges',
            'action' => 'sideRelations',
            'autoload' => true
        ),
        'moveOngoings' => array(
            'package' => 'ProductionPath',
            'controller' => 'Devices',
            'action' => 'move',
            'autoload' => true
        ),
        'deviceOrder' => array(
            'package' => 'ProductionPath',
            'controller' => 'Ongoings',
            'action' => 'deviceOrder',
            'autoload' => true
        ),
        'loadProducts' => array(
            'package' => 'printshop',
            'controller' => 'ProductOptions',
            'action' => 'loadProducts'
        ),
        'adminProjects' => array(
            'package' => 'editor',
            'controller' => 'AdminProjects',
            'action' => 'adminProjects',
            'childs' => array('adminProjectLayers'),
            'custom' => array('extended', 'deleteChilds')
        ),
        'adminProjectLayers' => array(
            'package' => 'editor',
            'controller' => 'AdminProjects',
            'action' => 'layers',
            'childs' => array('adminProjectObjects', 'adminProjectLayerAttributes'),
            'custom' => array('extendedLayer')
        ),
        'adminProjectSortLayer' => array('package' => 'editor',
            'controller' => 'AdminProjects',
            'action' => 'sortLayer'),
        'adminProjectLayerAttributes' => array(
            'package' => 'editor',
            'controller' => 'AdminProjects',
            'action' => 'attributes'),
        'adminProjectObjects' => array('package' => 'editor',
            'controller' => 'AdminProjects',
            'action' => 'objects'),
        'adminProjectOnlyObjects' => array('package' => 'editor',
            'controller' => 'AdminProjects',
            'action' => 'onlyObjects'),
        'adminProjectOnlyLayers' => array('package' => 'editor',
            'controller' => 'AdminProjects',
            'action' => 'onlyLayers'),
        'upload' => array('package' => 'editor',
            'controller' => 'Upload',
            'action' => 'upload',
            'custom' => array('compress', 'theme'),
        ),
        'upload_url' => array('package' => 'editor',
            'controller' => 'Upload',
            'action' => 'url'
        ),
        'fotobudka' => array(
            'package' => 'editor',
            'controller' => 'Upload',
            'action' => 'fotobox'
        ),
        'adminFonts' => array(
            'package' => 'editor',
            'controller' => 'Fonts',
            'action' => 'fonts',
            'custom' => array('checkFont'),
        ),
        'createCompany' => array(
            'package' => 'config',
            'controller' => 'Config',
            'action' => 'createCompany'
        ),
        'copyPerms' => array(
            'package' => 'config',
            'controller' => 'Config',
            'action' => 'copyPerms'
        ),
        'resetDomain' => array(
            'package' => 'config',
            'controller' => 'Config',
            'action' => 'resetDomain'
        ),
        'removeDomain' => array(
            'package' => 'config',
            'controller' => 'Config',
            'action' => 'removeDomain'
        ),
        'routes' => array(
            'package' => 'Route',
            'controller' => 'Routes',
            'action' => 'index',
            'custom' => array(
                'moveUp',
                'moveDown',
                'breadcrumbs',
                'level',
                'productToRoute',
                'show',
                'buildRouting',
                'one',
                'getRouteByUrl',
                'generateRoutesFile',
                'translateState'
            ),
            'childs' => array('mainContents'),
            'autoload' => true
        ),
        'mainContents' => array(
            'controller' => 'MainContents',
            'action' => 'index',
            'custom' => array('sort'),
        ),
        'adminHelps' => array(
            'package' => 'AdminHelp',
            'controller' => 'Help',
            'action' => 'helps',
            'childs' => array('helpKeys'),
            'autoload' => true
        ),
        'helpKeys' => array(
            'package' => 'AdminHelp',
            'controller' => 'Help',
            'action' => 'keys',
            'childs' => array('helpLangs'),
            'autoload' => true
        ),
        'helpLangs' => array(
            'package' => 'AdminHelp',
            'controller' => 'Help',
            'action' => 'langs',
            'autoload' => true
        ),
        'ps_preflightFolder' => array(
            'package' => 'printshop',
            'controller' => 'PreFlight',
            'action' => 'index',
        ),
        'activeModules' => array(
            'controller' => 'Modules',
            'action' => 'activeModules'
        ),
        'operatorLogs' => array(
            'package' => 'ProductionPath',
            'controller' => 'Operators',
            'action' => 'operatorLogs',
            'custom' => array('count'),
            'autoload' => true
        ),
        'mailTypes' => array('controller' => 'mail',
            'action' => 'types',
            'childs' => array('mailContents', 'mailVariables')),
        'mailContents' => array('controller' => 'mail',
            'action' => 'contents'),
        'mailVariables' => array(
            'controller' => 'mail',
            'action' => 'variables'
        ),
        'offers' => array('controller' => 'Offers',
            'action' => 'offers',
            'custom' => array('getCurrent')
        ),
        'offerItems' => array('controller' => 'Offers',
            'action' => 'items',
            'custom' => array('files', 'getFile', 'userCanAddFile')),
        'ountOffers' => array('controller' => 'Offers',
            'action' => 'count'),
        'offerCompanies' => array('controller' => 'Offers',
            'action' => 'companies'),
        'auctions' => array('controller' => 'Auctions',
            'action' => 'index',
            'custom' => array('forCompany', 'getAuctions', 'finishAuction', 'responseWinner', 'order', 'isAuctionUser', 'export'),
            'childs' => array('auctionResponses', 'auctionAllResponses', 'auctionSelectWinner', 'auctionFiles')),
        'auctionFiles' => array('controller' => 'Auctions',
            'action' => 'files',
            'custom' => array('getFile'),
        ),
        'auctionResponses' => array(
            'controller' => 'Auctions',
            'action' => 'response',
        ),
        'auctionAllResponses' => array(
            'controller' => 'Auctions',
            'action' => 'allresponses'),

        'auctionSelectWinner' => array(
            'controller' => 'Auctions',
            'action' => 'selectWinner'),
        'prices' => array(
            'controller' => 'BasePrices',
            'action' => 'index'
        ),
        'userTypes' => array(
            'controller' => 'UserTypes',
            'action' => 'types',
            'custom' => array('userTypeGroups', 'userTypeRoles')
        ),
        'templates' => array(
            'package' => 'templates',
            'controller' => 'TemplateRoot',
            'action' => 'templates',
            'custom' => array('show', 'upload', 'getFile', 'getCss', 'setSource', 'getUrl', 'removeFile')
        ),
        'local_templates' => array(
            'package' => 'templates',
            'controller' => 'Templates',
            'action' => 'templates',
            'custom' => array('upload', 'setSource', 'getFile', 'removeFile')
        ),
        'dp_carts_data' => array(
            'package' => 'orders',
            'controller' => 'DpCartsData',
            'action' => 'index',
            'custom' => array(
                'updateAddresses',  'getUserCart'
            )
        ),
        'dp_orders' => array(
            'package' => 'orders',
            'controller' => 'DpOrders',
            'action' => 'index',
            'custom' => array(
                'sellerNotReady',
                'saveOffer',
                'offerList',
                'orderList',
                'offerListCount',
                'orderListCount',
                'isAdmin',
                'isSeller',
                'isBok',
                'order',
                'count',
                'placeOrder',
                'updateAddress',
                'updateVatAddress',
                'getCart',
                'setUser',
                'saveCart',
                'getAddresses',
                'myZone',
                'myZoneOffers',
                'paymentSuccess',
                'paymentStatus',
                'myZoneCount',
                'payment',
                'updatePrice',
                'recalculateDelivery',
                'addToJoinedDelivery',
                'paymentRemind',
                'getOrderInvoiceAddress',
                'changeOrderPrice',
                'restoreOrderPrice',
                'changeAddresses',
                'fileReminder',
                'canEditPrice',
                'acceptOffer',
                'rejectOffer',
                'changeMultiOffer'
            )
        ),
        'dp_products' => array(
            'package' => 'Orders',
            'controller' => 'DpProducts',
            'action' => 'index',
            'custom' => array(
                'baseCalcInfo',
                'baseInfo',
                'count',
                'deletePublic',
                'myZone',
                'getByOrder',
                'restoreAccept',
                'copy',
                'exportOrders'
            ),
            'childs' => array('calcFilesUploaderGuestSet','calcFilesUploaderSet','calcFilesUploader', 'productFiles', 'reportFiles'),
            'autoload' => true
        ),
        'schedule' => array(
            'package' => 'ProductionPath',
            'controller' => 'Schedule',
            'action' => 'index',
            'custom' => array(
                'count',
                'sort',
                'updateOngoings'
            ),
            'autoload' => true
        ),
        'planning' => array(
            'package' => 'ProductionPath',
            'controller' => 'Planning',
            'action' => 'index',
            'custom' => array(
                'count'
            ),
            'autoload' => true
        ),
        'calcFilesUploaderGuestSet' => array(
            'package' => 'orders',
            'controller' => 'calcFilesUploader',
            'action' => 'createGuestSet'
        ),
        'calcFilesUploaderSet' => array(
            'package' => 'orders',
            'controller' => 'calcFilesUploader',
            'action' => 'filesSet'
        ),
        'calcFilesUploader' => array(
            'package' => 'orders',
            'controller' => 'calcFilesUploader',
            'action' => 'files',
            'custom' => array(
                'setImageBW', 'setImageSepia', 'setCollectionToBW', 'setCollectionToSepia', 'removeCollectionFilters', 'cropImage', 'restoreImage', 'copyImage', 'changeQty', 'editImage'
            )
        ),
        'productFiles' => array(
            'package' => 'orders',
            'controller' => 'DpProductFiles',
            'action' => 'files',
            'custom' => array(
                'productListFiles',
                'canSeeUserFiles',
                'makeMiniature',
                'saveFileProps',
                'saveProductProps'
            ),
            'childs'=>array('productReportFiles')
        ),
        'reportFiles' => array(
            'package' => 'orders',
            'controller' => 'DpProducts',
            'action' => 'reportFiles',
            'autoload' => true
        ),
        'productReportFiles' => array(
            'package' => 'orders',
            'controller' => 'DpProductFiles',
            'action' => 'reportFiles'
        ),
        'dp_views' => array(
            'package' => 'templates',
            'controller' => 'Views',
            'action' => 'index',
            'custom' => array('variables', 'mainVariables', 'sort', 'masks', 'createMask')
        ),
        'dp_categories' => array(
            'controller' => 'Categories',
            'action' => 'index',
            'custom' => array(
                'selectedToGroup',
                'setSelectedToGroup',
                'selectedToType',
                'setSelectedToType',
                'getContains',
                'getContainsAdmin',
                'getParents',
                'forView',
                'oneForView',
                'sort',
                'sortItems',
                'manyForView',
                'categoryContains',
                'getCategoryTree',
                'getChilds',
                'uploadIcon',
                'forViewPublic',
                'getGroups',
                'getFirstByType'
            )
        ),
        'pdfGenerating' => array(
            'controller' => 'PdfGenerate',
            'action' => 'generatePdf'
        ),
        'jpgPreview' => array(
            'controller' => 'PdfGenerate',
            'action' => 'jpgPreview'
        ),
        'authors' => array(
            'controller' => 'Authors',
            'action' => 'index'
        ),
        'ps_typeDescriptions' => array(
            'package' => 'printshop',
            'controller' => 'TypeDescriptions',
            'action' => 'typeDescriptions',
            'custom' => array('typeDescriptionsPublic', 'files', 'descFiles'),
        ),
        'ps_typeDescriptionsFormats' => array(
            'package' => 'printshop',
            'controller' => 'TypeDescriptionsFormats',
            'action' => 'typeDescriptionsFormats'
        ),
        'ps_groupDescriptions' => array(
            'package' => 'printshop',
            'controller' => 'GroupDescriptions',
            'action' => 'groupDescriptions',
            'custom' => array('groupDescriptionsPublic', 'files', 'descFiles'),
        ),
        'categoriesDescriptions' => array(
            'controller' => 'CategoriesDescriptions',
            'action' => 'categoriesDescriptions',
            'custom' => array('categoriesDescriptionsPublic', 'files', 'descFiles'),
        ),
        'subcategoriesDescriptions' => array(
            'controller' => 'SubcategoriesDescriptions',
            'action' => 'subcategoriesDescriptions',
            'custom' => array('subcategoriesDescriptionsPublic', 'files', 'descFiles'),
        ),
        'ps_connectOptions' => array(
            'package' => 'printshop_config',
            'controller' => 'ConnectOptions',
            'action' => 'index',
            'custom' => array('addToGroup', 'price')
        ),
        'taUploadIcons' => array(
            'controller' => 'TextAngularUpload',
            'action' => 'textAngularIcons'
        ),
        'graphicsUpload' => array(
            'controller' => 'Graphics',
            'action' => 'uploadElement',
            'custom' => array(
                'modelIcon',
                'favicon'
            )
        ),
        'dp_ModelIconsExtensions' => array(
            'controller' => 'ModelIconExtensions',
            'action' => 'modelIconExtensions'
        ),
        'homePageBanner' => array(
            'controller' => 'HomePageBanner',
            'action' => 'homePageBanner',
            'custom' => array('homePageBannerPublic')
        ),
        'ps_patterns' => array(
            'package' => 'printshop',
            'controller' => 'TypeDescriptionPatterns',
            'action' => 'patterns',
            'custom' => array('patternsPublic')
        ),
        'ps_realizationTimeWorkingHours' => array(
            'package' => 'PrintShop',
            'controller' => 'RealizationTimeWorkingHours',
            'action' => 'index',
            'autoload' => true
        ),
        'dp_addresses' => array(
            'package' => 'Addresses',
            'controller' => 'Addresses',
            'action' => 'address',
            'custom' => array(
                'getAddress',
                'updateAddress',
                'getAddresses',
                'addAddress',
                'emptyAddress',
            ),
            'autoload' => true
        ),
        'dp_countries' => array(
            'package' => 'config',
            'controller' => 'Countries',
            'action' => 'index',
            'custom' => array('getAll')
        ),
        'productCard' => array(
            'controller' => 'ProductCard',
            'action' => 'generateCard',
            'custom' => array('generateXML')
        ),
        'dp_static_contents' => array(
            'package' => 'contents',
            'controller' => 'StaticContents',
            'action' => 'index',
            'autoload' => true,
            'custom' => array('getContent')
        ),
        'dp_coupons' => array(
            'package' => 'coupons',
            'controller' => 'Coupons',
            'action' => 'index',
            'autoload' => true,
            'custom' => array('products', 'count', 'check')
        ),
        'dp_newsletter' => array(
            'package' => 'newsletter',
            'controller' => 'Newsletter',
            'action' => 'index',
            'autoload' => true,
            'custom' => array('export')
        ),
        'dp_invoices' => array(
            'package' => 'orders',
            'controller' => 'Invoices',
            'action' => 'generate',
            'custom' => array('changeInvoiceType', 'getForUser')
        ),
        'dp_shipment' => array(
            'package' => 'orders',
            'controller' => 'Shipment',
            'action' => 'index',
            'custom' => array('printLabel', 'generateLabels', 'labels')
        ),
        'dp_reclamation_faults' => array(
            'package' => 'Reclamations',
            'controller' => 'ReclamationFaults',
            'action' => 'faults',
            'autoload' => true,
        ),
        'dp_reclamations' => array(
            'package' => 'Reclamations',
            'controller' => 'Reclamations',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'files',
                'findByOrder',
                'myZone',
                'myZoneCount',
                'count',
                'getFiles',
                'canUploadReclamationFiles',
                'canCreateReclamation',
                'createReclamation'
            )
        ),
        'dp_reclamations_statuses' => array(
            'package' => 'Reclamations',
            'controller' => 'ReclamationsStatuses',
            'action' => 'index',
            'autoload' => true,
            'custom' => array('sort', 'forClient')
        ),
        'dp_reclamations_messages' => array(
            'package' => 'Reclamations',
            'controller' => 'ReclamationsMessages',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'myZone',
                'count',
                'countAll',
                'canReadWriteMessages',
                'sendEmail'
            )
        ),
        'dp_news' => array(
            'package' => 'Others',
            'controller' => 'News',
            'action' => 'index',
            'autoload' => true,
            'custom' => array('rss')
        ),
        'dp_orders_messages' => array(
            'package' => 'orders',
            'controller' => 'OrdersMessages',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'myZone',
                'count',
                'countAll',
                'canReadWriteOrderMessages',
                'sendEmail'
            )
        ),
        'dp_mainMetaTags' => array(
            'package' => 'MetaTags',
            'controller' => 'MainMetaTags',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'uploadImage'
            )
        ),
        'dp_metaTags' => array(
            'package' => 'MetaTags',
            'controller' => 'MetaTags',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'uploadImage'
            )
        ),
        'dp_authorizationLogs' => array(
            'package' => 'Authorization',
            'controller' => 'AuthorizationLogs',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'count',
                'deleteByUser'
            )
        ),
        'dp_customProducts' => array(
            'package' => 'CustomProducts',
            'controller' => 'CustomProducts',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'files',
                'canUploadCustomProductFiles',
                'count',
                'getOne',
                'getPublic',
                'publicCount'
            )
        ),
        'dp_calculate' => array(
            'package' => 'PrintShop',
            'controller' => 'Count',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'cartReCalculate',
                'cartRestorePrices'
            )
        ),
        'ps_printTypeWorkspaces' => array(
            'package' => 'PrintShop',
            'controller' => 'PrintShopPrintTypeWorkspaces',
            'action' => 'index',
            'autoload' => true
        ),
        'calculate' => array(
            'package' => 'Calculate',
            'controller' => 'Calculate',
            'action' => 'index',
            'autoload' => true,
            'custom' => array(
                'printOffer'
            )
        ),
        'mainCssFile' => array(
            'package' => 'Contents',
            'controller' => 'Styles',
            'action' => 'mainFile',
            'autoload' => true
        ),
        'templateVariables' => array(
            'package' => 'Contents',
            'controller' => 'TemplateVariables',
            'action' => 'index',
            'autoload' => true,
            'custom' => array('getTemplates', 'getSelectors', 'getForRange', 'getGlobal', 'assoc', 'getVariables')
        )
    );


    /**
     * @return array
     */
    public static function getResources()
    {
        return RoutingResources::resources;
    }


}
