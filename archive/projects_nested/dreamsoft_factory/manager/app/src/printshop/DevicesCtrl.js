angular.module('digitalprint.app')
    .controller('printshop.DevicesCtrl', function ($scope, $filter, $modal, DeviceService, Notification,
                                                   DepartmentService) {

        DeviceService.getAll().then(function (data) {
            $scope.devices = data;
        });

        DepartmentService.getAll().then(function (data) {
            $scope.departments = data;
        });

        $scope.sortChange = false;

        $scope.sortableOptions = {
            stop: function(e, ui) {
                $scope.sortChange = true;
            },
            axis: 'y',
            placeholder: 'success',
            handle: 'button.button-sort',
            cancel: ''
        };

        $scope.add = function () {
            DeviceService.create($scope.form).then(function (data) {
                $scope.devices.push(data);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (device) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-device.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.device = device;
                    $scope.form = device;

                    $scope.ok = function () {
                        DeviceService.update($scope.form).then(function (data) {
                            if( data.response ) {
                                device = data.item;
                                var idx = _.findIndex($scope.devices, {ID: data.item.ID});
                                if( idx > -1 ) {
                                    $scope.devices[idx] = data.item;
                                }
                                $modalInstance.close();
                                Notification.success($filter('translate')('success'));
                            } else {
                                Notification.error($filter('translate')('error'));
                            }
                        });
                    }
                }
            });
        };

        $scope.same = function (device) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/device-same-devices.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.device = _.clone(device);
                    $scope.currentDevices = _.clone($scope.devices, true);
                    //usuwamy maszynę którą ustawiamy
                    var idx = _.findIndex($scope.currentDevices, {ID: device.ID});
                    if (idx > -1) {
                        $scope.currentDevices.splice(idx, 1);
                    }

                    DeviceService.same(device.ID).then(function (data) {
                        _.each(data, function (each) {
                            var elem = _.findWhere($scope.currentDevices, {ID: each});
                            elem.selected = 1;
                        })
                    });

                    $scope.ok = function () {
                        var devices = [];
                        _.each($scope.currentDevices, function (each) {
                            if (each.selected) {
                                devices.push(each.ID);
                            }
                        });
                        DeviceService.setSame(device.ID, devices).then(function (data) {
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'))
                        });
                    }
                }
            })
        };

        $scope.remove = function (id) {
            DeviceService.remove(id).then(function (data) {
                var idx = _.findIndex($scope.devices, {ID: id});
                $scope.devices.splice(idx, 1);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'))
            })
        };

        $scope.sortCancel = function () {
            $scope.refresh();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.devices, function (item) {
                result.push(item.ID);
            });

            DeviceService.sort(result).then(function (data) {
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
