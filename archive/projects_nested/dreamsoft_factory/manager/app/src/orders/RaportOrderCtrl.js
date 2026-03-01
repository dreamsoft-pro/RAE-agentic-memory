angular.module('digitalprint.app')
    .controller('orders.RaportOrderCtrl', function($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, DepartmentService, $timeout,
        $window, $q, $stateParams, DpOrderService) {

        $scope.orderID = $stateParams.orderID;
        $scope.dateStart = "";
        $scope.dateEnd = "";
        $scope.order = {};
        $scope.ongoingsByDate = [];
        $scope.filterOngoingsByDate = [];
        $scope.periodStats = {};

        function init() {
            var today = new Date();
            today.setDate(today.getDate() - 1);
            $scope.dateEnd = Math.round((today.getTime())/1000);
            var today7DaysBack = new Date();
            today7DaysBack.setDate(today7DaysBack.getDate() - 8);
            $scope.dateStart = Math.round((today7DaysBack.getTime())/1000);

            DpOrderService.get($scope.orderID).then(function (data) {
                $scope.order = data;
            });
            

            getRaport();
        }
        
        $scope.formatTime = function (timeInSeconds) {
            var seconds = pad(timeInSeconds % 60);
            var minutes = pad(Math.floor(timeInSeconds / 60) % 60);
            var hours = pad(Math.floor(timeInSeconds / 3600));

            return hours + ':' + minutes + ':' + seconds
        };

        function pad(n) {
            return (n < 10) ? ("0" + n) : n;
        }

        init();

        $scope.dateChange = function () {
            $timeout(function () {
                getRaport();
            }, 1000);
        };

        function getRaport(){
            var dates = {};
            var countDays = 0;
            var countBreaks = 0;
            var countWork = 0;
            dates.dateStart = $scope.dateStart;
            dates.dateEnd = $scope.dateEnd;
            OngoingService.getOrderLogs($scope.orderID, dates).then(function (data) {
                var ongoingsByDate = [];
                for(var date in data){
                    ongoingsByDate.push(data[date]);
                }
                
                if(ongoingsByDate.length > 0){
                    $scope.ongoingsByDate = ongoingsByDate;
                }else{
                    Notification.error($filter('translate')('error') + ': ' + $filter('translate')('no_jobs_found'));
                    $scope.ongoingsByDate = [];
                }
                _.each($scope.ongoingsByDate, function (singleDay) {
                    countDays++;
                    _.each(singleDay.data, function (singleOngoing) {
                        if(singleOngoing.isBrake == true){
                            countBreaks += parseInt(singleOngoing.timeOfBreak);
                        }else if(singleOngoing.isBrake == false){
                            if(singleOngoing.timeOfWork != 'none'){
                                countWork += parseInt(singleOngoing.timeOfWork);   
                            }
                        }
                    });
                });
                $scope.periodStats.days = countDays;
                $scope.periodStats.breaks = countBreaks;
                $scope.periodStats.work = countWork;
                $scope.periodStats.totalTime = countBreaks + countWork;
                $scope.filterOngoingsByDate = _.clone($scope.ongoingsByDate);
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

    });