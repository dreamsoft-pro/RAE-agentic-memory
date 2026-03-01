'use strict';

angular.module('digitalprint.services')
    .factory('ModelIconsService', function ($q, $http, $config, Restangular) {
        var ModelIconsService = {};

        function getResource() {
            return 'dp_ModelIconsExtensions';
        }

        var resource = getResource();

        ModelIconsService.getAll = function () {
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

        return ModelIconsService;
    });