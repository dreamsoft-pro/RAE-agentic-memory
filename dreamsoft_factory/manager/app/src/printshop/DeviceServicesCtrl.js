angular.module('digitalprint.app')
    .controller('printshop.DeviceServicesCtrl', function ($scope, $filter, $modal, DeviceService, Notification,
                                                          $stateParams) {
        $scope.deviceID = $stateParams.deviceID;

        /*$scope.cycles = [{ID: 1, name: "Raz dziennie"},
            {ID: 2, name: "Raz tygodniowo"},
            {ID: 3, name: "Raz w miesiącu"},
            {ID: 4, name: "Raz na rok"}
        ];*/

        $scope.dayOfMonthActive = false;
        $scope.monthActive = false;
        $scope.dayOfWeekActive = false;

        $scope.cycles = [{ID: 1, name: "device_services_once_a_day"},
            {ID: 2, name: "device_services_weekly"},
            {ID: 3, name: "device_services_monthly"},
            {ID: 4, name: "device_services_yearly"}
        ];

        $scope.changeCycle = function (cycleID) {
            if(cycleID == 2){
                $scope.dayOfMonthActive = false;
                $scope.monthActive = false;
                $scope.dayOfWeekActive = true;
            }else if(cycleID == 3){
                $scope.dayOfMonthActive = true;
                $scope.monthActive = false;
                $scope.dayOfWeekActive = false;
            }else if(cycleID == 4){
                $scope.dayOfMonthActive = true;
                $scope.monthActive = true;
                $scope.dayOfWeekActive = false;
            }else{
                $scope.dayOfMonthActive = false;
                $scope.monthActive = false;
                $scope.dayOfWeekActive = false;
            }
        };

        $scope.resetServiceForm = function () {
            $scope.form = {};
        };
        $scope.resetServiceForm();

        DeviceService.get($scope.deviceID).then(function (data) {
            $scope.deviceName = data.name;
        });

        function getDeviceServices() {
            DeviceService.getServices($scope.deviceID).then(function (data) {
                _.each(data,function(item){
                    item.cycleName=_.findWhere($scope.cycles,{ID:item.cycleID}).name;
                });
                $scope.services = data;
            });
        }
        getDeviceServices();

        $scope.saveService = function () {
            DeviceService.addService($scope.deviceID,$scope.form).then(function (data) {
                    Notification.success($filter('translate')('success'));
                    getDeviceServices();
                    $scope.form = {};
            }, function(data){
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.deleteDeviceService = function (service) {
            DeviceService.deleteService($scope.deviceID, service.ID).then(function (data) {
                Notification.success($filter('translate')('success'));
                getDeviceServices();
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };
    });
