angular.module('digitalprint.routes')
    .config(function($stateProvider) {

        var printshop = {};

        printshop.base = {
            parent: 'base',
            name: 'printshop-base',
            url: '/printshop',
            ncyBreadcrumb: {
                label: 'Printshop'
            }
        };

        printshop.index = {
            parent: 'printshop-base',
            name: 'printshop-products',
            url: '/products',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/groups.html',
                    controller: 'printshop.GroupsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "configuration_products" | translate }}'
            }
        };
        printshop.allTypes = {
            parent: 'printshop-products',
            name: 'printshop-group-types',
            url: '/types',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/types.html',
                    controller: 'printshop.TypesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "configuration_types" | translate }}'
            }
        };

        printshop.realizationTimes = {
            parent: 'printshop-base',
            name: 'printshop-realizationTimes',
            url: '/realization-times',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/realization-times.html',
                    controller: 'printshop.RealizationTimesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "realization_times" | translate }}'
            }
        };

        printshop.types = {
            parent: 'printshop-products',
            name: 'printshop-types',
            url: '/group/:groupID',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/types.html',
                    controller: 'printshop.TypesCtrl'
                },
                'realizationTimes@printshop-types': {
                    templateUrl: 'src/printshop/templates/realization-times-details.html',
                    controller: 'printshop.RtGroupCtrl'
                },
                'margins@printshop-types': {
                    templateUrl: 'src/printshop/templates/_margins.html'
                },
                'marginsSelector@printshop-types': {
                    templateUrl: 'src/printshop/templates/margins-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"group" | translate}}: {{currentGroupName}}'
            }
        };

        var typeSettingsResolve = [
            '$q', '$stateParams', 'PsGroupService', 'PsTypeService',
            function($q, $stateParams, PsGroupService, PsTypeService) {
                var currentGroupID = parseInt($stateParams.groupID);
                var currentTypeID = parseInt($stateParams.typeID);
                var def = $q.defer();

                $q.all([
                    PsGroupService.getAll(),
                    PsTypeService.getAll(currentGroupID)
                ]).then(function(data) {
                    var groups = data[0];
                    var types = data[1];
                    var group = _.findWhere(groups, { ID: currentGroupID });
                    var type = _.findWhere(types, { ID: currentTypeID });

                    def.resolve({
                        currentGroupID: currentGroupID,
                        currentTypeID: currentTypeID,
                        group: group,
                        type: type
                    });
                }, function(data) {
                    def.reject(data);
                });

                return def.promise;
            }
        ];


        printshop.typeSettings = {
            parent: 'printshop-types',
            name: 'printshop-type-settings',
            url: '/type/:typeID',
            abstract: true,
            ncyBreadcrumb: {
                label: '{{ "type" | translate }}: {{currentTypeName}}'
            }
        };

        printshop.complexEdit = {
            parent: 'printshop-type-settings',
            name: 'printshop-complex-products',
            url: '/complex-products',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/complex-products.html',
                    controller: 'printshop.ComplexProductsCtrl'
                },
                'productComplexMenu@printshop-complex-products': {
                    templateUrl: 'src/printshop/templates/product-complex-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"products" | translate}}'
            }
        };

        printshop.formats = {
            parent: 'printshop-type-settings',
            name: 'printshop-formats',
            url: '/formats',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/formats.html',
                    controller: 'printshop.FormatsCtrl'
                },
                'productMenu@printshop-formats': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"formats" | translate}}'
            }
        };

        printshop.staticPrices = {
            parent: 'printshop-formats',
            name: 'printshop-format-static-prices',
            url: '/:formatID/static-prices',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/static-prices.html',
                    controller: 'printshop.FormatStaticPricesCtrl'
                },
                'productMenu@printshop-formats': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: 'Stałe ceny'
            }
        };

        printshop.pages = {
            parent: 'printshop-type-settings',
            name: 'printshop-pages',
            url: '/pages',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/pages.html',
                    controller: 'printshop.PagesCtrl'
                },
                'productMenu@printshop-pages': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"pages" | translate}}'
            }
        };

        printshop.volumes = {
            parent: 'printshop-type-settings',
            name: 'printshop-volumes',
            url: '/volumes',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/volumes.html',
                    controller: 'printshop.VolumesCtrl'
                },
                'productMenu@printshop-volumes': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"volumes" | translate}}'
            }
        };

        printshop.complexVolumes = {
            parent: 'printshop-type-settings',
            name: 'printshop-complex-volumes',
            url: '/complex-volumes',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/volumes.html',
                    controller: 'printshop.VolumesCtrl'
                },
                'productMenu@printshop-complex-volumes': {
                    templateUrl: 'src/printshop/templates/product-complex-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"products" | translate}}'
            }
        };

        printshop.attributes = {
            parent: 'printshop-type-settings',
            name: 'printshop-attributes',
            url: '/attributes',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/attributes.html',
                    controller: 'printshop.AttributesCtrl'
                },
                'productMenu@printshop-attributes': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"attributes" | translate}}'
            }
        };

        printshop.increases = {
            parent: 'printshop-type-settings',
            name: 'printshop-increases',
            url: '/increases/:increaseTypeID',
            resolve: {
                getData: typeSettingsResolve,
                increaseTypes: ['$q', '$stateParams', 'PsIncreaseTypeService', function($q, $stateParams, PsIncreaseTypeService) {
                    return PsIncreaseTypeService.getAll().then(function(data) {
                        return data;
                    });
                }]
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/increases.html',
                    controller: 'printshop.IncreasesCtrl'
                },
                'productMenu@printshop-increases': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"increases" | translate}}'
            }
        };

        printshop.typeRealizationTimes = {
            parent: 'printshop-type-settings',
            name: 'printshop-type-realizationTimes',
            url: '/realizationTimes',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/realization-times-details.html',
                    controller: 'printshop.RtTypeCtrl'
                },
                'productMenu@printshop-type-realizationTimes': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"realization_times" | translate}}'
            }
        };

        printshop.typeComplexRealizationTimes = {
            parent: 'printshop-type-settings',
            name: 'printshop-type-complex-realizationTimes',
            url: '/complex-realization-times',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/realization-times-details.html',
                    controller: 'printshop.RtTypeCtrl'
                },
                'productMenu@printshop-type-complex-realizationTimes': {
                    templateUrl: 'src/printshop/templates/product-complex-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"realization_times" | translate}}'
            }
        };

        printshop.typeMargins = {
            parent: 'printshop-type-settings',
            name: 'printshop-type-margins',
            url: '/margins',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/type-margins.html',
                    controller: 'printshop.MarginsTypeCtrl'
                },
                'margins@printshop-type-margins': {
                    templateUrl: 'src/printshop/templates/_margins.html'
                },
                'productMenu@printshop-type-margins': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                },
                'marginsSelector@printshop-type-margins': {
                    templateUrl: 'src/printshop/templates/margins-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"margins" | translate}}'
            }
        };

        printshop.labelImposition = {
            parent: 'printshop-type-settings',
            name: 'printshop-type-labelImposition',
            url: '/labelImposition',
            resolve: {
                getData: typeSettingsResolve
            },
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/labelImposition.html',
                    controller: 'printshop.LabelImpositionCtrl'
                },
                'productMenu@printshop-type-labelImposition': {
                    templateUrl: 'src/printshop/templates/product-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"labelImposition" | translate}}'
            }
        };

        printshop.configAttributes = {
            parent: 'printshop-base',
            name: 'printshop-configAttributes',
            url: '/attributes',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/config-attributes.html',
                    controller: 'printshop.ConfigAttributesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "config_attributes" | translate }}'
            }
        };

        printshop.configAttributesOptions = {
            parent: 'printshop-configAttributes',
            name: 'printshop-attributes-options',
            url: '/options',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/config-options.html',
                    controller: 'printshop.ConfigOptionsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{"attributes_options" | translate}}'
            }
        };

        printshop.configOptions = {
            parent: 'printshop-configAttributes',
            name: 'printshop-configOptions',
            url: '/:attrID/options',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/config-options.html',
                    controller: 'printshop.ConfigOptionsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "attribute" | translate }}: {{currentAttrName}}'
            }
        };

        printshop.configOptionSettings = {
            parent: 'printshop-configOptions',
            name: 'printshop-configOptionSettings',
            url: '/:optID',
            abstract: true,
            ncyBreadcrumb: {
                label: '{{ "option" | translate }}: {{currentOptionName}}'
            }
        };

        var configOptionSettingsResolve = ['$q', '$stateParams', 'PsConfigOptionService', 'PsConfigAttributeService', function($q, $stateParams, PsConfigOptionService, PsConfigAttributeService) {
            var currentAttrID = $stateParams.attrID;
            var currentOptID = $stateParams.optID;
            var def = $q.defer();
            var ConfigOptionService = new PsConfigOptionService(currentAttrID);

            function resolveNeighbors(options, direction) {
                var id;
                options.forEach(function(option, i, all) {
                    if (option.ID == currentOptID) {
                        var index = i + direction;
                        if (index === all.length) {
                            index = 0;
                        }
                        if (index === -1) {
                            index = all.length - 1;
                        }
                        id = all[index].ID;
                    }
                });
                return id;
            }

            $q.all([
                PsConfigAttributeService.getOne(currentAttrID),
                ConfigOptionService.getOne(currentOptID),
                new PsConfigOptionService(currentAttrID).getAll()
            ]).then(function(data) {
                var attribute = data[0];
                var option = data[1];
                def.resolve({
                    currentOptID: currentOptID,
                    currentAttrID: currentAttrID,
                    attribute: attribute,
                    option: option,
                    prevOption: resolveNeighbors(data[2], -1),
                    nextOption: resolveNeighbors(data[2], 1),
                    menu: ['edit', 'descriptions', 'prices', 'increases', 'exclusions', 'operations', 'realizationTimes', 'efficiency', 'altpapers']
                });
            }, function(data) {
                def.reject(data);
            });

            return def.promise;
        }];

        function configOptionSettings(name) {
            var views = {
                'content@base': {
                    templateUrl: 'src/printshop/templates/config-option-' + name.toLowerCase() + '.html',
                    controller: 'printshop.ConfigOption' + _.capitalize(name) + 'Ctrl'
                }
            };
            views['menu@printshop-configOptionSettings-' + name] = { templateUrl: 'src/printshop/templates/config-option-menu.html' };
            return {
                parent: 'printshop-configOptionSettings',
                name: 'printshop-configOptionSettings-' + name,
                url: '/' + name,
                resolve: {
                    getData: configOptionSettingsResolve
                },
                views: views,
                ncyBreadcrumb: {
                    label: '{{' + _.snakeCase(name) + ' | translate}}'
                }
            }
        }

        printshop.configOptionSettingsEdit = configOptionSettings('edit');
        printshop.configOptionSettingsAltpapers = configOptionSettings('altpapers');
        printshop.configOptionSettingsDescriptions = configOptionSettings('descriptions');
        printshop.configOptionSettingsEfficiency = configOptionSettings('efficiency');
        printshop.configOptionSettingsRealizationTimes = configOptionSettings('realizationTimes');
        printshop.configOptionSettingOperations = configOptionSettings('operations');
        printshop.configOptionSettingExclusions = configOptionSettings('exclusions');
        printshop.configOptionSettingPrices = configOptionSettings('prices');
        printshop.configOptionSettingIncreases = configOptionSettings('increases');

        printshop.configTechnologies = {
            parent: 'printshop-base',
            name: 'printshop-configTechnologies',
            url: '/technologies',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/technologies.html'
                },
                'workspaces@printshop-configTechnologies': {
                    templateUrl: 'src/printshop/templates/technologies-workspaces.html',
                    controller: 'printshop.WorkspacesCtrl'
                },
                'pricelists@printshop-configTechnologies': {
                    templateUrl: 'src/printshop/templates/technologies-pricelists.html',
                    controller: 'printshop.PricelistsCtrl'
                },
                'printtypes@printshop-configTechnologies': {
                    templateUrl: 'src/printshop/templates/technologies-printtypes.html',
                    controller: 'printshop.PrinttypesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{"technologies" | translate}}'
            }
        };

        printshop.productionPath = {
            parent: 'printshop-base',
            name: 'printshop-production-path',
            url: '/productionPath',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/production-path.html'
                },
                'departments@printshop-production-path': {
                    templateUrl: 'src/printshop/templates/production-path-departments.html',
                    controller: 'printshop.DepartmentsCtrl'
                },
                'pauses@printshop-production-path': {
                    templateUrl: 'src/printshop/templates/production-path-pauses.html',
                    controller: 'printshop.PausesCtrl'
                },
                'devices@printshop-production-path': {
                    templateUrl: 'src/printshop/templates/production-path-devices.html',
                    controller: 'printshop.DevicesCtrl'
                },
                'skills@printshop-production-path': {
                    templateUrl: 'src/printshop/templates/production-path-skills.html',
                    controller: 'printshop.SkillsCtrl'
                },
                'operators@printshop-production-path': {
                    templateUrl: 'src/printshop/templates/production-path-operators.html',
                    controller: 'printshop.OperatorsCtrl'
                },
                'operations@printshop-production-path': {
                    templateUrl: 'src/printshop/templates/production-path-operations.html',
                    controller: 'printshop.OperationsCtrl'
                },
                'processes@printshop-production-path': {
                    templateUrl: 'src/printshop/templates/production-path-processes.html',
                    controller: 'printshop.ProcessesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "production_path" | translate }}'
            }
        };

        printshop.productionPathDeviceEfficiency = {
            parent: 'printshop-production-path',
            name: 'printshop-production-path-device-efficiency',
            url: '/:deviceID/efficiency',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/production-path-device-efficiency.html',
                    controller: 'printshop.DeviceEfficiencyCtrl'
                },
                'deviceMenu@printshop-production-path-device-efficiency': {
                    templateUrl: 'src/printshop/templates/device-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"device_efficiency" | translate}}'
            }
        };

        printshop.productionPathDeviceSpeed = {
            parent: 'printshop-production-path',
            name: 'printshop-production-path-device-speed',
            url: '/:deviceID/speed',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/production-path-device-speed.html',
                    controller: 'printshop.DeviceSpeedCtrl'
                },
                'deviceMenu@printshop-production-path-device-speed': {
                    templateUrl: 'src/printshop/templates/device-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"speed_change" | translate}}'
            }
        };
        printshop.productionPathDevicePrices = {
            parent: 'printshop-production-path',
            name: 'printshop-production-path-device-prices',
            url: '/:deviceID/prices',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/production-path-device-prices.html',
                    controller: 'printshop.DevicePricesCtrl'
                },
                'deviceMenu@printshop-production-path-device-prices': {
                    templateUrl: 'src/printshop/templates/device-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"prices" | translate}}'
            }
        };

        printshop.productionPathDeviceSettings = {
            parent: 'printshop-production-path',
            name: 'printshop-production-path-device-settings',
            url: '/:deviceID/settings',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/production-path-device-settings.html',
                    controller: 'printshop.DeviceSettingsCtrl'
                },
                'deviceMenu@printshop-production-path-device-settings': {
                    templateUrl: 'src/printshop/templates/device-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"settings" | translate}}'
            }
        };

        printshop.productionPathDeviceServices = {
            parent: 'printshop-production-path',
            name: 'printshop-production-path-device-services',
            url: '/:deviceID/services',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/production-path-device-services.html',
                    controller: 'printshop.DeviceServicesCtrl'
                },
                'deviceMenu@printshop-production-path-device-services': {
                    templateUrl: 'src/printshop/templates/device-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"services_cycle" | translate}}'
            }
        };

        printshop.margins = {
            parent: 'printshop-base',
            name: 'margins',
            url: '/margins',
            views: {
                'content@base': {
                    templateUrl: 'src/printshop/templates/margins.html',
                    controller: 'printshop.MarginsCtrl'
                },
                'marginsMenu@margins': {
                    templateUrl: 'src/printshop/templates/margins-menu.html'
                },
                'marginsEdit@margins': {
                    templateUrl: 'src/printshop/templates/_margins.html'
                },
                'marginsSelector@printshop-types': {
                    templateUrl: 'src/printshop/templates/margins-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"margins" | translate}}'
            }
        };

        _.each(printshop, function(route) {
            $stateProvider.state(route);
        })

    });
