angular.module('digitalprint.services')
    .service('PsWorkspaceService', function ($q, $rootScope, $http, $config, $cacheFactory, Restangular) {

        var PsWorkspaceService = {};

        var cache = $cacheFactory('ps_workspaces');

        PsWorkspaceService.getAll = function (force) {
            var def = $q.defer();

            if (cache.get('collection') && !force) {
                def.resolve(cache.get('collection'));
            } else {
                Restangular.all('ps_workspaces').getList().then(function (data) {
                    var collection = data.plain();
                    cache.put('collection', collection);
                    if (force) {
                        $rootScope.$emit('ps_workspaces', collection);
                    }
                    def.resolve(collection);
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        PsWorkspaceService.add = function (item) {
            var def = $q.defer();

            Restangular.all('ps_workspaces').doPOST(item).then(function (data) {
                if (data.ID) {
                    var collection = cache.get('collection');
                    collection.push(data.plain());
                    cache.put('collection', collection);
                    $rootScope.$emit('ps_workspaces', collection);
                    def.resolve(collection);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsWorkspaceService.edit = function (item) {
            var def = $q.defer();

            Restangular.all('ps_workspaces').customPUT(item).then(function (data) {
                if (data.response) {
                    var collection = cache.get('collection');
                    var idx = _.findIndex(collection, {ID: item.ID});
                    if (idx > -1) {
                        collection[idx] = angular.copy(item);
                    }
                    cache.put('collection', collection);
                    $rootScope.$emit('ps_workspaces', collection);
                    def.resolve(collection);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsWorkspaceService.remove = function (item) {
            var def = $q.defer();

            Restangular.all('ps_workspaces').one(item.ID + '').remove().then(function (data) {
                if (data.response) {
                    var collection = cache.get('collection');
                    var idx = _.findIndex(collection, {ID: item.ID});
                    if (idx > -1) {
                        collection.splice(idx, 1);
                    }
                    cache.put('collection', collection);
                    $rootScope.$emit('ps_workspaces', collection);
                    def.resolve(collection);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        PsWorkspaceService.getByPrintType = function (printTypeID) {
            var def = $q.defer();

            Restangular.all('ps_workspaces/getByPrintType/' + printTypeID).getList().then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });


            return def.promise;
        };

        PsWorkspaceService.devices = function(workspace) {
            var def = $q.defer();

            $http({
                url: $config.API_URL + ['ps_workspaces', workspace.ID, 'ps_workspaceDevices'].join('/'),
                method: 'GET'
            }).success(function(data) {
                def.resolve(data);
            }, function(data) {
                def.reject(data);
            });

            return def.promise;
        }

        PsWorkspaceService.setDevices = function(workspace, devices) {
            var def = $q.defer();

            $http({
                url: $config.API_URL + ['ps_workspaces', workspace.ID, 'ps_workspaceDevices'].join('/'),
                method: 'PATCH',
                data: devices
            }).success(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        return PsWorkspaceService;

    });
