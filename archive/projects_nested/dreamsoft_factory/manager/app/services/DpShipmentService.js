/**
 * Created by Rafał on 26-07-2017.
 */
angular.module('digitalprint.services')
    .service('DpShipmentService', function ($rootScope, $q, $http, $config) {

        var DpShipmentService = {};

        var resource = 'dp_shipment';

        DpShipmentService.getForOrder = function (orderID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, orderID].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpShipmentService.generateLabels = function (packages, orderID) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'generateLabels'].join("/"),
                data: {
                    packages: packages,
                    orderID: orderID
                }
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpShipmentService.printLabel = function (shipmentID, orderAddressID) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'printLabel'].join("/"),
                data: {
                    shipmentID: shipmentID,
                    orderAddressID: orderAddressID
                }
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpShipmentService.deleteLabel = function (orderAddressID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, 'labels', orderAddressID].join("/"),
                data: {
                    orderAddressID: orderAddressID
                }
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return DpShipmentService;
    });