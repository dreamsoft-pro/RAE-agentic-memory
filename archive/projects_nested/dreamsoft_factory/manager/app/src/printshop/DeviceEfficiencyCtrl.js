angular.module('digitalprint.app')
    .controller('printshop.DeviceEfficiencyCtrl', function ($scope, $filter, $modal, DeviceService, Notification, $stateParams) {
        $scope.deviceID = $stateParams.deviceID;

        $scope.deviceService = DeviceService;

        DeviceService.get($scope.deviceID).then(function (data) {
            $scope.deviceName = data.name;
            $scope.form = data;
        });

        DeviceService.getWorkUnits().then(function (data) {
            $scope.workUnits=data.response;
        });

        $scope.save = function () {
            DeviceService.updateEfficiency($scope.form).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error(data.error);
                }
            });
        };

        function getSpeeds() {
            DeviceService.getSpeeds($scope.deviceID).then(function (data) {
                $scope.speeds = data;
            });
        }

        getSpeeds();

        $scope.addSpeed = function () {
            DeviceService.addSpeed($scope.deviceID, $scope.speedForm).then(function (data) {
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
            DeviceService.deleteSpeed($scope.deviceID, speedID).then(function (data) {
                Notification.success($filter('translate')('success'));
                getSpeeds();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

    });
