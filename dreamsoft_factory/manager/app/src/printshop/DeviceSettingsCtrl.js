angular.module('digitalprint.app')
    .controller('printshop.DeviceSettingsCtrl', function ($scope, $filter, $modal, DeviceService, Notification,
                                                   DepartmentService, $stateParams, ShiftService) {
        $scope.deviceID=$stateParams.deviceID;

        $scope.machineOperators = [{ID: 0, name: $filter('translate')('one_person')},
            {ID: 1, name: $filter('translate')('many_persons')}
        ];
        $scope.machineProcesses = [{ID: 0, name: $filter('translate')('one_process')},
            {ID: 1, name: $filter('translate')('many_processes')}
        ];
        $scope.machineDefaultPaths = [{ID: 0, name: $filter('translate')('simple_path')},
            {ID: 1, name: $filter('translate')('full_path')}
        ];
        $scope.countAdditionalOperations = [{ID: 0, name: $filter('translate')('do_not_count')},
            {ID: 1, name: $filter('translate')('count')}
        ];
        $scope.runningTasksAlerts = [{ID: 0, name: $filter('translate')('do_not_show')},
            {ID: 1, name: $filter('translate')('show')}
        ];

        $scope.operationPlannedTimes = [{ID: 0, name: $filter('translate')('do_not_show')},
            {ID: 1, name: $filter('translate')('show')}
        ];

        DeviceService.get($scope.deviceID).then(function (data) {
            $scope.deviceName = data.name;
        });

        function getSettings(){
            DeviceService.getSettings($scope.deviceID).then(function (data) {
                $scope.form = data;
            });
        }
        getSettings();
        $scope.saveSettings=function(){
            var sendData = $scope.form;
            if(sendData.worksInSaturday == true){
                sendData.worksInSaturday = 1;
            }else{
                sendData.worksInSaturday = 0;
            }
            if(sendData.worksInSunday == true){
                sendData.worksInSunday = 1;
            }else{
                sendData.worksInSunday = 0;
            }
            DeviceService.saveSettings($scope.deviceID, sendData).then(function(data){
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                    getSettings();
                } else {
                    Notification.error(data.error);
                }
            });
        }

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

        ShiftService.getAllFromDevice($scope.deviceID).then(function (data) {
            $scope.shifts = data;
        });

        DeviceService.getAll(true).then(function (data) {
            $scope.devicesList = data;
            console.log($scope.devicesList);
        });

        $scope.copyFromDeviceID = null;

        $scope.addShift = function () {
            $scope.formShift.deviceID = $scope.deviceID;
            ShiftService.createForDevice($scope.formShift).then(function (data) {
                $scope.shifts.push(data.item);
                $scope.formShift = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.removeShift = function (id) {
            ShiftService.removeFromDevice(id).then(function (data) {
                if( data.response ) {
                    var idx = _.findIndex($scope.shifts, {ID: id});
                    if( idx > -1 ) {
                        $scope.shifts.splice(idx, 1);
                    }
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.sortCancel = function () {
            $scope.refresh();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.shifts, function (item) {
                result.push(item.ID);
            });

            ShiftService.sortOnDevice(result).then(function (data) {
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

        $scope.copyShift = function () {
            $scope.formCopy.copyToDeviceID = $scope.deviceID;
            ShiftService.copyFrom($scope.formCopy).then(function (data) {
                $scope.shifts = data.items;
                $scope.formCopy = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

    });
