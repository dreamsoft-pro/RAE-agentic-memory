angular.module('digitalprint.app')
    .controller('orders.RaportDevicesCtrl', function($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, DepartmentService, $timeout,
        $window, $q) {

        $scope.devicesLogs = [];
        $scope.dateStart = new Date();
        $scope.dateEnd = new Date();

        function init() {
            var today = new Date();
            today.setDate(today.getDate() - 1);
            $scope.dateEnd = today;
            $scope.dateStart = today;

            getRaport();
        }

        init();

        function getRaport(){
            var date1 = new Date();
            var date2 = new Date();
            date1.setTime($scope.dateStart.getTime());
            date1.setDate(date1.getDate() - 1);
            date2.setTime($scope.dateEnd.getTime());
            date2.setDate(date2.getDate() - 1);

            var dates = {};
            dates.dateStart = Math.round((date1.getTime())/1000);
            dates.dateEnd = Math.round((date2.getTime())/1000);
            OngoingService.getAllDeviceLogs(dates).then(function (data) {
                $scope.devicesLogs = data;
            });
        }

        $scope.search = function () {
            var newFilter = {};
            for(var filter in $scope.filterData){
                if($scope.filterData[filter] != ''){
                    newFilter[filter] = $scope.filterData[filter];
                }
            }
            $scope.filterData = newFilter;
        };

        $scope.changeDate = function(date){
            var dateStart = new Date();
            var dateEnd = new Date();
            var today = new Date();
            if(date == "last_full_week"){
                var day = today.getDay() || 7;
                if( day !== 1 ){
                    dateStart.setHours(-24 * (day - 1));
                    dateEnd.setHours(-24 * (day - 1));
                }
                dateStart.setHours(-24 * 7);
                dateEnd.setHours(-24 * 1);
            }else if(date == "last_full_month"){
                dateStart = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                dateEnd = new Date(today.getFullYear(), today.getMonth(), 0);
            }else if(date == "today"){
                dateStart.setDate(dateStart.getDate());
                dateEnd.setDate(dateEnd.getDate());
            }else  if(date == "yesterday"){
                dateStart.setDate(dateStart.getDate() - 1);
                dateEnd.setDate(dateEnd.getDate() - 1);
            }else  if(date == "last_week"){
                dateStart.setDate(dateStart.getDate() - 7);
                dateEnd.setDate(dateEnd.getDate() );
            }else  if(date == "last_month"){
                dateStart.setDate(dateStart.getDate() - 31);
                dateEnd.setDate(dateEnd.getDate());
            }            
            $scope.dateStart = dateStart;
            $scope.dateEnd = dateEnd;
            getRaport();
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

    });