angular.module('digitalprint.app')
    .controller('orders.ScheduleCtrl', function($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, ScheduleService, $timeout,
        $window, $q) {

        $scope.sortChange = false;

        $scope.sortableOptions = {
            stop: function(e, ui) {
                $scope.sortChange = true;
            },
            axis: 'y',
            placeholder: 'success',
            handle: 'button.button-sort',
            cancel: ''
        };

        $scope.showRows = 25;
        $scope.productsConfig = {
            count: 'schedule/count',
            params: {
                accept: 1,
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.dpProducts.items = data;
                console.log(data);
            }
        };

        $scope.dpProducts = new ApiCollection('schedule', $scope.productsConfig);
        $scope.dpProducts.get();

        var updateTableTimeout;
        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.dpProducts.get();
            }, 1000);
        };

        function init() {
            $scope.dpProducts.clearCache();
        }

        init();

        $scope.sortCancel = function () {
            $scope.refresh();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.dpProducts.items, function (item) {
                result.push(item.ID);
            });

            var ongoingsOrder = [];
            _.each($scope.dpProducts.items, function (item) {
                _.each(item.products, function (product) {
                    _.each(product.ongoings.list, function (ongoing) {
                        ongoingsOrder.push(ongoing.ID);
                    });
                });
            });

            ScheduleService.sort(result).then(function (data) {
                $scope.sortChange = false;
                OngoingService.sort(ongoingsOrder).then(function (dataOngoingSort) {
                    Notification.success($filter('translate')('success'));
                    $scope.dpProducts.clearCache();
                }, function (dataOngoingSort) {
                    Notification.error($filter('translate')('error'));
                    $scope.sortCancel();
                });
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };

    });