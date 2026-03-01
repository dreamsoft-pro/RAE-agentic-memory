/**
 * Created by Rafał on 26-07-2017.
 */
'use strict';

angular.module('digitalprint.app')
    .controller('orders.TransportCtrl', function ($scope, DpShipmentService, Notification, $window) {

        $scope.orderAddresses = [];
        $scope.labels = [];

        function init() {

        }

        init();

        $scope.search = function() {
            var orderID = this.form.orderID;

            $scope.labels = [];

            DpShipmentService.getForOrder(orderID).then(function(data) {
                $scope.orderAddresses = data;
            });
        };

        function reload(orderID) {
            DpShipmentService.getForOrder(orderID).then(function(data) {
                $scope.orderAddresses = data;
            });
        }

        $scope.generateLabel = function(orderAddress) {

            var packages = [{
                ID: orderAddress.ID,
                width: orderAddress.input.width,
                height: orderAddress.input.height,
                length: orderAddress.input.length,
                weight: orderAddress.input.weight,
                joinedWeight: orderAddress.joinedWeight
            }];

            DpShipmentService.generateLabels(packages, orderAddress.orderID).then( function(data) {
                if( data.results ) {
                    reload( orderAddress.orderID);
                }
                if( data.errors && data.errors.length > 0 ) {
                    _.each(data.errors, function (error) {
                        Notification.warning(error);
                    });
                }
            });
        };

        $scope.generateAllLabels = function(orderAddresses) {

            var first = _.first(orderAddresses);
            var packages = [];
            _.each(orderAddresses, function(orderAddress) {
                if( orderAddress.input !== undefined) {
                    packages.push({
                        ID: orderAddress.ID,
                        width: orderAddress.input.width,
                        height: orderAddress.input.height,
                        length: orderAddress.input.length,
                        joinedWeight: orderAddress.joinedWeight
                    });
                }
            });
            var orderID = first.orderID;

            DpShipmentService.generateLabels(packages, orderID).then( function(data) {
                if( data.results && data.results.length > 0 ) {
                    reload(orderID);
                }
                if( data.errors && data.errors.length > 0 ) {
                    _.each(data.errors, function (error) {
                        Notification.warning(error);
                    });
                }
            });
        };

        $scope.printLabel = function(orderAddress) {
            DpShipmentService.printLabel(orderAddress.shipmentID, orderAddress.ID).then( function(data) {
                if (data.response === true) {
                    if( data.provider === 'dhl' ) {
                        $window.open(data.file, '_blank');
                    } else if( data.provider === 'ups' ) {
                        $scope.labels = data.labels;
                    } else if ( data.provider === 'dpd-russia' ) {
                        orderAddress.labels = data.results.labels;
                        orderAddress.shipmentID = data.results.shipmentID;
                    }
                }
            });
        };

        $scope.printLabel = function(orderAddress) {
            DpShipmentService.deleteLabel(orderAddress).then(function(responseData) {
                console.log(responseData);
            });
        };

        $scope.removeAddressLabel = function(orderAddress) {
            console.log('orderAddress: ', orderAddress);
            DpShipmentService.deleteLabel(orderAddress.ID).then(function(responseData) {
                console.log(responseData);
            });
        };

    });