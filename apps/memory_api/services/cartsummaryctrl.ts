javascript
'use strict';

angular.module('dpClient.app')
    .controller('CartSummaryCtrl', function($scope, $modal) {

        $scope.deliveryMethod = function(cart) {
            $modal.open({
                templateUrl: '@/lib/api/cart/templates/modalboxes/delivery-method.html',
                controller: 'DeliveryMethodController'
            }).result.then(function(selectedMethod) {
                // Handle selected delivery method
            });
        };
    });

angular.module('dpClient.app')
    .controller('DeliveryMethodController', function($scope, $modalInstance, cart) {

        $scope.cart = cart;

        $scope.selectMethod = function(method) {
            $modalInstance.close(method);
        };

        $scope.cancel = function() {
            $modalInstance.dismiss('cancel');
        };
    });
