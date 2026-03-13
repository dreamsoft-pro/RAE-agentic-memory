angular.module('digitalprint.services')
    .service('SettingService', function ($rootScope, $q, $config, $http, localStorageService, $cacheFactory) {

        var resource;
        var cache = $cacheFactory('settings');

        var SettingService = function (module) {
            this.module = module;
            resource = ['settings', this.module].join('/');
        };

        SettingService.prototype.setModule = function (module) {
            this.module = module;
            resource = ['settings', this.module].join('/');
        };

        SettingService.prototype.getAll = function (force) {
            var def = $q.defer();

            if (cache.get(this.module) && !force) {
                def.resolve(cache.get(this.module));
            } else {
                $http({
                    method: 'GET',
                    url: $config.API_URL + resource
                }).success(function (data) {
                    def.resolve(data);
                }).error(function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        SettingService.prototype.save = function (data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                cache.remove(this.module);
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

        SettingService.prototype.delete = function (key) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + resource + '/' + key
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return SettingService;
    });