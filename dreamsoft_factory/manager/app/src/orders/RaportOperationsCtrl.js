angular.module('digitalprint.app')
    .controller('orders.RaportOperationsCtrl', function($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, DepartmentService, $timeout,
        $window, $q, $stateParams, DpOrderService) {

        $scope.tasks = [];
        $scope.dateStart = new Date();
        $scope.dateEnd = new Date();

        var updateTableTimeout;
        $scope.showRows = 25;

        $scope.operationsConfig = {
            count: 'ongoings/getOperationsLogsCount',
            params: {
                //dateStart: $scope.dateEnd,
                //dateEnd: $scope.dateEnd,
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.tasks = data;
            }
        };

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.dpOperationsApi.get({cache: false});
            }, 1000);
        };


        function init() {
            var today = new Date();
            today.setDate(today.getDate() - 1);
            var today2 = new Date();
            today2.setDate(today2.getDate() - 1);
            today2.setHours(0);
            today2.setMinutes(0);
            today2.setSeconds(0);
            today.setHours(23);
            today.setMinutes(59);
            today.setSeconds(59);
            $scope.dateStart = today2;
            $scope.dateEnd = today;  
            

            $scope.dpOperationsApi = new ApiCollection('ongoings/getOperationsLogs', $scope.operationsConfig);
            $scope.dpOperationsApi.setParam('dateStart', Math.round((today2.getTime())/1000));
            $scope.dpOperationsApi.setParam('dateEnd', Math.round((today.getTime())/1000));
            $scope.dpOperationsApi.clearCache();

            

            //getRaport();
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
            var date1 = new Date();
            var date2 = new Date();
            date1.setTime($scope.dateStart.getTime());
            date1.setDate(date1.getDate());
            date2.setTime($scope.dateEnd.getTime());
            date2.setDate(date2.getDate());

            date1.setHours(0);
            date1.setMinutes(0);
            date1.setSeconds(0);
            date2.setHours(23);
            date2.setMinutes(59);
            date2.setSeconds(59);

            $scope.dpOperationsApi.params.dateStart = Math.round((date1.getTime())/1000);
            $scope.dpOperationsApi.params.dateEnd = Math.round((date2.getTime())/1000);

            $scope.setParams();
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

    });