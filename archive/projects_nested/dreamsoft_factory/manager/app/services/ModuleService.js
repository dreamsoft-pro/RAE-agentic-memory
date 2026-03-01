angular.module('digitalprint.services')
    .service('ModuleService', function ($rootScope, $q, $http, $config, $cacheFactory) {

        var ModuleService = {};

        var resource = 'modules';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        ModuleService.getAll = function (force) {
            if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
                getAllDef = $q.defer();
            } else {
                return getAllDef.promise;
            }
            // var def = $q.defer();

            if (cache.get('collection') && !force) {
                getAllDef.resolve(cache.get('collection'));
            } else {
                $http({
                    method: 'GET',
                    url: $config.API_URL + resource
                }).success(function (data) {
                    cache.put('collection', data);
                    $rootScope.$emit('Module.getAll', data);
                    getAllDef.resolve(data);
                }).error(function (data) {
                    getAllDef.reject(data);
                });
            }

            return getAllDef.promise;
        };

        ModuleService.getExtended = function (type, func) {
            var def = $q.defer();
            func = func || null;

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'extended'].join('/'),
                params: {type: type, func: func}
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ModuleService.create = function (module) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: module
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

        ModuleService.update = function (module) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: module
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

        ModuleService.remove = function (id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join("/")
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

        ModuleService.getKeys = function (module) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, module.ID, 'module_keys'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ModuleService.addKey = function (moduleID, requestData) {
            var def = $q.defer();

            console.log('requestData: ', requestData);

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, moduleID, 'module_keys'].join("/"),
                data: requestData
            }).success(function (data) {
                if (data.item) {
                    def.resolve(data.item);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ModuleService.editKey = ModuleService.addKey;

        ModuleService.removeKey = function (moduleID, keyID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, moduleID, 'module_keys', keyID].join("/")
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

        ModuleService.getOptions = function (moduleID, keyID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, moduleID, 'module_keys', keyID, 'module_options'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ModuleService.addOption = function (moduleID, keyID, option) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, moduleID, 'module_keys', keyID, 'module_options'].join("/"),
                data: option
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data.item);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ModuleService.editOption = ModuleService.addOption;

        ModuleService.removeOption = function (moduleID, keyID, optionID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, moduleID, 'module_keys', keyID, 'module_options', optionID].join("/")
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

        return ModuleService;
    });
