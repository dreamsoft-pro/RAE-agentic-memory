angular.module('digitalprint.app')
    .controller('orders.OngoingsCtrl', function ($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, DepartmentService, $timeout,
        $window, $q) {


        $scope.form = {};
        $scope.devices = [];

        $scope.customPause = null;
        $scope.currentDeviceID = false;
        $scope.changeOperatorInAdditional = false;
        $scope.currentDevice = [];

        var modalInstancePause;
        var modalInstanceWorkplace;
        var modalInstanceOperators;

        $scope.showRows = 25;
        $scope.ongoingsConfig = {
            count: 'devices/countFilteredOngoings',
            params: {
                deviceID: $state.params.deviceID,
                finished: 0,
                inProgress: 1,
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.ongoingsCtrl.items = data;
                console.log(data);
            }
        };

        $scope.ongoingsCtrl = new ApiCollection('deviceOngoings', $scope.ongoingsConfig);

        var updateTableTimeout;
        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.ongoingsCtrl.clearCache();
                $scope.ongoingsCtrl.get();
            }, 5000);
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
                            _.each(tmp, function (tmp2, i2) {
                                    if($state.params.deviceID == tmp2.ID){
                                        $scope.currentDevice = tmp2;
                                    }
                            });
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

            if ($state.params.deviceID) {

                $scope.ongoingsCtrl.setParam('finished', 0);
                $scope.ongoingsCtrl.setParam('deviceID', $state.params.deviceID);

                $scope.ongoingsCtrl.clearCache();
            }

        }

        function reloadOngoings() {
            $scope.ongoingsCtrl.clearCache();
        }

        function countOngoings() {
            DeviceService.countOngoings().then(function (data) {
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
                    if (sameDevices.length > 0) {
                        $scope.task = _.clone(task);
                        $scope.currentDevices = [];
                        $scope.form = {};
                        _.each(sameDevices, function (each) {
                            _.each($scope.devicesByDepartments, function (each2) {
                                _.each(each2, function (each3) {
                                    if (each3.ID == each) {
                                        $scope.currentDevices.push(each3);
                                    }
                                });
                            });
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
                    } else {
                        Notification.error($filter('translate')("Brak powiazanych maszyn!"));
                    }
                }
            })
        };

        $scope.history = function (task, isAdditional) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/production-path-logs.html',
                size: 'lg',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.task = _.clone(task, true);
                    OngoingService.ongoingsLogs(task.ID, isAdditional).then(function (data) {
                        var additionals = false;
                        angular.forEach(data, function (value, key) {
                            if (data[key].isAdditional == true) {
                                additionals = true;
                            }
                            var pauseReason = "";
                            if (data[key].state == 2) {
                                if (data[key].customPause != null) {
                                    pauseReason = data[key].customPause;
                                } else if (data[key].pauseID != null) {
                                    pauseReason = data[key].pause.name;
                                }
                            }
                            data[key].pauseReason = pauseReason;
                        });
                        $scope.logs = data;
                        $scope.additionals = additionals;
                    });

                    $scope.getTime = function (item) {
                        var logs = _.where($scope.logs, { ongoingID: item.ongoingID });
                        return item.timestamp - _.first(logs).timestamp;
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

        $scope.startTask = function (task) {
            var ongoing = {};
            ongoing.state = 1;
            var allowStart = true;
            var info = "";
            if($scope.currentDevice.defaultPath === 1){
                if(!task.isSetSideType && task.doubleSidedSheet == 1){
                    info = "no_side_type_selected_in_path";
                    allowStart = false;
                }
                if(!task.isSetSheetNumber && task.sheetsInfo.rangeSheets > 1){
                    info = "no_sheet_selected_in_path";
                    allowStart = false;
                }
            }
            if(allowStart){
                if($scope.currentDevice.runningTasksAlert){
                    OngoingService.getAlreadyStartedTasks(task.ID).then(function (data) {
                        var ongoingsByOperator = data;
                        if(ongoingsByOperator.length > 0){
                            $modal.open({
                                templateUrl: 'src/orders/templates/modalboxes/production-path-alert-running.html',
                                size: 'lg',
                                scope: $scope,
                                controller: function ($scope, $modalInstance) {
                                    $scope.tasks = ongoingsByOperator;
                                }
                            });
                        }
                    });
                }

                if($scope.currentDevice.multiOperator === 1){
                    var taskOperators = [];
                    OngoingService.getOperatorsWithSkills(task.ID).then(function (data) {
                        taskOperators = data;
                        if (taskOperators.length > 0) {
                            modalInstancePause = $modal.open({
                                templateUrl: 'src/orders/templates/modalboxes/production-path-additional-operators.html',
                                size: 'lg',
                                scope: $scope,
                                controller: function ($scope, $modalInstance) {
                                    $scope.task = _.clone(task, true);
                                    $scope.form = {};
                                    $scope.taskOperators = taskOperators;
                                    $scope.additionalOperators = [];
                                    $scope.addOperator = function (operator) {
                                        if($scope.additionalOperators.includes(operator)){
                                            $scope.additionalOperators.pop(operator);
                                        }else{
                                            $scope.additionalOperators.push(operator);
                                        }
                                    };
                                    $scope.save = function () {
                                        $modalInstance.close();
                                        $scope.changeState(task, 1, $scope.additionalOperators);
                                    }
                                }
                            });
                        }else{
                            $modalInstance.close();
                            $scope.changeState(task, 1, null);
                        }
                    });
                }else{
                    $scope.changeState(task, 1, null);
                }
            }else{
                Notification.error($filter('translate')('error') + ': ' + $filter('translate')(info));
            }
        };

        $scope.changeState = function (task, state, additionalOperators) {
            var ongoing = {};
            ongoing.state = state;
            var renew = null;
            if (state === 3) {
                ongoing.finished = 1;
            }
            if (state === 1 && task.sheetNumber > 0) {
                renew = task.sheetNumber;
            }
            ongoing.processID = task.processID;
            ongoing.additionalOperators = additionalOperators;

            OngoingService.patchOngoings(task.ID, ongoing).then(function (data) {

                task = _.extend(task, ongoing);
                if (ongoing.finished) {
                    reloadOngoings();
                    countOngoings();
                }
                if(renew == null){
                    Notification.success($filter('translate')(data.info));
                }else{
                    Notification.success($filter('translate')("resume_from_sheet_number: "+renew));
                }
            }, function (data) {
                Notification.error($filter('translate')('error') + ': ' + $filter('translate')(data.info));
            });
        };

        $scope.changeStatePause = function (task, pause, customPauseValue) {
            modalInstancePause.close();
            var state = 2;
            var ongoing = {};
            ongoing.state = state;
            ongoing.processID = task.processID;
            if(pause){
                ongoing.pauseID = pause.ID;
            }
            ongoing.customPause = customPauseValue;
            ongoing.sheetNumber = null;

            if(pause && pause.report_sheets == 1){
                modalInstancePause = $modal.open({
                    templateUrl: 'src/orders/templates/modalboxes/production-path-pause-report-sheets.html',
                    size: 'sm',
                    scope: $scope,
                    controller: function ($scope, $modalInstance) {
                        $scope.task = task;
                        $scope.saveProgressTask = function(task) {
                            $modalInstance.dismiss('cancel');
                            OngoingService.patchOngoings(task.ID, ongoing).then(function (data) {
                                var toSave = {
                                    ongoingID: task.ID,
                                    madeSheets: task.madeSheets,
                                    madeSheetsReverse: task.madeSheetsReverse
                                };
                                OngoingService.saveProgress(toSave).then(function (data) {
                                    if (data.response) {
                                        Notification.success($filter('translate')('saved_message'));
                                        task = _.extend(task, ongoing);
                                        reloadOngoings();
                                        countOngoings();
                                    } else {
                                        Notification.error($filter('translate')('error'));
                                    }
                                }, function () {
                                    Notification.error($filter('translate')('error'));
                                });
                            }, function (data) {
                                Notification.error($filter('translate')('error') + ': ' + $filter('translate')(data.info));
                            });
                        };
                    }
                });
            }else{
                OngoingService.patchOngoings(task.ID, ongoing).then(function (data) {
                    task = _.extend(task, ongoing);
                    reloadOngoings();
                    countOngoings();
                    Notification.success($filter('translate')(data.info));
                }, function (data) {
                    Notification.error($filter('translate')('error') + ': ' + $filter('translate')(data.info));
                });
            }
        };

        $scope.pauseTask = function (task) {
            var pausesArray = [];
            PauseService.getAll().then(function (data) {
                pausesArray = data;
                if (pausesArray.length > 0) {
                    modalInstancePause = $modal.open({
                        templateUrl: 'src/orders/templates/modalboxes/production-path-pause.html',
                        size: 'lg',
                        scope: $scope,
                        controller: function ($scope, $modalInstance) {
                            $scope.task = task;
                            $scope.pauses = pausesArray;
                        }
                    });
                } else {
                    $scope.changeState(task, 2, null);
                }
            });
        };

        $scope.changeToWorkplace = function (workplace) {
            modalInstanceWorkplace.close();
            OngoingService.patchWorkplace(workplace).then(function (data) {
                reloadOngoings();
                countOngoings();
                Notification.success($filter('translate')(data.info));
            }, function (data) {
                Notification.error($filter('translate')('error') + ': ' + $filter('translate')(data.info));
            });
        };

        $scope.changeWorkplace = function (task) {
            var taskWorkplaces = [];
            OngoingService.getTaskWorkplaces(task.itemID).then(function (data) {
                taskWorkplaces = data;
                if (taskWorkplaces.length > 0) {
                    modalInstanceWorkplace = $modal.open({
                        templateUrl: 'src/orders/templates/modalboxes/production-path-workplaces.html',
                        size: 'lg',
                        scope: $scope,
                        controller: function ($scope, $modalInstance) {
                            $scope.task = _.clone(task, true);
                            $scope.workplaces = taskWorkplaces;
                        }
                    });
                }
            });
        };

        $scope.changeOperator = function (task) {
            var taskOperators = [];
            OngoingService.getOperatorsWithSkills(task.ID).then(function (data) {
                taskOperators = data;
                if (taskOperators.length > 0) {
                    modalInstanceOperators = $modal.open({
                        templateUrl: 'src/orders/templates/modalboxes/production-path-operators.html',
                        size: 'lg',
                        scope: $scope,
                        controller: function ($scope, $modalInstance) {
                            $scope.task = _.clone(task, true);
                            $scope.operators = taskOperators;
                            $scope.changeOperatorInAdditional = false;
                        }
                    });
                }
            });
        };

        $scope.changeToOperator = function (operator, isAdditional) {
            modalInstanceOperators.close();
            if(isAdditional == false){
                OngoingService.patchOperator(operator).then(function (data) {
                    reloadOngoings();
                    countOngoings();
                    Notification.success($filter('translate')(data.info));
                }, function (data) {
                    Notification.error($filter('translate')('error') + ': ' + $filter('translate')(data.info));
                });
            }else{
                OngoingService.patchOperatorAdditional(operator).then(function (data) {
                    reloadOngoings();
                    countOngoings();
                    Notification.success($filter('translate')(data.info));
                }, function (data) {
                    Notification.error($filter('translate')('error') + ': ' + $filter('translate')(data.info));
                });
            }
        };

        $scope.changeProcess = function (task, processID) {
            var ongoing = {};
            ongoing.processID = processID;

            if (task.processID === processID) {
                if (task.state === 2) {
                    Notification.warning($filter('translate')('process_is_stopped'));
                    return;
                } else if (task.state === 1) {
                    Notification.warning($filter('translate')('process_already_running'));
                    return;
                }
                return;
            }

            if (task.sheetNumber) {
                ongoing.sheetNumber = task.sheetNumber;
            }

            if (task.processSideType) {
                ongoing.processSideType = task.processSideType;
            }

            if (task.state === 1) {

                ongoingPause(task).then(function (saved) {
                    if (saved) {
                        ongoing.state = 1;
                        changeOngoing(task, ongoing, processID);
                    }
                });
            } else {

                if (task.sheetsInfo.rangeSheets > 1 && !task.sheetNumber) {

                    Notification.warning($filter('translate')('select_printed_sheet'));
                    return false;

                }

                if (task.doubleSidedSheet === 1 && !task.processSideType) {
                    Notification.warning($filter('translate')('select_side_of_process'));
                    return false;
                }

                ongoing.state = 1;
                changeOngoing(task, ongoing, processID);
            }

        };

        function ongoingPause(task) {
            var def = $q.defer();

            var ongoing = {};
            ongoing.state = 2;

            OngoingService.patchOngoings(task.ID, ongoing).then(function (data) {
                task = _.extend(task, ongoing);
                def.resolve(true);
            }, function (data) {
                def.reject(data.info);
            });


            return def.promise;
        }

        function changeOngoing(task, ongoing, processID) {
            OngoingService.patchOngoings(task.ID, ongoing).then(function (data) {
                task = _.extend(task, ongoing);
                _.each(task.operation.processes, function (process) {
                    process.selected = false;
                    if (process.ID === processID) {
                        process.selected = true;
                    }
                });
                Notification.success($filter('translate')('saved_message'));
            }, function (data) {
                Notification.error($filter('translate')('error') + ': ' + $filter('translate')(data.info));
            });
        }

        $scope.showOrderMessage = function (task) {

            if (!task.orderMessage) {
                return false;
            }

            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/show-order-message.html',
                size: 'lg',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.orderID = task.orderID;
                    $scope.orderMessage = task.orderMessage;

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };
                }
            })

        };

        $scope.getProductCard = function (productID) {

            ProductCardService.get(productID).then(function (data) {
                if (data.success === true) {
                    $window.open(data.link, '_blank');
                }
            });

            return true;
        };

        $scope.saveProgress = function (task) {
            var toSave = {
                ongoingID: task.ID,
                madeSheets: task.madeSheets,
                madeSheetsReverse: task.madeSheetsReverse
            };

            OngoingService.saveProgress(toSave).then(function (data) {
                if (data.response) {
                    countOngoings();
                    reloadOngoings();
                    Notification.success($filter('translate')('saved_message'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function () {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.selectSheetNumber = function (task, number) {
            task.isSetSheetNumber = 1;
            task.isSetSideType = 1;
            if (task.sheetNumber !== number) {
                task.processSideType = 1;
                task.sheetNumber = number;
            }
        };

        $scope.selectProcessSideType = function (task, type) {
            task.isSetSideType = 1;
            if (task.processSideType !== type) {
                task.processSideType = type;
            }

        };

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

        $scope.sumOngoings = function (devices) {
            var sum = 0;
            _.each(devices, function (device) {
                var countIfnfo = _.findWhere($scope.countOngoings, { ID: device.ID });
                if (countIfnfo) {
                    sum += countIfnfo.countTasks;
                }
            });
            return sum;
        };

        $scope.additionalOperation = function (task, currentDevice) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/production-path-additional_operation.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = {};
                    if(currentDevice.countAdditionalOperation && currentDevice.countAdditionalOperation == 1){
                        $scope.form.countTime = 1;
                    }                     
                    $scope.currentDevice = _.clone(currentDevice, true);
                    $scope.ok = function (data) {
                        var operation = {};
                        operation.ongoingID = task.ID;
                        operation.operationName = $scope.form.name;
                        operation.operationDesc = $scope.form.description;
                        operation.calculateTime = $scope.form.countTime;
                        console.log($scope.form.countTime);
                        OngoingService.addAdditionalOperation(operation).then(function (data) {
                            countOngoings();
                            reloadOngoings();
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            })
        };

        $scope.changeStateAdditional = function (task, state) {
            var operation = {};
            operation.state = state;
            operation.ID = task.ID;

            OngoingService.patchOngoingAdditional(operation).then(function (data) {
                //task = _.extend(task, operation);
                    reloadOngoings();
                    countOngoings();
                Notification.success($filter('translate')(data.info));
            }, function (data) {
                Notification.error($filter('translate')('error') + ': ' + $filter('translate')(data.info));
            });
        };

        $scope.changeOperatorAdditional = function (task) {
            var taskOperators = [];
            OperatorService.getAll().then(function (data) {
                taskOperators = data;
                _.each(taskOperators, function (taskOperator) {
                    taskOperator.ongoingID = task.ID;
                });
                if (taskOperators.length > 0) {
                    modalInstanceOperators = $modal.open({
                        templateUrl: 'src/orders/templates/modalboxes/production-path-operators.html',
                        size: 'lg',
                        scope: $scope,
                        controller: function ($scope, $modalInstance) {
                            $scope.task = _.clone(task, true);
                            $scope.operators = taskOperators;
                            $scope.changeOperatorInAdditional = true;
                        }
                    });
                }
            });
        };

        init();

    });
