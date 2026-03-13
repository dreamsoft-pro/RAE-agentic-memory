angular.module('digitalprint.app')
    .controller('customerservice.UnfinishedOrderCtrl', function ($filter, $timeout, $modal, $scope, $state,
                                                                 $stateParams, DpOrderService, ApiCollection,
                                                                 Notification, UserService, typeOfResource) {

        $scope.order = {};
        $scope.sellerForm = {};
        $scope.userLimit = 10;

        $scope.typeOfResource = typeOfResource;

        var userID = $stateParams.userID;

        function init() {

            DpOrderService.sellerNotReady(typeOfResource.type).then(function (data) {
                $scope.orders = data;
            }, function (data) {
                Notification.error($filter('translate')('data_retrieve_failed'));
            });

        }

        $scope.addProduct = function () {

            var userID = null;

            if (this.order.user !== undefined && this.order.user !== null) {
                userID = this.order.user.ID;
            } else if (this.order.searchUser !== undefined && this.order.searchUser !== null) {
                userID = this.order.searchUser.ID;
            }

            var orderID = null;

            if (this.order.ID !== undefined) {
                orderID = this.order.ID;
            }

            if( typeOfResource.type === 'order' ) {
                $state.go('create-order-groups', {
                    'userID': userID,
                    'orderID': orderID
                });
            } else if ( typeOfResource.type === 'offer' ) {
                $state.go('create-offer-groups', {
                    'userID': userID,
                    'orderID': orderID
                });
            }


        };

        $scope.edit = function (order, product) {
            var params = {
                'orderID': order.ID,
                'groupID': product.groupID,
                'typeID': product.typeID,
                'calcID': product.calcID,
                'productID': product.productID
            };

            if( typeOfResource.type === 'order' ) {
                $state.go('create-order-calc', params);
            } else if (typeOfResource.type === 'offer') {
                $state.go('create-offer-calc', params);
            }
        };

        $scope.history = function (order, product) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/calculation-history.html',
                scope: $scope,
                size: 'lg',
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
                    $scope.edit = function (calculation) {
                        var data = _.extend(product, {
                            calcID: calculation.ID
                        });
                        $scope.$parent.edit(order, data);
                        $modalInstance.close();
                    }
                }
            });
        };

        $scope.saveOffer = function(order) {

            var data = {
                expires: order.expires,
                sendInfoToUser: 1
            };

            if(order.user.super === 1) {
                Notification.error('Super user can\'t have offers!');
            }

            if (order.user && order.user.user) {
                data.userID = order.user.ID;
            }

            data.expires = order.expires;

            if( order.orderMessage ) {
                data.orderMessage = order.orderMessage;
            }

            DpOrderService.saveOffer(order.ID, data).then(function (data) {
                var idx = _.findIndex($scope.orders, {
                    ID: order.ID
                });
                if (idx > -1) {
                    $scope.orders.splice(idx, 1);
                }
                Notification.success($filter('translate')('success'));

            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.makeOrder = function (order) {
            var data = {};

            if (order.user && order.user.user) {
                data.userID = order.user.ID;
            }
            if (angular.isDefined(order.orderMessage)) {
                data.orderMessage = order.orderMessage;
            }
            DpOrderService.saveOffer(order.ID, data).then(function (data) {
                var idx = _.findIndex($scope.orders, {
                    ID: order.ID
                });
                if (idx > -1) {
                    $scope.orders.splice(idx, 1);
                }
                $state.go('order-make-order', {orderID: order.ID});
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        init();

    });