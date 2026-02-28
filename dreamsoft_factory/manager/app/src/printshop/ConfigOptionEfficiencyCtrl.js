angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionEfficiencyCtrl', function ($scope, $filter, $rootScope, getData, Notification,
                                                                  PsConfigOptionService, DeviceService,
                                                                  PsPricelistService, PsPrintTypeService, PsWorkspaceService) {

        var currentAttrID = $scope.currentAttrID = getData.currentAttrID;
        var currentOptID = $scope.currentOptID = getData.currentOptID;

        $scope.option = angular.copy(getData.option);
        $scope.attribute = getData.attribute;
        $scope.menu = getData.menu;
        $scope.prevOption = getData.prevOption;
        $scope.nextOption = getData.nextOption;
        $rootScope.currentAttrName = getData.attribute.name;
        $rootScope.currentOptionName = getData.option.name;

        $scope.deviceService = DeviceService;

        var ConfigOptionService = new PsConfigOptionService(currentAttrID);

        var ControllerService = PsConfigOptionService.getControllerService($scope.attribute.type);

        ControllerService.getAll().then(function (data) {
            $scope.controllers = data;
        });

        $scope.onSelectController=function(controller){
            if(controller){
                $scope.controllerID = controller.ID;
                $scope.controllerName = controller.name;
            }else{
                delete $scope.controllerID;
                delete $scope.controllerName;
            }
            loadOverrides();
        };

        function loadOverrides() {
            getEfficiency();
            getSpeeds();
            getSpeedChanges();
            getSideRelations();
        };

        loadOverrides();

        $scope.save = function () {
            ConfigOptionService.updateEfficiency($scope.form).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error(data.error);
                }
            });
        };

        function getEfficiency() {
            ConfigOptionService.getEfficiency($scope.currentOptID, $scope.controllerID).then(function (data) {
                $scope.form = data;
            });
        }

        $scope.saveEfficiency = function () {
            ConfigOptionService.saveEfficiency($scope.currentOptID, $scope.controllerID, $scope.form).then(
                function (data) {
                    Notification.success($filter('translate')('success'));
                    getEfficiency();
                }, function (data) {
                    Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
                });

        };

        function getSpeeds() {
            ConfigOptionService.getEfficiencySpeeds($scope.currentOptID, $scope.controllerID).then(function (data) {
                $scope.speeds = data;
            });
        }


        $scope.addSpeed = function () {
            ConfigOptionService.addEfficiencySpeed($scope.currentOptID, $scope.controllerID, $scope.speedForm).then(function (data) {
                Notification.success($filter('translate')('success'));
                $scope.resetSpeedForm();
                getSpeeds();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.resetSpeedForm = function () {
            $scope.speedForm = {};
        };

        $scope.resetSpeedForm();

        $scope.deleteSpeed = function (speedID) {
            ConfigOptionService.deleteEfficiencySpeed($scope.currentOptID, $scope.controllerID, speedID).then(function (data) {
                Notification.success($filter('translate')('success'));
                getSpeeds();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.resetSpeedChangeForm = function () {
            $scope.speedChangeForm = {};
        };
        $scope.resetSpeedChangeForm();

        function getSpeedChanges() {
            ConfigOptionService.getEfficiencySpeedChanges($scope.currentOptID, $scope.controllerID).then(function (data) {
                $scope.speedChanges = data;
            });
        }

        $scope.addSpeedChange = function () {
            ConfigOptionService.addEfficiencySpeedChange($scope.currentOptID, $scope.controllerID, $scope.speedChangeForm).then(function (data) {
                Notification.success($filter('translate')('success'));
                $scope.resetSpeedChangeForm();
                getSpeedChanges();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.deleteSpeedChange = function (speedChange) {
            ConfigOptionService.deleteEfficiencySpeedChange($scope.currentOptID, $scope.controllerID, speedChange.ID).then(function (data) {
                Notification.success($filter('translate')('success'));
                getSpeedChanges();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.resetSideRelationForm = function () {
            $scope.sideRelationForm = {};
        };
        $scope.resetSideRelationForm();

        function getSideRelations(){
            ConfigOptionService.getEfficiencySideRelations($scope.currentOptID, $scope.controllerID).then(function (data) {
                $scope.speedChangesRelations = data;
            });
        }

        $scope.addSideRelation=function(){
            ConfigOptionService.addEfficiencySideRelation($scope.currentOptID, $scope.controllerID, $scope.sideRelationForm).then(function (data) {
                Notification.success($filter('translate')('success'));
                $scope.resetSideRelationForm();
                getSideRelations();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        }

        $scope.deleteSideRelation = function (sideRelation) {
            ConfigOptionService.deleteEfficiencySideRelation($scope.currentOptID, $scope.controllerID, sideRelation.ID).then(function (data) {
                Notification.success($filter('translate')('success'));
                getSideRelations();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };
    });
