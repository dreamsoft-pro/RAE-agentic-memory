angular.module('digitalprint.app')
    .controller('printshop.AttributesCtrl', function ($scope, $stateParams, $modal, $filter, $q, Notification,
                                                      PsAttributeService, PsConfigAttributeService,
                                                      PsConfigOptionService, PsFormatService, PsTooltipService,
                                                      PsPageService, DeliveryService, PsTypeService) {

        $scope._ = _;

        var currentGroupID = $scope.currentGroupID = $stateParams.groupID;
        var currentTypeID = $scope.currentTypeID = $stateParams.typeID;

        $scope.formatCustomNames = {};
        $scope.pageCustomNames = {};
        $scope.attributeSettings = {};

        $scope.specialAttributes = [{name: 'Formaty', ID: -1}, {name: 'Strony', ID: -2}];

        var AttributeService = new PsAttributeService(currentGroupID, currentTypeID);
        var ConfigOptionService = new PsConfigOptionService(0);
        $q.all([PsConfigAttributeService.getAll(true),
            AttributeService.getAll(true),
            ConfigOptionService.getAll(),
            PsTypeService.getExclusions(currentGroupID,currentTypeID)]).then(function(data){
            $scope.attributes = data[0];
            var selectedOptions = data[1];
            $scope.selectedOptions = {};

            _.each(selectedOptions, function (value, key) {
                if ($scope.selectedOptions[value.attrID] === undefined) {
                    $scope.selectedOptions[value.attrID] = {};
                }
                if ($scope.selectedOptions[value.attrID][value.optID] === undefined) {
                    $scope.selectedOptions[value.attrID][value.optID] = {};
                }

                $scope.selectedOptions[value.attrID][value.optID] = {formats: value.formats};
                $scope.selectedOptions[value.attrID][value.optID].invisible = value.invisible;
                $scope.selectedOptions[value.attrID][value.optID].default = value.default;
                $scope.selectedOptions[value.attrID][value.optID].excludedDeliveries = value.excludedDeliveries;

            });
            $scope.allOptions = _.groupBy(data[2], 'attrID');
            $scope.exclusions = _.isArray(data[3]) && data[1].length==0 ? {}:data[3];
            updateCountedExclusions();
        });

        PsConfigAttributeService.getCustomNames(currentTypeID).then(function (data) {
            $scope.countCustomNames = data;
        });

        PsConfigAttributeService.getAttributeSettings(currentTypeID).then(function (data) {
            $scope.attributeSettings = data;
        });

        var FormatService = new PsFormatService(currentGroupID, currentTypeID);
        FormatService.getAll().then(function (data) {
            $scope.formats = data;
        });

        FormatService.getCustomNames().then(function (data) {
            if (data.length === 0) {
                $scope.formatCustomNames = {};
            } else {
                $scope.formatCustomNames = data;
            }
        });

        function refreshCustomFormatName() {
            FormatService.getCustomNames().then(function (data) {
                if (data.length === 0) {
                    $scope.formatCustomNames = {};
                } else {
                    $scope.formatCustomNames = data;
                }
            });
        }

        var PageService = new PsPageService(currentGroupID, currentTypeID);

        PageService.getCustomNames().then(function (data) {
            if (data.length === 0) {
                $scope.pageCustomNames = {};
            } else {
                $scope.pageCustomNames = data;
            }
        });

        function refreshCustomPageName() {
            PageService.getCustomNames().then(function (data) {
                if (data.length === 0) {
                    $scope.pageCustomNames = {};
                } else {
                    $scope.pageCustomNames = data;
                }
            });
        }

        var TooltipService = new PsTooltipService(currentGroupID, currentTypeID);
        TooltipService.getAll().then(function (data) {
            $scope.tooltips = data;
        });

        $scope.setOption = function (attrID, optID) {
            if ($scope.selectedOptions[attrID] === undefined) {
                $scope.selectedOptions[attrID] = {};
            }

            if ($scope.selectedOptions[attrID][optID] === undefined) {
                $scope.selectedOptions[attrID][optID] = {};
            }

            if (!_.keys($scope.selectedOptions[attrID][optID]).length) {
                $scope.selectedOptions[attrID][optID] = {formats: null};
            } else {
                $scope.selectedOptions[attrID] = _.omit($scope.selectedOptions[attrID], optID.toString());

            }

            $scope.optionSave(attrID, optID, $scope.selectedOptions[attrID][optID]);
            if (!_.keys($scope.selectedOptions[attrID]).length) {
                delete $scope.selectedOptions[attrID];
            }
            updateCountedExclusions();
        };

        $scope.selectAllImpl = function (attrID,allSelectionState) {
            $scope.allOptions[attrID].forEach(function(options){
                if(allSelectionState && (!$scope.selectedOptions[attrID] || !$scope.selectedOptions[attrID][options.ID])){
                    $scope.setOption(attrID, options.ID);
                }else if(!allSelectionState && $scope.selectedOptions[attrID]  && $scope.selectedOptions[attrID][options.ID]){
                    $scope.setOption(attrID, options.ID);
                }
            });
        };

        $scope.optionSave = function (attrID, optID, item) {
            var action;
            if (item === undefined) {
                action = 'remove';
            } else {
                action = 'add';
            }

            AttributeService.saveOption({attrID: attrID, optID: optID, action: action}).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.setInvisible = function (attr) {
            var optID = _.first(_.keys($scope.selectedOptions[attr.ID]));
            var currentValue = $scope.selectedOptions[attr.ID][optID].invisible;

            if( typeof currentValue === 'number') {
                currentValue = currentValue ? 0 : 1;
            } else if (typeof currentValue === 'boolean') {
                currentValue = currentValue === true ? 0 : 1;
            }

            AttributeService.setInvisible(attr.ID, optID, currentValue).then(function (data) {
                $scope.selectedOptions[attr.ID][optID].invisible = currentValue;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.attrFormats = function (attrID, optID) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/attribute-formats.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.optionFormats = $scope.selectedOptions[attrID][optID].formats;
                    console.log($scope.allOptions);

                    _.each($scope.formats, function (item) {
                        if (_.indexOf($scope.optionFormats, item.ID) > -1) {
                            item.selected = 1;
                        } else {
                            item.selected = 0;
                        }
                    });

                    $scope.save = function () {
                        $scope.optionFormats = [];

                        _.each($scope.formats, function (item) {
                            if (item.selected) {
                                $scope.optionFormats.push(item.ID);
                            }
                        });

                        AttributeService.setFormats(attrID, optID, $scope.optionFormats).then(function (data) {
                            $scope.selectedOptions[attrID][optID].formats = angular.copy($scope.optionFormats);
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })
        };

        $scope.tooltip = function (attr) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/attribute-tooltips.html',
                scope: $scope,
                resolve:{
                    languages: function(LangSettingsService) {
                        return LangSettingsService.getAll().then( function(data) {
                            return data;
                        })
                    }
                },
                backdrop: 'static',
                controller: function ($scope, $modalInstance, $rootScope) {
                    $scope.languages = $rootScope.languages;

                    $scope.selectedLang = $rootScope.currentLang.code;

                    $scope.editItem = attr;
                    $scope.editTooltip = $scope.tooltips[attr.ID] ? $scope.tooltips[attr.ID].tooltip : {};

                    $scope.save = function () {
                        TooltipService.save(attr.ID, $scope.editTooltip).then(function (data) {
                            if ($scope.tooltips[attr.ID] === undefined) {
                                $scope.tooltips[attr.ID] = {};
                            }
                            $scope.tooltips[attr.ID].tooltip = angular.copy($scope.editTooltip);
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })

        };

        $scope.setDefaultOption = function (selectedOptions, attribute, option) {

            selectedOptions[attribute.ID][option.ID].default = selectedOptions[attribute.ID][option.ID].default ? 0 : 1;

            AttributeService.setDefault(
                attribute.ID,
                option.ID,
                selectedOptions[attribute.ID][option.ID].default
            ).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                    _.each(selectedOptions[attribute.ID], function (oneOption, optID) {
                        if (parseInt(optID) !== data.optionID) {
                            oneOption.default = 0;
                        }
                    });
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.customAttributeNames = function (attribute) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-attribute-names.html',
                scope: $scope,
                resolve: {
                    names: function () {
                        return AttributeService.getCustomNames(attribute.ID).then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, names) {

                    $scope.form = {};
                    if (names.length === 0) {
                        names = {};
                    }
                    $scope.form.names = names;

                    $scope.save = function () {

                        var countCustomNames = 0;
                        _.each(this.form.names, function (name) {
                            if (name.length > 0) {
                                countCustomNames++;
                            }
                        });

                        $scope.countCustomNames[attribute.ID] = countCustomNames;

                        AttributeService.setCustomNames(attribute.ID, this.form.names).then(function (data) {
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })

        };

        $scope.setCustomFormatNames = function () {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-attribute-names.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {

                    $scope.form = {};
                    var names = $scope.formatCustomNames;
                    if (_.isEmpty($scope.formatCustomNames)) {
                        names = {};
                    }

                    $scope.form.names = names;

                    $scope.save = function () {

                        FormatService.setCustomNames(this.form.names).then(function (data) {
                            Notification.success($filter('translate')('success'));
                            refreshCustomFormatName();
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })

        };

        $scope.setCustomPageNames = function () {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-attribute-names.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {

                    $scope.form = {};
                    var names = $scope.pageCustomNames;
                    if (_.isEmpty($scope.pageCustomNames)) {
                        names = {};
                    }

                    $scope.form.names = names;

                    $scope.save = function () {

                        PageService.setCustomNames(this.form.names).then(function (data) {
                            Notification.success($filter('translate')('success'));
                            refreshCustomPageName();
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })

        };

        $scope.setSelectByPicture = function (attrID, attributeSetting) {

            if (attributeSetting === undefined) {
                attributeSetting = {};
                attributeSetting.attrID = attrID;
                attributeSetting.selectByPicture = 0;
            }

            $scope.attributeSettings[attrID] = attributeSetting;

            var selectByPicture = attributeSetting.selectByPicture ? 0 : 1;

            AttributeService.setSelectByPicture(attributeSetting.attrID, selectByPicture).then(function (saved) {
                if (saved.response === true) {
                    attributeSetting.selectByPicture = selectByPicture;
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function () {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.setAuthCalculation = function (option) {
            option.authorizedOnlyCalculation = option.authorizedOnlyCalculation ? 0 : 1;
            ConfigOptionService.edit(option).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.setDeliveryExclusions = function (option) {

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/option-deliveries.html',
                scope: $scope,
                resolve: {
                    deliveries: function () {
                        return DeliveryService.getAll(false, '?active=1').then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, deliveries) {

                    $scope.deliveries = deliveries;

                    _.each($scope.deliveries, function (item) {

                        var deliveryIndex = _.indexOf(
                            $scope.selectedOptions[option.attrID][option.ID].excludedDeliveries,
                            item.ID
                        );

                        if (deliveryIndex > -1) {
                            item.selected = true;
                        } else {
                            item.selected = false;
                        }
                    });

                    $scope.save = function () {

                        var optionDeliveries = [];

                        _.each($scope.deliveries, function (item) {
                            if (item.selected) {
                                optionDeliveries.push(item.ID);
                            }
                        });

                        AttributeService.setDeliveries(option.attrID, option.ID, optionDeliveries).then(function (data) {
                            $scope.selectedOptions[option.attrID][option.ID].excludedDeliveries = _.clone(optionDeliveries, true);
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                }
            });

        };

        $scope.editOption = function (attrID, optionID, $event) {
            window.open('#/printshop/attributes/' + attrID + '/options/' + optionID + '/edit', '_blank');
            $event.stopPropagation();
        };

        function updateCountedExclusions() {
            _.each($scope.allOptions, function (options, attrID) {
                _.each(options,function(option){
                    var exclusionsToSelections = _.filter($scope.exclusions, function (exclusion) {
                        return exclusion.attrID==attrID && exclusion.optID==option.ID && $scope.selectedOptions[exclusion.excAttrID] && $scope.selectedOptions[exclusion.excAttrID][exclusion.excOptID]
                    });

                    option.exclusions = _.map(exclusionsToSelections,function(exclusion){
                        var optionName=_.find($scope.attributes,function(attr){
                            return attr.ID==exclusion.excAttrID
                        }).name;
                        return optionName+' - '+_.find($scope.allOptions[exclusion.excAttrID],function(option){
                            return option.ID==exclusion.excOptID
                        }).name
                    });
                });
            })
        }
    });
