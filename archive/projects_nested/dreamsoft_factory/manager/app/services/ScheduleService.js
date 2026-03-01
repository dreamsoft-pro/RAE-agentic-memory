angular.module('digitalprint.services')
    .factory('ScheduleService', function ($rootScope, $q, $http, $config, $cacheFactory) {

        var ScheduleService = {};
        var resource = 'schedule';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        ScheduleService.sort = function (sort) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'sort'].join('/'),
                data: sort
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ScheduleService.updateOngoings = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'updateOngoings'].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return ScheduleService;

    });