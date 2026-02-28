angular.module('digitalprint.app')
    .controller('printshop.OperationsCtrl', function ($scope, $filter, $modal, OperationService,
                                                      DeviceService, Notification, ProcessService) {

        OperationService.getAll().then(function (data) {
            $scope.operations = data;
        });

        $scope.sortChange = false;
        $scope.sortableOptions = {
            stop: function (e, ui) {
                $scope.sortChange = true;
            },
            axis: 'y',
            placeholder: 'success',
            handle: 'button.button-sort',
            cancel: ''
        };

        $scope.refresh = function () {
            OperationService.getAll(true).then(function (data) {
                $scope.operations = data;
            });
        };

        $scope.add = function () {
            OperationService.create($scope.form).then(function (data) {
                $scope.operations.push(data);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (operation) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-operation.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.operation = _.clone(operation);
                    $scope.form = _.clone(operation);

                    $scope.ok = function () {
                        OperationService.update($scope.form).then(function (data) {
                            operation = _.extend(operation, $scope.form);
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        });
                    }
                }
            });
        };

        $scope.devices = function (operation) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/operation-devices.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.operation = operation;

                    $scope.currentDevices = [];
                    DeviceService.getAll().then(function (data) {

                        $scope.currentDevices = _.clone(data, true);

                        OperationService.devices(operation).then(function (data) {
                            _.each(data, function (elem) {
                                var idx = _.findIndex($scope.currentDevices, {ID: elem});
                                if (idx > -1) {
                                    $scope.currentDevices[idx].selected = 1;
                                }
                            })
                        });
                    });

                    $scope.ok = function () {
                        var selectedDevices = [];
                        _.each($scope.currentDevices, function (each) {
                            if (each.selected === 1) {
                                selectedDevices.push(each.ID);
                            }
                        });

                        OperationService.setDevices(operation, selectedDevices).then(function (data) {
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.processes = function (operation) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/operation-processes.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.operation = operation;

                    $scope.currentProcesses = [];
                    ProcessService.getAll().then(function (data) {

                        $scope.currentProcesses = _.clone(data, true);

                        OperationService.processes(operation).then(function (data) {
                            _.each(data, function (elem) {
                                var idx = _.findIndex($scope.currentProcesses, {ID: elem});
                                if (idx > -1) {
                                    $scope.currentProcesses[idx].selected = 1;
                                }
                            })
                        });
                    });

                    $scope.ok = function () {
                        var selectedProcesses = [];
                        _.each($scope.currentProcesses, function (each) {
                            if (each.selected === 1) {
                                selectedProcesses.push(each.ID);
                            }
                        });

                        OperationService.setProcesses(operation, selectedProcesses).then(function (data) {
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (id) {
            OperationService.remove(id).then(function (data) {
                var idx = _.findIndex($scope.operations, {ID: id});
                $scope.operations.splice(idx, 1);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error') + " " + data.info)
            })
        };

        $scope.sortCancel = function () {
            $scope.refresh();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.operations, function (item) {
                result.push(item.ID);
            });

            OperationService.sort(result).then(function (data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };

        $scope.search = function () {
            var newFilter = {};
            for(var filter in $scope.filterData){
                if($scope.filterData[filter] != ''){
                    newFilter[filter] = $scope.filterData[filter];
                }
            }
            $scope.filterData = newFilter;
        };

    });