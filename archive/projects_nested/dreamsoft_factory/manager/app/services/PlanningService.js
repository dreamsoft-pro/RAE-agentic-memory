angular.module('digitalprint.services')
    .factory('PlanningService', function ($rootScope, $q, $http, $config, $cacheFactory) {

        var PlanningService = {};
        var resource = 'schedule';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        PlanningService.getData = function (sort) {
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

        return PlanningService;

    });