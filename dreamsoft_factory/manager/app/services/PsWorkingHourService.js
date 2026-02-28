'use strict';

angular.module('digitalprint.services')
    .factory('PsWorkingHourService', function ($q, $http, $config) {

        var PsWorkingHourService = {};

        var resource = 'ps_realizationTimeWorkingHours';

        PsWorkingHourService.getAll = function () {
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

        PsWorkingHourService.update = function (data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return PsWorkingHourService;

    });