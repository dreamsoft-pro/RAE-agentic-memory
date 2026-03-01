'use strict';

angular.module('digitalprint.services')
    .factory('ProductCardService', function ($q, $http, $config) {

        var ProductCardService = {};

        var resource = getResource();

        function getResource() {
            return 'productCard';
        }

        ProductCardService.get = function (productID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, productID].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ProductCardService.getXml = function (productID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'generateXML',productID].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return ProductCardService;
    });
