angular.module('digitalprint.services')
    .factory('ShiftService', function ($rootScope, $q, $http, $config, $cacheFactory) {

        var ShiftService = {};
        var resource = 'shifts';
        var deviceResource = 'deviceShift';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        ShiftService.getAll = function (force) {
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

        ShiftService.create = function (data) {
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

        ShiftService.update = function (module) {
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

        ShiftService.remove = function (id) {
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

        ShiftService.sort = function (sort) {
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

        //FOR DEVICES
        ShiftService.getAllFromDevice = function (deviceID) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + deviceResource + '/' + deviceID
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ShiftService.createForDevice = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + deviceResource,
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ShiftService.updateOnDevice = function (module) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + deviceResource,
                data: module
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ShiftService.removeFromDevice = function (id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [deviceResource, id].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ShiftService.sortOnDevice = function (sort) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [deviceResource, 'sort'].join('/'),
                data: sort
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ShiftService.copyFrom = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [deviceResource, 'copyFrom'].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return ShiftService;

    });