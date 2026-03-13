angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionsCtrl', function ($rootScope, $scope, $modal, $stateParams, $filter, $state, $q,
                                                         Notification, PsConfigAttributeService, UploadService,
                                                         PsConfigOptionService, ConnectOptionService, FileUploader,
                                                         $config, AuthDataService, $http, SettingService) {

        var settings = new SettingService('additionalSettings');
        $scope.filteredAttribute;
        settings.getAll().then(function (data) {
            $scope.filteredAttribute = data.filteredAttribute.value;
        });
        $scope.showAll = $state.current.name == 'printshop-attributes-options'
        $scope.options = [];
        resetForm();
        $scope.sortChange = false;
        $scope.isExportFileUploading = true;
        $scope.isImportFileUploading = true;

        var currentAttrID = $scope.currentAttrID = $scope.showAll ? '' : parseInt($stateParams.attrID);

        var ConfigOptionService = new PsConfigOptionService(currentAttrID);

        var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

        $scope.sortableOptions = {
            stop: function (e, ui) {
                $scope.sortChange = true;
            },
            axis: 'y',
            placeholder: 'success',
            handle: 'button.button-sort',
            cancel: ''
        };

        function loadData() {
            $q.all([PsConfigAttributeService.getAll(true), ConfigOptionService.getAll(true)]).then(function (data) {
                $scope.attributes = data[0];
                if (!$scope.showAll) {
                    $scope.attr = _.findWhere($scope.attributes, {ID: currentAttrID});
                    $rootScope.currentAttrName = $scope.attr.name;
                }
                $scope.options = data[1];
                _.each($scope.options, function (option) {
                    var attr = _.find($scope.attributes, function (attr) {
                        return option.attrID == attr.ID;
                    });
                    if (attr) {
                        option.attrName = attr.name;
                        option.sortAttr = attr.sort;
                    }
                });
                $scope.options = _.sortBy($scope.options, 'sortAttr');
            });
        }

        loadData();

        $scope.countProducts = {};
        PsConfigAttributeService.countProducts().then(function (data) {
            $scope.countProducts = data;
        });

        $scope.groupOptions = [];
        ConnectOptionService.getAll().then(function (data) {
            $scope.groupOptions = data;
            var defaultGr = {ID: 0, name: $filter('translate')('select')};
            $scope.groupOptions.unshift(defaultGr);
        });


        function resetForm() {
            $scope.form = {};
            $scope.form.type = 1;
        }

        //IMPORT/EXPORT PRICES START
        $scope.exportPrices = function () {
            $scope.isExportFileUploading = false;
            $scope.export($scope.form.exportModel).then(function (data) {
                if (data.response) {
                    $modal.open({
                        templateUrl: 'shared/templates/modalboxes/files.html',
                        scope: $scope,
                        controller: function ($scope, $modalInstance) {
                            $scope.filesTitle = 'prices_export';
                            $scope.files = [data.url];
                            $scope.fileLabel = 'filesLabel';
                        }
                    });
                } else {
                    Notification.error(data.data);
                }
                $scope.isExportFileUploading = true;
            });
        };
        $scope.export = function (lang) {
            var def = $q.defer();
            var resource = 'price_exporter';
            $http({
                method: 'POST',
                url: $config.API_URL + resource + '',
                data: {
                    attributeID: parseInt($stateParams.attrID),
                    exportType: "kilos",
                    "domainID": $scope.currentDomain.ID
                }
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                console.log("error");
                Notification.error($filter('translate')('error'));
                def.reject(data);
            });
            return def.promise;
        };
        var accessTokenName = $config.API_ACCESS_TOKEN_NAME;
        var header = {};
        header[accessTokenName] = AuthDataService.getAccessToken();
        $scope.uploader = new FileUploader({
            url: $config.API_URL + 'price_importer',
            headers: header,
            autoUpload: false,
            queueLimit: 1
        });
        $scope.createForm = function () {
            $scope.form = {};
        };
        $scope.importPrices = function () {
            $scope.isImportFileUploading = false;
            UploadService.upload($scope.uploader, {
                'importType': $scope.form.importType,
                'domainID': $scope.currentDomain.ID
            }).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('successfully_updated_positions') + ": " + data.updated);
                    $scope.createForm();
                } else {
                    Notification.error(data.data);
                }
                $scope.isImportFileUploading = true;
            });
        };
        //IMPORT/EXPORT PRICES END

        $scope.getCountProducts = function (item) {
            if (!$scope.countProducts.opts || !$scope.countProducts.opts[currentAttrID]) {
                return 0;
            }
            return _.keys($scope.countProducts.opts[currentAttrID][item.ID]).length || 0;
        };

        $scope.getCountProductsList = function (item) {
            if (!$scope.countProducts.opts || !$scope.countProducts.opts[currentAttrID]) {
                return '';
            }

            return _.pluck($scope.countProducts.opts[currentAttrID][item.ID], 'type').join(', ');
        };

        $scope.refresh = function () {
            loadData()
            $scope.sortChange = false;
        };

        $scope.sortCancel = function () {
            $scope.refresh();
        };

        $scope.sortSave = function () {

            var result = [];
            _.forEach($scope.options, function (elem) {
                result.push(elem.ID);
            });

            ConfigOptionService.sort(result).then(function (data) {
                $scope.sortChange = false;
            });
        };

        $scope.copy = function (option) {

            new PsConfigOptionService(option.attrID).copy(option.ID).then(function (data) {
                $scope.refresh();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.add = function () {

            ConfigOptionService.add($scope.form).then(function (data) {
                $scope.options.push(data);
                resetForm();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.saveAuthCalculation = function (option) {
            ConfigOptionService.edit(option).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.savePrintRotated = function (option) {
            ConfigOptionService.edit(option).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.editStart = function (elem) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-option.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.oryg = elem;
                    $scope.form = {};
                    $scope.form = angular.copy(elem);

                    $scope.save = function () {
                        ConfigOptionService.edit($scope.form).then(function (data) {
                            var idx = _.findIndex($scope.options, {ID: $scope.form.ID});

                            if (idx > -1) {
                                $scope.options[idx] = angular.copy($scope.form);
                            }
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.uploadIcon = function (optionForm) {
                        $modal.open({
                            templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                            scope: $scope,
                            backdrop: 'static',
                            keyboard: false,
                            controller: function ($scope, $modalInstance) {

                                var header = {};
                                header[accessTokenName] = AuthDataService.getAccessToken();

                                var uploader = $scope.uploader = new FileUploader({
                                    'url': ConfigOptionService.getUploadUrl(),
                                    queueLimit: 1,
                                    headers: header,
                                    'autoUpload': false
                                });

                                uploader.filters.push({
                                    name: 'imageFilter',
                                    fn: function (item, options) {
                                        var itemName = item.name.split('.');
                                        var lastItem = itemName.pop();
                                        var possibleExtensions = ['jpg', 'jpeg', 'png', 'svg','webp'];

                                        if (possibleExtensions.indexOf(lastItem) > -1) {
                                            return true;
                                        }
                                        Notification.warning($filter('translate')('required_ext') + possibleExtensions.join(','));
                                        return false;
                                    }
                                });

                                $scope.ok = function () {

                                    var file = uploader.queue[0];
                                    $scope.file = file;

                                    var formData = [];

                                    formData.push({'optionID': optionForm.ID});
                                    file.formData = formData;

                                    uploader.uploadItem(file);

                                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                                        if (response.response === true) {

                                            optionForm.icon = response.icon;
                                            var optionIdx = _.findIndex($scope.options, {ID: optionForm.ID});
                                            if (optionIdx > -1) {
                                                $scope.options[optionIdx].icon = response.icon;
                                            }
                                            Notification.success($filter('translate')('file_uploaded'));
                                            $modalInstance.close();
                                        } else {
                                            Notification.success($filter('translate')('uploading_problem'));
                                        }
                                    };
                                };

                                $scope.cancel = function () {
                                    if (uploader.isUploading) {
                                        alert('Upload trwa! Poczekaj na zakończenie uploadu lub anuluj go przed zamknięciem')
                                    } else {
                                        $modalInstance.close();
                                    }
                                }
                            }
                        });
                    };

                    $scope.deleteIcon = function (optionForm) {

                        ConfigOptionService.removeIcon(optionForm.ID).then(function (data) {
                            if (data.response) {
                                optionForm.icon = null;
                                var optionIdx = _.findIndex($scope.options, {ID: optionForm.ID});
                                if (optionIdx > -1) {
                                    $scope.options[optionIdx].icon = null;
                                    Notification.success($filter('translate')('deleted_successful'));
                                }
                            }
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })
        };

        $scope.remove = function (elem) {

            new PsConfigOptionService(elem.attrID).remove(elem).then(function (data) {
                var idx = _.findIndex($scope.options, {ID: elem.ID});
                if (idx > -1) {
                    $scope.options.splice(idx, 1);
                }
                Notification.success($filter('translate')('removed') + " " + elem.name);
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.connectOptions = function () {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/connect-options.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {

                    $scope.form = {};

                    $scope.save = function () {

                        ConnectOptionService.add($scope.form).then(function (data) {

                            $scope.groupOptions.push(data.item);

                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                    $scope.editConnectStart = function (elem) {
                        $modal.open({
                            templateUrl: 'src/printshop/templates/modalboxes/edit-connect-option.html',
                            scope: $scope,
                            controller: function ($scope, $modalInstance) {
                                $scope.oryg = elem;
                                $scope.form = {};
                                $scope.form = angular.copy(elem);

                                $scope.save = function () {
                                    ConnectOptionService.edit($scope.form).then(function (data) {

                                        var idx = _.findIndex($scope.groupOptions, {ID: $scope.form.ID});

                                        if (idx > -1) {
                                            $scope.groupOptions[idx] = angular.copy($scope.form);
                                        }
                                        $modalInstance.close();
                                        Notification.success($filter('translate')('success'));
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

                    $scope.editPaperPrice = function (connect) {
                        $modal.open({
                            templateUrl: 'src/printshop/templates/modalboxes/set-prices-connect-option.html',
                            scope: $scope,
                            resolve: {
                                prices: function () {
                                    return ConnectOptionService.getPrices(connect).then(function (data) {
                                        return data;
                                    });
                                }
                            },
                            controller: function ($scope, $modalInstance, prices) {
                                $scope.connectOption = connect;
                                $scope.prices = prices;
                                $scope.form = {};

                                $scope.save = function () {

                                    ConnectOptionService.setPrice(connect, $scope.form).then(function (data) {

                                        if (data.response) {
                                            var idx = _.findIndex($scope.prices, {ID: data.item.ID});
                                            if (idx > -1) {
                                                $scope.prices[idx] = data.item;
                                            } else {
                                                $scope.prices.push(data.item);
                                            }
                                            Notification.success($filter('translate')('success'));
                                        } else {
                                            Notification.error($filter('translate')('error'));
                                        }

                                    }, function (data) {
                                        Notification.error($filter('translate')('error'));
                                    });

                                };

                                $scope.removePrice = function (price) {
                                    ConnectOptionService.removePrice(price).then(function (data) {
                                        if (data.response) {

                                            var idx = _.findIndex($scope.prices, {ID: price.ID});

                                            if (idx > -1) {
                                                $scope.prices.splice(idx, 1);
                                            }

                                            Notification.success($filter('translate')('success'));
                                        }
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

                }
            });
        };

        $scope.idFilter = function (elem) {
            return elem.ID > 0;
        };

        $scope.deleteConnectOption = function (connectOption) {
            ConnectOptionService.remove(connectOption.ID).then(function (data) {
                if (data.response) {

                    var idx = _.findIndex($scope.groupOptions, {ID: connectOption.ID});

                    if (idx > -1) {
                        $scope.groupOptions.splice(idx, 1);
                    }

                    Notification.success($filter('translate')('success'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.changeConnect = function (option) {

            var idx = _.findIndex($scope.groupOptions, {ID: option.connectID});

            if (idx === -1) {
                option.connectID = 0;
                return;
            }

            ConnectOptionService.addToGroup(option).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('saved_message'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

        $scope.editRelativeOptions = function (option) {
            var ConfigOptionService = new PsConfigOptionService($stateParams.attrID);
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-relative-options.html',
                scope: $scope,
                resolve: {
                    filterConfigData: function () {
                        return PsConfigAttributeService.getFilterConfig($scope.filteredAttribute).then(function (data) {
                            return data;
                        });
                    },
                    filterData: function () {
                        return ConfigOptionService.getRelativeOptionsFilter(option.ID).then(function (data) {
                            return data;
                        });
                    },
                    allOptions: function () {
                        return PsConfigAttributeService.getOptions($scope.filteredAttribute).then(function (data) {
                            _.each(data, function (item) {
                                item.descriptions.weight = item.weight
                                item.descriptions.thickness = item.pageSize
                                _.each(['certificates', 'printingTechniques', 'color_hex', 'application', 'category', 'group', 'paper_type'],
                                    function (name) {
                                        if(item.descriptions[name]){
                                            return;
                                        }
                                        item.descriptions[name] = item.descriptions[name] ? _.map(item.descriptions[name].split(','),
                                            function (value) {
                                                return value.trim()
                                            }):[]
                                    })
                            })
                            return data;
                        });
                    },
                },
                controller: function ($scope, $modalInstance, filterConfigData, filterData, allOptions) {
                    var filterParts = [];
                    var filterConfig = filterConfigData.filterConfig;
                    var descriptionsMap = filterConfigData.descriptionsMap;

                    function createFilterPart(items, name, type, filterConfig, label, hidden, precision) {
                        try {
                            items = _.clone(items);
                            var item = {name: name, type: type, title: !!label ? label : name, hidden: hidden};
                            switch (type) {
                                case 'select':
                                case 'multi-select':
                                case 'multi-select-color':
                                    item.values = filterConfig[name].values;
                                    item.selectedValues = {};
                                    break;
                                case 'range':
                                    item.minValue0 = item.minValue = filterConfig[name].minValue;
                                    item.maxValue0 = item.maxValue = filterConfig[name].maxValue;
                                    var diff = filterConfig[name].maxValue - filterConfig[name].minValue
                                    var step = 1
                                    if (diff < 1) {
                                        step = 0.01;
                                    } else if (diff < 10) {
                                        step = 0.1;
                                    } else if (diff < 100) {
                                        step = 1
                                    } else {
                                        step = Math.round(diff / 50);
                                    }
                                    item.options = {
                                        floor: filterConfig[name].minValue,
                                        ceil: filterConfig[name].maxValue,
                                        step: step,
                                        precision: precision,
                                        onChange: function () {
                                            $scope.onInputChange.apply(this)
                                        }
                                    }
                                    break;
                            }
                            items.push(item);
                        } catch (e) {
                            console.error('Problem while creating filter part '+ e.message);
                        }
                        return items;
                    }

                    var filterParts = createFilterPart(filterParts, 'name', 'text', filterConfig, 'name_of_atrritute');
                    filterParts = createFilterPart(filterParts, 'category', 'select', filterConfig);
                    filterParts = createFilterPart(filterParts, 'group', 'select', filterConfig);
                    filterParts = createFilterPart(filterParts, 'paper_type', 'select', filterConfig);
                    filterParts = createFilterPart(filterParts, 'weight', 'range', filterConfig, null, false, 0);
                    filterParts = createFilterPart(filterParts, 'whiteness', 'range', filterConfig, null, false, 0);
                    filterParts = createFilterPart(filterParts, 'thickness', 'range', filterConfig, null, false, 3);
                    filterParts = createFilterPart(filterParts, 'opacity', 'range', filterConfig, null, false, 0);
                    filterParts = createFilterPart(filterParts, 'roughness', 'range', filterConfig, null, false, 0);
                    filterParts = createFilterPart(filterParts, 'certificates', 'multi-select', filterConfig);
                    filterParts = createFilterPart(filterParts, 'printingTechniques', 'multi-select', filterConfig);
                    filterParts = createFilterPart(filterParts, 'application', 'multi-select', filterConfig);
                    filterParts = createFilterPart(filterParts, 'color_hex', 'multi-select-color', filterConfig, 'paper_color');
                    _.each(filterData, function (fd) {
                        var part = _.findWhere(filterParts, {name: fd.name});
                        if (fd.valueType == 'min') {
                            part.minValue = fd.value;
                        } else if (fd.valueType == 'max') {
                            part.maxValue = fd.value;
                        } else if (part.type == 'multi-select' || part.type == 'multi-select-color') {
                            if (!part.selectedValues) {
                                part.selectedValues = [];
                            }
                            part.selectedValues[fd.value] = true;
                        }  else if (fd.valueType == 'exact') {
                            part.value = String(fd.value);
                        }
                    });
                    $scope.filterParts = _.cloneDeep(filterParts);

                    $scope.withUnit = function (value, unit) {
                        if (!value) {
                            return '-';
                        }
                        return value + ' ' + unit
                    }

                    var timerId;

                    $scope.onInputChange = function (force) {
                        clearTimeout(timerId)
                        if (!(force === true)) {
                            timerId = setTimeout(function () {
                                $scope.onInputChange(true)
                            }, 1000);
                            return
                        }
                        $scope.filtersUsed = true;
                        ConfigOptionService.search($stateParams.attrID, $scope.filterParts).then(function (data) {
                            $scope.filteredOptions = data
                        }, function (error) {
                        });
                    }

                    $scope.onColorClick = function (unit, value) {
                        if (value) {
                            unit.selectedValues[value] = !unit.selectedValues[value];
                        } else {
                            unit.selectedValues = {};
                        }

                        $scope.onInputChange();
                    }

                    $scope.save = function () {
                        var filter = [];
                        _.each($scope.filterParts, function (unit) {
                            var description = _.findWhere(descriptionsMap, {name: unit.name})
                            var item = {typeID: description ? description.ID : null, name: unit.name}
                            if (unit.value) {
                                item.value = unit.value;
                                item.valueType = 'exact';
                                filter.push(_.clone(item));
                            }
                            if (unit.minValue) {
                                item.value = unit.minValue;
                                item.valueType = 'min';
                                filter.push(_.clone(item));
                            }
                            if (unit.maxValue) {
                                item.value = unit.maxValue;
                                item.valueType = 'max';
                                filter.push(_.clone(item));
                            }
                            if (unit.selectedValues) {
                                _.each(unit.selectedValues, function (value, key) {
                                    if (value) {
                                        item.value = key;
                                        item.valueType = 'exact';
                                        filter.push(_.clone(item));
                                    }
                                });
                            }
                        });
                        ConfigOptionService.saveRelativeOptionsFilter(option.ID, filter).then(function (data) {
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                            loadData();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                    $scope.onInputChange();
                }
            })
        }

        $scope.setFileUploadAvailable = function (option) {
            option.fileUploadAvailable = option.fileUploadAvailable ? 0 : 1;
            ConfigOptionService.edit(option).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };
    });
