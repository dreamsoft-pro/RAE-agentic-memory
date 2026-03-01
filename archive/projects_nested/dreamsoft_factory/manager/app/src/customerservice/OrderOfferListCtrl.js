angular.module('digitalprint.app')
    .controller('customerservice.OrderOfferListCtrl', function ($scope, $rootScope, UserAddressService, ApiCollection,
                                                                DpOrderService, $state, $filter, $modal,
                                                                UserService, Notification, OrderMessageWidgetService,
                                                                socket, $timeout ) {

        $scope.showRows = 25;
        $scope.offersConfig = {
            count: 'dp_orders/offerListCount',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.ordersCtrl.items = data;
            }
        };

        $scope.ordersCtrl = new ApiCollection('dp_orders/offerList', $scope.offersConfig);
        $scope.ordersCtrl.clearCache();
        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.ordersCtrl.clearCache();
            }, 1000);
        };

        function init() {

        }

        $scope.edit = function (order, product) {
            var params = {
                'orderID': order.ID,
                'groupID': product.groupID,
                'typeID': product.typeID,
                'calcID': product.calcID,
                'productID': product.productID
            };
            $state.go('create-offer-calc', params);
        };

        $scope.goToSendOrder = function (order) {
            var data = {ready: 0};
            DpOrderService.edit(order.ID, data).then(function (data) {
                $state.go('create-order', {orderID: order.ID});
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.history = function (order, product) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/calculation-history.html',
                scope: $scope,
                size: 'lg',
                windowClass: 'modal-wide-screen',
                resolve: {
                    calculations: function (CalculationService) {
                        if(product.isMultiVolumeOffer === 1){
                            return CalculationService.historyMultiOffer(product.productID).then(function (data) {
                                return data;
                            }, function (data) {
                                console.error(data);
                                Notification.error($filter('translate')('data_retrieve_failed'));
                            });
                        }else{
                            return CalculationService.history(product.baseID).then(function (data) {
                                return data;
                            }, function (data) {
                                console.error(data);
                                Notification.error($filter('translate')('data_retrieve_failed'));
                            });
                        }
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

        $scope.createOrder=function(order){
            $state.go('order-make-order', {orderID: order.ID});
        };

        $scope.renewOffer = function (order) {

            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/save-offer.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {

                    $scope.offer = order;

                    $scope.save = function() {

                        var data = {
                            expires: order.expires,
                            sendInfoToUser: 1
                        };

                        if (order.userID && order.userMail) {
                            data.userID = order.userID;
                        }

                        data.expires = order.expires;

                        DpOrderService.saveOffer(order.ID, data).then(function (data) {
                            if( data.response ) {
                                order.offerStatus = 1;
                                Notification.success($filter('translate')('success'));
                                $modalInstance.close();
                            }

                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    }
                }
            });

        };

        $scope.messages = function (offer) {
            OrderMessageWidgetService.messagesModal($scope, offer, socket, {'type': 'offer'});
        };

        init();

    });
