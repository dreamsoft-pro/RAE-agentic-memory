angular.module('digitalprint.app')
    .controller('superadmin.ModulesCtrl', function ($scope, $rootScope, $filter, $modal, ModuleService, ModuleTypeService, Notification) {

        /**
         ModuleTypeService
         **/
        $scope.moduleTypes = [];
        $scope.form = {};

        function resetForm() {
            $scope.form = {};
            $scope.form.typeID = _.first($scope.moduleTypes).ID;
        }

        ModuleTypeService.getAll().then(function (data) {
            $scope.moduleTypes = data;
            resetForm();
        });

        $rootScope.$on('ModuleTypeService.getAll', function (e, data) {
            $scope.moduleTypes = data;
            resetForm();
        });

        /**
         ModuleService
         **/

        $scope.modules = [];
        $scope.filterModules = [];
        $scope.pagination = {
            perPage: 10,
            currentPage: 1
        };

        $scope.pagination.setPage = function (pageNo) {
            $scope.pagination.currentPage = pageNo;
        };

        ModuleService.getAll().then(function (data) {
            $scope.modules = data;
            $scope.filterModules = _.clone($scope.modules);

        });

        $scope.add = function () {
            ModuleService.create($scope.form).then(function (data) {
                $scope.modules.push(data);
                $scope.search(false);
                resetForm();
                Notification.success("Ok");
            }, function (data) {
                Notification.error("Error");
            });
        };

        $scope.edit = function (module) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/edit-module.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = _.clone(module);

                    $scope.ok = function () {
                        ModuleService.update($scope.form).then(function (data) {
                            module = _.extend(module, $scope.form);
                            $modalInstance.close();
                            Notification.success("Ok");
                        });
                    }
                }
            });
        };

        $scope.keys = function (module) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/module-keys.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.moduleKeys;
                    $scope.form = {};
                    $scope.keyTypes = ['text', 'select', 'password', 'number', 'price'];

                    ModuleService.getKeys(module).then(function (data) {
                        $scope.moduleKeys = data;
                    });

                    $scope.add = function () {
                        ModuleService.addKey(module.ID, $scope.form).then(function (data) {
                            $scope.moduleKeys.push(data);
                            $scope.form = {};
                            Notification.success("Ok");
                        }, function (data) {
                            console.log(data);
                            Notification.error("Error");
                        });
                    };

                    $scope.edit = function (key) {
                        $modal.open({
                            templateUrl: 'src/superadmin/templates/modalboxes/edit-module-key.html',
                            scope: $scope,
                            controller: function ($scope, $modalInstance) {
                                $scope.form = _.clone(key, true);
                                console.log($scope.form);

                                $scope.ok = function () {
                                    ModuleService.editKey(module.ID, $scope.form).then(function (data) {
                                        key = _.extend(key, $scope.form);
                                        $modalInstance.close();
                                        Notification.success("Ok");
                                    }, function (data) {
                                        console.log(data);
                                        Notification.error("Error");
                                    })
                                }
                            }
                        })
                    };

                    $scope.options = function (key) {
                        $modal.open({
                            templateUrl: 'src/superadmin/templates/modalboxes/module-key-options.html',
                            scope: $scope,
                            controller: function ($scope, $modalInstance) {
                                $scope.form = {};
                                $scope.options = {};

                                ModuleService.getOptions(module.ID, key.ID).then(function (data) {
                                    $scope.options = data;
                                }, function (data) {
                                    Notification.error("Get options error");
                                    $modalInstance.close();
                                });

                                $scope.add = function () {
                                    ModuleService.addOption(module.ID, key.ID, $scope.form).then(function (data) {
                                        $scope.options.push(data);
                                        Notification.success("Ok");
                                    }, function (data) {
                                        console.log(data);
                                        Notification.error("Error");
                                    })
                                };

                                $scope.edit = function (option) {
                                    $modal.open({
                                        templateUrl: 'src/superadmin/templates/modalboxes/edit-module-key-option.html',
                                        scope: $scope,
                                        controller: function ($scope, $modalInstance) {
                                            $scope.form = _.clone(option, true);

                                            $scope.ok = function () {
                                                ModuleService.editOption(module.ID, key.ID, $scope.form).then(function (data) {
                                                    option = _.extend(option, $scope.form);
                                                    $modalInstance.close();
                                                    Notification.success("Ok");
                                                }, function (data) {
                                                    console.log(data);
                                                    Notification.error("Error");
                                                });
                                            }
                                        }
                                    })
                                };

                                $scope.remove = function (optionID) {
                                    ModuleService.removeOption(module.ID, key.ID, optionID).then(function (data) {
                                        var idx = _.findIndex($scope.options, {ID: optionID});
                                        $scope.options.splice(idx, 1);
                                        Notification.success("Ok");
                                    }, function (data) {
                                        console.log(data);
                                        Notification.error("Error");
                                    });
                                }
                            }
                        });
                    };

                    $scope.remove = function (keyID) {
                        ModuleService.removeKey(module.ID, keyID).then(function (data) {
                            var idx = _.findIndex($scope.moduleKeys, {ID: keyID});
                            $scope.moduleKeys.splice(idx, 1);
                            Notification.success("Ok");
                        }, function (data) {
                            console.log(data);
                            Notification.error("Error");
                        })
                    }

                }
            })
        };

        $scope.search = function (setFirstPage) {
            if (_.isUndefined(setFirstPage)) {
                setFirstPage = true;
            }
            _.each($scope.filterData, function (item, key) {
                if (_.isNull(item)) {
                    delete $scope.filterData[key];
                }
            });

            $scope.filterModules = $filter('filter')(
                $scope.modules,
                $scope.filterData
            );
            if (setFirstPage) {
                $scope.pagination.setPage(1);
            }
        };

        $scope.remove = function (id) {

            var idx = _.findIndex($scope.modules, {
                ID: id
            });

            ModuleService.remove(id).then(function () {
                $scope.modules.splice(idx, 1);
                $scope.search(false);
                Notification.success('Success');
            });

        };


    });