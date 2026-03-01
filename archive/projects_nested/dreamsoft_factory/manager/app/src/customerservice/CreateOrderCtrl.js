angular.module('digitalprint.app')
    .controller('customerservice.CreateOrderCtrl', function ( $filter, $timeout, $modal, $scope, $state, $stateParams,
                                                             DpOrderService, ApiCollection, Notification, UserService,
                                                              CurrencyService, OrderDataService, typeOfResource ) {

        $scope.order = {};
        $scope.sellerForm = {};
        $scope.userLimit = 10;
        $scope.currencies = [];

        var userID = $stateParams.userID;

        $scope.typeOfResource = typeOfResource;

        function init() {

            DpOrderService.sellerNotReady(typeOfResource.type).then(function (data) {
                $scope.orders = data;
            }, function (data) {
                Notification.error($filter('translate')('data_retrieve_failed'));
            });

            CurrencyService.getAll().then( function(currencies) {
                if( currencies ) {
                    _.each(currencies, function(currency) {
                        if(currency.default === 1) {
                            $scope.order.currency = currency.code;
                        }
                    })
                }
                $scope.currencies = currencies;
            });
        }

        var usersConfig = {
            params: {
                limit: $scope.userLimit
            },
            onSuccess: function (data) {
                $scope.usersCollection.items = data;
            }
        };

        $scope.usersCollection = new ApiCollection('users/searchAll', $scope.usersConfig);

        $scope.addProduct = function () {

            var userID = null;

            if( this.order.user !== undefined && this.order.user !== null ) {
                userID = this.order.user.ID;
            } else if( this.order.searchUser !== undefined && this.order.searchUser !== null ) {
                userID = this.order.searchUser.ID;
            }

            var orderID = null;

            if( this.order.ID !== undefined ) {
                orderID = this.order.ID;
            }

            OrderDataService.setNewOrder(this.order.currency);

            if( typeOfResource.type === 'order' ) {

                $state.go('create-order-groups', {
                    'userID': userID,
                    'orderID': orderID
                });

            } else if (typeOfResource.type === 'offer') {

                $state.go('create-offer-groups', {
                    'userID': userID,
                    'orderID': orderID
                });
            }

        };

        var updateTableTimeout;
        $scope.findUser = function (val, type) {
            $scope.usersCollection.params.search = val;
            $scope.usersCollection.params.type = type;
            $timeout.cancel(updateTableTimeout);

            updateTableTimeout = $timeout(function () {
                return $scope.usersCollection.clearCache().then(function (data) {
                    $scope.usersCollection.items = data;
                    return data;
                });
            }, 300);
            return updateTableTimeout;
        };

        $scope.addUser = function (order) {

            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/add-user.html',
                scope: $scope,
                size: 'lg',
                resolve: {
                    countries: function( CountriesService ) {
                        return CountriesService.getAllEnabled().then(function(countriesData) {
                            return countriesData;
                        });
                    },
                    discountGroups: function(DiscountService) {
                        return DiscountService.getAll().then(function (data) {
                            return data.discountGroups;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, countries, discountGroups) {

                    $scope.form = {};
                    $scope.countries = countries;
                    $scope.discountGroups = discountGroups;

                    order.searchUser = {};

                    $scope.save = function() {
                        console.log($scope.form);
                        UserService.add($scope.form).then(function (data) {
                            $scope.form = {};
                            if( data.user ) {
                                UserService.getUser(data.user.ID).then( function(userData) {
                                    order.searchUser = userData;
                                    Notification.success($filter('translate')('user_has_been_added'));
                                    $modalInstance.close();
                                });
                            }
                        }, function (data) {
                            Notification.error(data.info || $filter('translate')('error'));
                        });
                    };

                }
            });

        };

        init();

    });