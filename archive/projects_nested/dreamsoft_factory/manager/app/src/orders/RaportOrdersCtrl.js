angular.module('digitalprint.app')
    .controller('orders.RaportOrdersCtrl', function($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, DepartmentService, $timeout,
        $window, $q, DpOrderService) {

            var updateTableTimeout;

            $scope.dateStart = "";
            $scope.dateEnd = "";

            $scope.showRows = 25;
            $scope.ordersConfig = {
                count: 'dp_orders/count',
                params: {
                    production: 1,
                    isOrder: 1,
                    ready: 1,
                    limit: $scope.showRows
                },
                onSuccess: function (data) {
                    _.each(data, function (order) {
                        var maxRealisationDate = 0;
                        var maxRealisationDateString = "";
                        var totalOperations = 0;
                        var finishedOperations = 0;
                        var estimatedTime = 0;
                        var realTime = 0;
                        _.each(order.products, function (product) {
                            var time = Date.parse(product.realisationDate);
                            if(time > maxRealisationDate){
                                maxRealisationDate = time;
                                maxRealisationDateString = product.realisationDate;
                            }

                            _.each(product.calcProducts, function (calcProduct) {
                                OngoingService.getOngoingsForCalcProduct(calcProduct.ID).then(function (dataOngoings) {
                                   _.each(dataOngoings, function (ongoing) {
                                        totalOperations++;
                                        estimatedTime += ongoing.estimatedTime;
                                        realTime += ongoing.realTime;
                                        if(ongoing.finished == 1){
                                            finishedOperations++;
                                        }
                                    });

                                    order.timeCalc = {};
                                    order.timeCalc.estimatedTime = estimatedTime;
                                    order.timeCalc.realTime = realTime;

                                    order.operations = {};
                                    order.operations.total = totalOperations;
                                    order.operations.finished = finishedOperations;
                                }, function (dataOngoings) {
                                    Notification.error($filter('translate')('error'));
                                });
                            });

                        });
                        var now = Date.now();
                        if(now > maxRealisationDate){
                            order.isLateRealisationDate = true;
                        }else{
                            order.isLateRealisationDate = false;
                        }    
                        order.realisationDate =   maxRealisationDateString;                
                    });

                    $scope.orders = data;
                }
            };

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.dpOrdersCtrl.get({cache: false});
            }, 1000);
        };

        function init() {
            $scope.dpOrdersCtrl = new ApiCollection('dp_orders', $scope.ordersConfig);

            $scope.dpOrdersCtrl.setParam('production', 1);
            $scope.dpOrdersCtrl.setParam('isOrder', 1);
            $scope.dpOrdersCtrl.setParam('ready', 1);
            $scope.dpOrdersCtrl.setParam('dateFrom', dateStart);
            $scope.dpOrdersCtrl.setParam('dateTo', dateEnd);

            $scope.dpOrdersCtrl.clearCache();

            var dateStart = new Date();
            var dateEnd = new Date();
            dateStart.setDate(dateStart.getDate() - 1);
            dateEnd.setDate(dateEnd.getDate() - 1);
            dateStart.setHours(0);
            dateStart.setMinutes(0);
            dateStart.setSeconds(0);
            dateEnd.setHours(23);
            dateEnd.setMinutes(59);
            dateEnd.setSeconds(59);

            $scope.dpOrdersCtrl.params.dateFrom = dateStart;
            $scope.dpOrdersCtrl.params.dateTo = dateEnd;
            $scope.setParams();
        }

        init();

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
                dateEnd.setDate(dateEnd.getDate());
            }else  if(date == "last_month"){
                dateStart.setDate(dateStart.getDate() - 31);
                dateEnd.setDate(dateEnd.getDate());
            }    
            dateStart.setHours(0);
            dateStart.setMinutes(0);
            dateStart.setSeconds(0);
            dateEnd.setHours(23);
            dateEnd.setMinutes(59);
            dateEnd.setSeconds(59);

            $scope.dpOrdersCtrl.params.dateFrom = dateStart;
            $scope.dpOrdersCtrl.params.dateTo = dateEnd;

            $scope.setParams();
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