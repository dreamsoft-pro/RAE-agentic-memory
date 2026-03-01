angular.module('digitalprint.app')
    .controller('orders.ProductionSettingsCtrl', function($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, DepartmentService, $timeout,
        $window, $q, $stateParams) {

            $scope.zoomOptions = [
                {ID: 1, name: "minute"},
                {ID: 2, name: "hour"},
                {ID: 3, name: "day"},
                {ID: 4, name: "week"},
                {ID: 5, name: "month"},
                {ID: 6, name: "quarter"}
            ];

            function getSettings(){
                OngoingService.getSettings().then(function (data) {
                    var timeStart = {};
                    timeStart.hour = data.raportTimeDayStart.split(":")[0];
                    timeStart.minutes = data.raportTimeDayStart.split(":")[1];
                    var timeEnd = {};
                    timeEnd.hour = data.raportTimeDayEnd.split(":")[0];
                    timeEnd.minutes = data.raportTimeDayEnd.split(":")[1];

                    console.log(timeStart);
                    console.log(timeEnd);

                    var time = new Date();
                    var timeRaportStart = new Date(time.getFullYear(), time.getMonth(), time.getDate(), timeStart.hour, timeStart.minutes, 0, 0);
                    data.raportTimeDayStart = timeRaportStart;
                    var timeRaportEnd = new Date(time.getFullYear(), time.getMonth(), time.getDate(), timeEnd.hour, timeEnd.minutes, 0, 0);
                    data.raportTimeDayEnd = timeRaportEnd;
                    $scope.form = data;
                    console.log(data);
                });
            }

            getSettings();

            $scope.saveSettings=function(){
                console.log($scope.form);
                var saveData = {};
                saveData.raportTimeDayStart = $scope.form.raportTimeDayStart.getHours()+":"+$scope.form.raportTimeDayStart.getMinutes();
                saveData.raportTimeDayEnd = $scope.form.raportTimeDayEnd.getHours()+":"+$scope.form.raportTimeDayEnd.getMinutes();
                saveData.defaultGanttScale = $scope.form.defaultGanttScale;
                OngoingService.saveSettings(saveData).then(function(data){
                    console.log(data);
                    if (data.response == "true") {
                        Notification.success($filter('translate')('success'));
                        getSettings();
                    } else {
                        Notification.error(data.error);
                    }
                });
            }
        
       
    });