/**
 * Created by Rafał on 01-06-2017.
 */
angular.module('digitalprint.services')
    .service('ConfigService', function ($rootScope, $q, $config, $http) {


        var ConfigService = {};

        ConfigService.resetDomain = function (force) {
            var resource = 'resetDomain';

            var def = $q.defer();

            $http({
                url: $config.API_URL + resource,
                method: 'PATCH'
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ConfigService.createCompany = function (form) {
            var resource = 'createCompany';

            var def = $q.defer();

            $http({
                url: $config.API_URL + resource,
                method: 'PATCH',
                data: form
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ConfigService.generateSiteMap = function() {
            var resource = 'settings/generateSiteMap';

            var def = $q.defer();

            $http({
                url: $config.API_URL + resource,
                method: 'GET'
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return ConfigService;
    });