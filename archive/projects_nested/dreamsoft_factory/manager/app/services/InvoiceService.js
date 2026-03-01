/**
 * Created by Rafał on 13-07-2017.
 */
'use strict';

angular.module('digitalprint.services')
    .factory('InvoiceService', function ($q, $http, $config) {

        var InvoiceService = {};

        var resource = getResource();

        function getResource() {
            return 'dp_invoices';
        }

        InvoiceService.get = function (orderID) {
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

        InvoiceService.changeInvoiceType = function (orderID, type) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'changeInvoiceType'].join("/"),
                data: {
                    orderID: orderID,
                    type: type
                }
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return InvoiceService;
    });