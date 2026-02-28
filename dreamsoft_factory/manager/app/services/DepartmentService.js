angular.module('digitalprint.services')
    .factory('DepartmentService', function ($rootScope, $q, $http, $config, $cacheFactory) {

        var DepartmentService = {};
        var resource = 'departments';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        DepartmentService.getAll = function (force) {
            if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
                getAllDef = $q.defer();
            } else {
                return getAllDef.promise;
            }

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function (data) {
                cache.put('collection', data);
                getAllDef.resolve(data);
            }).error(function (data) {
                getAllDef.reject(data);
            });

            return getAllDef.promise;
        };

        DepartmentService.create = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DepartmentService.update = function (module) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: module
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DepartmentService.remove = function (id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DepartmentService.sort = function (sort) {
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

        return DepartmentService;

    });