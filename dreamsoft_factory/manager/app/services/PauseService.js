angular.module('digitalprint.services')
    .factory('PauseService', function($rootScope, $q, $http, $config, $cacheFactory) {

        var PauseService = {};
        var resource = 'pauses';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        PauseService.getAll = function(force) {
            if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
                getAllDef = $q.defer();
            } else {
                return getAllDef.promise;
            }

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function(data) {
                cache.put('collection', data);
                getAllDef.resolve(data);
            }).error(function(data) {
                getAllDef.reject(data);
            });

            return getAllDef.promise;
        };

        PauseService.create = function(data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: data
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        PauseService.update = function(module) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: module
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        PauseService.updateReportSheets = function (data) {
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

        PauseService.remove = function(id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        PauseService.sort = function(sort) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'sort'].join('/'),
                data: sort
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        return PauseService;

    });