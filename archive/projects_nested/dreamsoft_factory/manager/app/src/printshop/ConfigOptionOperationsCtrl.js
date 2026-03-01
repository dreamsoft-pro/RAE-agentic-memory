angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionOperationsCtrl', function ($scope, $modal, $filter, $rootScope, getData, Notification,
                                                                  PsConfigOptionService, OperationService, DeviceService, $q) {

        var currentAttrID = $scope.currentAttrID = getData.currentAttrID;
        var currentOptID = $scope.currentOptID = getData.currentOptID;

        $scope.option = angular.copy(getData.option);
        $scope.attribute = angular.copy(getData.attribute);
        $scope.menu = getData.menu;
        $scope.prevOption = getData.prevOption;
        $scope.nextOption = getData.nextOption;
        $rootScope.currentAttrName = getData.attribute.name;
        $rootScope.currentOptionName = getData.option.name;

        var ConfigOptionService = new PsConfigOptionService(currentAttrID);

        var ControllerService = PsConfigOptionService.getControllerService($scope.attribute.type);

        ControllerService.getAll().then(function (data) {
            $scope.controllers = data;
        });

        OperationService.getAll().then(function (data) {
            $scope.operations = data;
        }, function (data) {
            console.log("Error", data);
        });

        $scope.selectController = function (controller) {
            $scope.selectedController = controller;
            ConfigOptionService.getOperations(currentOptID, $scope.selectedController.ID).then(function (data) {
                var devices = data.response;
                var operations = [];
                _.each(devices, function (device) {
                    var operationIdx = _.findIndex(operations, {operationID: device.operationID});
                    if (operationIdx > -1) {
                        operations[operationIdx].devices.push({deviceID:device.deviceID})
                    } else {
                        operations.push({operationID: device.operationID, devices: [{deviceID:device.deviceID}]});
                    }
                });
                $scope.selectedOperations = operations;
            });
        };

        $scope.setOperation = function (operationID) {

            var idx = _.findIndex($scope.selectedOperations, {operationID: operationID});
            if (idx > -1) {
                $scope.selectedOperations.splice(idx, 1);
                ConfigOptionService.saveOperations(currentOptID, $scope.selectedController.ID, $scope.selectedOperations).then(function (data) {
                    Notification.success($filter('translate')('operation_removed'));
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                    console.log("Error", data);
                });
            } else {
                $scope.selectedOperations.push({operationID: operationID, devices:[]});
                ConfigOptionService.saveOperations(currentOptID, $scope.selectedController.ID, $scope.selectedOperations).then(function (data) {
                    Notification.success($filter('translate')('operation_added'));
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                    console.log("Error", data);
                });
            }

        };

        $scope.operationOption = function (operation) {

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/option-operation-settings.html',
                scope: $scope,
                size: 'lg',
                resolve:{
                    devices:function(){
                        var def=$q.defer();
                        DeviceService.getAll().then(function(data){
                            def.resolve(data)
                        })
                        return def.promise;
                    }
                },
                controller: function ($scope, $modalInstance, devices) {
                    $scope.devices=devices;
                    var currentOperation=_.findWhere($scope.selectedOperations,{operationID:operation.ID});
                    _.each($scope.devices,function(device){
                        device.selected=_.findWhere(currentOperation.devices,{deviceID:device.ID})
                    });
                    $scope.save = function () {
                        var operations=_.clone($scope.selectedOperations);
                        var operationIndex=_.findIndex($scope.selectedOperations,{operationID:currentOperation.operationID});
                        operations[operationIndex].devices=_.filter($scope.devices,function(device){
                            return device.selected;
                        });
                        ConfigOptionService.saveOperations(currentOptID, $scope.selectedController.ID, operations)
                            .then(function (data) {
                                if(!data.response){
                                    Notification.error($filter('translate')('error'));
                                }else{
                                    Notification.success($filter('translate')('success'));
                                    $scope.selectController($scope.selectedController);
                                    $modalInstance.close();
                                }
                            }, function (data) {
                                Notification.error($filter('translate')('error'));
                                $modalInstance.close();
                            });
                    }

                }
            })
        };

    });
