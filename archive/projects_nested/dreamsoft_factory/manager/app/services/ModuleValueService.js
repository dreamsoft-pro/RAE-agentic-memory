angular.module('digitalprint.services')
    .service('ModuleValueService', function ($rootScope, $q, $http, $config, $cacheFactory) {


        var cache = $cacheFactory('moduleValue');

        var ModuleValueService = function (module) {
            this.module = module;
            this.resource = ['modules', this.module, 'module_values'].join('/');
            this.getAllDef = null
        };


        ModuleValueService.prototype.getAll = function (force) {
            var _this = this;

            if (_.isNull(_this.getAllDef) || force) {
                _this.getAllDef = $q.defer();
            } else {
                return _this.getAllDef.promise;
            }

            if (cache.get(this.module) && !force) {
                _this.getAllDef.resolve(cache.get(this.module));
            } else {
                $http({
                    method: 'GET',
                    url: $config.API_URL + this.resource
                }).success(function (data) {
                    cache.put(this.module, data);
                    $rootScope.$emit('ModuleValue.getAll', data);
                    _this.getAllDef.resolve(data);
                }).error(function (data) {
                    _this.getAllDef.reject(data);
                });
            }

            return _this.getAllDef.promise;
        };

        ModuleValueService.prototype.getList = function (params) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + this.resource,
                params: params
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ModuleValueService.prototype.update = function (courier) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + this.resource,
                data: courier
            }).success(function (data) {
                if (data.response) {
                    cache.remove(this.module);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return ModuleValueService;
    });
