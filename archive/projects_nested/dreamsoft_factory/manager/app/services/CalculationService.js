angular.module('digitalprint.services')
    .factory('CalculationService', function ($q, $http, $config, $cacheFactory) {

        var CalculationService = {};

        var resource = 'calculations';

        CalculationService.getAll = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        CalculationService.get = function (id) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, id].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        CalculationService.getAllSeller = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'seller'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        CalculationService.history = function (baseID) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'history', baseID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        CalculationService.historyMultiOffer = function (productID) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'historyMultiOffer', productID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        }

        CalculationService.deliveriesHistory = function (orderID) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'deliveriesHistory', orderID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return CalculationService;

    });
