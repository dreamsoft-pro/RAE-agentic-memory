angular.module('digitalprint.app')
    .controller('printshop.DeviceSpeedCtrl', function ($scope, $filter, $modal, DeviceService, Notification,
                                                       DepartmentService, $stateParams) {
        $scope.deviceID = $stateParams.deviceID;

        DeviceService.get($scope.deviceID).then(function (data) {
            $scope.deviceName = data.name;
        });

        $scope.resetSpeedChangeForm = function () {
            $scope.speedChangeForm = {};
        };
        $scope.resetSpeedChangeForm();
        $scope.resetSideRelationForm = function () {
            $scope.sideRelationForm = {};
        };
        $scope.resetSideRelationForm();

        function getSpeedChanges(){
            DeviceService.getSpeedChanges($scope.deviceID).then(function (data) {
                $scope.speedChanges = data;
            });
        }
        getSpeedChanges();

        $scope.addSpeedChange=function(){
            DeviceService.saveSpeedChange($scope.deviceID, $scope.speedChangeForm).then(function(data){
                Notification.success($filter('translate')('success'));
                $scope.resetSpeedChangeForm();
                getSpeedChanges()
            }, function(data){
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.deleteSpeedChange=function(speedChange){
            DeviceService.deleteSpeedChange($scope.deviceID, speedChange.ID).then(function (data) {
                Notification.success($filter('translate')('success'));
                getSpeedChanges();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        function getSideRelations(){
            DeviceService.getSideRelations($scope.deviceID).then(function (data) {
                $scope.speedChangesRelations = data;
            });
        }
        getSideRelations();

        $scope.addSideRelation=function(){
            DeviceService.addSideRelation($scope.deviceID, $scope.sideRelationForm).then(function(data){
                Notification.success($filter('translate')('success'));
                $scope.resetSideRelationForm();
                getSideRelations();
            }, function(data){
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.deleteSideRelation=function(relation){
            DeviceService.deleteSideRelation($scope.deviceID, relation.ID).then(function (data) {
                Notification.success($filter('translate')('success'));
                getSideRelations();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        }
    });
