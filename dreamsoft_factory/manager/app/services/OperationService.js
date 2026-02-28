angular.module('digitalprint.services')
    .factory('OperationService', function ($rootScope, $q, $http, $config, $cacheFactory) {

        var OperationService = {};

        var resource = 'operations';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        OperationService.getAll = function (force) {
            if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
                getAllDef = $q.defer();
            } else {
                return getAllDef.promise;
            }

            if (cache.get('collection') && !force) {
                getAllDef.resolve(cache.get('collection'));
            } else {
                $http({
                    method: 'GET',
                    url: $config.API_URL + resource
                }).success(function (data) {
                    cache.put('collection', data);
                    getAllDef.resolve(data);
                }).error(function (data) {
                    getAllDef.reject(data);
                });
            }

            return getAllDef.promise;
        };

        OperationService.create = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                if (data.ID) {
                    cache.remove('collection');
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OperationService.update = function (module) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: module
            }).success(function (data) {
                if (data.response) {
                    cache.remove('collection');
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OperationService.remove = function (id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join("/")
            }).success(function (data) {
                if (data.response) {
                    cache.remove('collection');
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OperationService.sort = function (sort) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'sort'].join('/'),
                data: sort
            }).success(function (data) {
                if (data.response) {
                    cache.remove('collection');
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OperationService.devices = function (operation) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, operation.ID, 'operationDevices'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OperationService.setDevices = function (operation, devices) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, operation.ID, 'operationDevices'].join("/"),
                data: devices
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

        OperationService.processes = function (operation) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, operation.ID, 'operationProcesses'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OperationService.setProcesses = function (operation, processes) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, operation.ID, 'operationProcesses'].join("/"),
                data: processes
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

        return OperationService;
    });
