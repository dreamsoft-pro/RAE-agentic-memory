javascript
'use strict';

angular.module('digitalprint.services')
    .factory('PsWorkingHourService', function ($q, $http, $config) {

        var PsWorkingHourService = {};

        var resource = 'ps_realizationTimeWorkingHours';

        PsWorkingHourService.getAll = function () {
            return $http.get($config.API_URL + resource)
                .then(function (response) {
                    return response.data;
                }, function (error) {
                    return $q.reject(error);
                });
        };

        PsWorkingHourService.update = function (data) {
            var def = $q.defer();
