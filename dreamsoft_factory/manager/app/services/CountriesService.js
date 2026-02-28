/**
 * Created by Rafał on 20-07-2017.
 */
angular.module('digitalprint.services')
    .factory('CountriesService', function ($rootScope, $q, $config, $http) {

        var CountriesService = {};

        CountriesService.getResource = function () {
            return ['dp_countries'].join('/')
        };

        CountriesService.getAll = function () {
            var def = $q.defer();
            var resource = this.getResource();
            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getAll'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        CountriesService.updateDisabled = function (data) {
            var def = $q.defer();
            var resource = this.getResource();
            $http({
                method: 'PATCH',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        CountriesService.getAllEnabled = function () {
            var def = $q.defer();
            var resource = this.getResource();
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

        return CountriesService;

    });