angular.module('digitalprint.app')
    .controller('orders.PlannedCtrl', function ($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, DepartmentService, $timeout,
        $window, $q, ScheduleService) {

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

        $scope.sortCancel = function () {
            $scope.refresh();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            var ongoingsOrder = [];
            var tmpdevices = $scope.devicesByDepartments;
            _.each(tmpdevices, function (tmp, i) {
                _.each(tmp, function (tmp2, i2) {
                    _.each(tmp2.planned, function (singleOngoing, i3) {
                        ongoingsOrder.push(singleOngoing.ID);
                        result.push(singleOngoing.productID);
                    });
                });
            });

            ScheduleService.sort(result).then(function (data) {
                $scope.sortChange = false;
                OngoingService.sort(ongoingsOrder).then(function (dataOngoingSort) {
                    Notification.success($filter('translate')('success'));
                }, function (dataOngoingSort) {
                    Notification.error($filter('translate')('error'));
                    $scope.sortCancel();
                });
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });

        };


        $scope.form = {};
        $scope.devices = [];

        $scope.customPause = null;

        $scope.currentDeviceID = false;

        //@todo: fix limit params
        $scope.showRows = 999999;
        $scope.ongoingsConfig = {
            count: 'devices/countFilteredOngoings',
            params: {
                finished: 0,
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                var tmpdevices = $scope.devicesByDepartments;
                _.each(tmpdevices, function (tmp, i) {
                    _.each(tmp, function (tmp2, i2) {
                        tmp2.planned = [];
                        _.each(data, function (singleOngoing, i3) {
                            if (singleOngoing.deviceID == tmp2.ID) {
                                tmp2.planned.push(singleOngoing);
                            }
                        });
                    });
                });
                $scope.ongoingsCtrl.items = data;
            }
        };

        $scope.ongoingsCtrl = new ApiCollection('deviceOngoingsPlanned', $scope.ongoingsConfig);

        var updateTableTimeout;
        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.ongoingsCtrl.get();
            }, 1000);
        };

        $scope.go = function (device) {
            if ($state.params.deviceID === device.ID) {

                $scope.ongoingsCtrl.setParam('deviceID', device.ID);
                $scope.ongoingsCtrl.get();


            } else {
                $state.go($state.current.name, { deviceID: device.ID });
            }
        };

        $scope.seeFinished = function (show) {
            var showInProgress;
            if (show) {
                showInProgress = 0;
            } else {
                showInProgress = 1;
            }
            $scope.ongoingsCtrl.setParam('finished', show);
            $scope.ongoingsCtrl.setParam('inProgress', showInProgress);
            $scope.ongoingsCtrl.get();
        };

        function init() {
            $q.all([DeviceService.getAll(), DepartmentService.getAll()])
                .then(function (data) {
                    $scope.devicesByDepartments = [];
                    _.each(data[1], function (dep, i) {
                        $scope.devicesByDepartments.push(_.filter(data[0], function (dev) {
                            return dev.departmentID === dep.ID;
                        }));
                    });

                    var tmpdevices = $scope.devicesByDepartments;
                    $scope.devicesByDepartments = [];
                    _.each(tmpdevices, function (tmp, i) {
                        if (tmp.length > 0) {
                            $scope.devicesByDepartments.push(tmp);
                        }
                    });

                    $scope.departments = data[1];

                    var selectedDevice = _.find(data[0], function (item) {
                        return $scope.ongoingsConfig.params.deviceID === item.ID;
                    });
                    if (selectedDevice) {
                        $scope.deviceName = selectedDevice.name;
                    }
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                });

            OperationService.getAll().then(function (data) {
                $scope.operations = data;
            });
            OperatorService.getAll().then(function (data) {
                $scope.operators = data;
            });

            countOngoings();

            $scope.ongoingsCtrl.setParam('finished', 0);
            $scope.ongoingsCtrl.clearCache();

        }

        function reloadOngoings() {
            $scope.ongoingsCtrl.clearCache();
        }

        function countOngoings() {
            DeviceService.countOngoingsPlanned().then(function (data) {
                $scope.countOngoings = data;
                _.each($scope.departments, function (department) {
                    department.count = 2
                })
            });
        }

        $scope.move = function (task) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/production-path-move.html',
                scope: $scope,
                resolve: {
                    sameDevices: function () {
                        return DeviceService.same(task.deviceID).then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, sameDevices) {
                    $scope.task = _.clone(task);
                    $scope.currentDevices = [];
                    $scope.form = {};

                    _.each(sameDevices, function (each) {
                        var elem = _.findWhere($scope.devices, { ID: each });
                        $scope.currentDevices.push(elem);
                    });
                    $scope.form.deviceID = _.first($scope.currentDevices).ID;

                    $scope.ok = function (data) {
                        DeviceService.ongoingMove(task.deviceID, task.ID, $scope.form.deviceID).then(function (data) {
                            countOngoings();
                            reloadOngoings();
                            var idx = _.findIndex($scope.tasks, { ID: task.ID });
                            if (idx > -1) {
                                $scope.tasks.splice(idx, 1);
                            }
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            })
        };

        $scope.formatTime = function (timeInSeconds) {
            var seconds = pad(timeInSeconds % 60);
            var minutes = pad(Math.floor(timeInSeconds / 60) % 60);
            var hours = pad(Math.floor(timeInSeconds / 3600));

            return hours + ':' + minutes + ':' + seconds
        };

        function pad(n) {
            return (n < 10) ? ("0" + n) : n;
        }





        $scope.toHours = function (seconds) {
            if (seconds) {
                var h = Math.floor(seconds / 3600);
                seconds = seconds - h * 3600;
                var m = Math.floor(seconds / 60);
                var formated = '';
                if (h > 0) {
                    formated = h;
                }
                if (m > 0) {
                    if (h > 0) {
                        formated += ':';
                    }
                    formated += m
                }
                if (formated) {
                    if (h > 0) {
                        formated += ' h';
                    } else if (m > 0) {
                        formated += ' m';
                    }
                }
                return formated;
            }
            return '';
        };

        $scope.sumOngoings = function (devices, departmentID) {
            var sum = 0;
            _.each(devices, function (device) {
                if (device.planned && device.departmentID == departmentID) {
                    var count = device.planned.length;
                    sum += count;
                }
            });
            return sum;
        };

        init();

    });