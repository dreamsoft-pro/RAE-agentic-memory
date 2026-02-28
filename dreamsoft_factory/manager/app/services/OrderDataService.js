'use strict';

angular.module('digitalprint.services')
    .factory('OrderDataService', function( localStorageService ) {

        var orders = [];

        function OrderDataService( json ) {
            angular.extend( this, json );
        }

        function save() {
            localStorageService.set('orders', orders);
        }

        function init() {
            orders = localStorageService.get('orders');
        }

        function setNewOrder( currency ) {

            orders.push({
                'currency': currency
            });
            save();

        }

        function getLastOrder() {
            if( !orders ) {
                return {};
            }
            return orders[orders.length-1];
        }


        return {
            init: init,
            setNewOrder: setNewOrder,
            getLastOrder: getLastOrder
        };
});