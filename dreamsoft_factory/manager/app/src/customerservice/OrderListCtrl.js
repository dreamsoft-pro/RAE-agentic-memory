angular.module('digitalprint.app')
    .controller('customerservice.OrderListCtrl', function ($scope, ApiCollection, CalculationService, DpOrderService,
                                                           $state, $filter, $modal, UserService, Notification,
                                                           $timeout) {

        $scope.showRows = 25;
        $scope.usersConfig = {
            count: 'dp_orders/orderListCount',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.ordersCtrl.items = data;
            }
        };

        $scope.ordersCtrl = new ApiCollection('dp_orders/orderList', $scope.usersConfig);
        $scope.ordersCtrl.clearCache();

        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.ordersCtrl.clearCache();
            }, 1000);
        };

        $scope.getProductInfo = function (order, productItem) {
            var id = productItem.productID;
            return  _.findWhere(order.products, {ID: id});
        };

        $scope.history = function (order, product) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/calculation-history.html',
                scope: $scope,
                size: 'lg',
                windowClass: 'modal-wide-screen',
                resolve: {
                    calculations: function (CalculationService) {
                        return CalculationService.history(product.baseID).then(function (data) {
                            return data;
                        }, function (data) {
                            console.error(data);
                            Notification.error($filter('translate')('data_retrieve_failed'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, calculations) {
                    $scope.calculations = calculations;
                    $scope.order = order;
                    $scope.edit = function (calculation) {
                        var data = _.extend(product, {calcID: calculation.ID});
                        $scope.$parent.edit(order, data);
                        $modalInstance.close();
                    }
                }
            });
        };

        $scope.edit = function (order, product) {
            var params = {
                'orderID': order.ID,
                'groupID': product.groupID,
                'typeID': product.typeID,
                'calcID': product.calcID,
                'productID': product.productID
            };
            $state.go('create-order-calc', params);
        };


    });
