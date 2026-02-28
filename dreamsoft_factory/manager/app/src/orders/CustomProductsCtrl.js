'use strict';

angular.module('digitalprint.app')
    .controller('orders.CustomProductsCtrl', function ($scope, ApiCollection, $timeout, $modal, $state,
                                                       DpAddressService, Notification, $filter) {

        $scope.showRows = 25;
        $scope.customProductConfig = {
            count: 'dp_customProducts/count',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.customProductsCtrl.items = data;
            }
        };

        $scope.customProductsCtrl = new ApiCollection('dp_customProducts', $scope.customProductConfig);

        if($state.params.customProductID) {
            $scope.customProductsCtrl.setParam('ID', $state.params.customProductID);
        }

        $scope.customProductsCtrl.get();

        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.customProductsCtrl.get();
            }, 1000);
        };

        $scope.files = function (customProduct) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/custom-product-files.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope) {
                    $scope.files = customProduct.files;
                }
            });
        };

        $scope.defaultAddress = function( user ) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/default-address.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance, $config) {

                    $scope.address = {};

                    DpAddressService.getDefaultAddress(user.ID, 1).then( function(data) {
                        $scope.address = data.address;
                    });

                }
            });
        };

        function init() {


        }

        init();

    });