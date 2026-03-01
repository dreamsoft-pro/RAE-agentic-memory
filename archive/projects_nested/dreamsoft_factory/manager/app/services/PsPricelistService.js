angular.module('digitalprint.services')
    .service('PsPricelistService', function ($q, $rootScope, $cacheFactory, Restangular, $config, $http) {

        var PsPricelistService = {};

        var cache = $cacheFactory('ps_priceLists');

        PsPricelistService.getUploadUrl = function (priceListID) {
            return $config.API_URL + ['ps_priceLists', 'uploadIcon', priceListID].join('/');
        };

        PsPricelistService.getAll = function (force) {
            var def = $q.defer();

            if (cache.get('collection') && !force) {
                def.resolve(cache.get('collection'));
            } else {
                Restangular.all('ps_priceLists').getList().then(function (data) {
                    var collection = data.plain();
                    cache.put('collection', collection);
                    if (force) {
                        $rootScope.$emit('ps_priceLists', collection);
                    }
                    def.resolve(collection);
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        PsPricelistService.add = function (item) {
            var def = $q.defer();

            Restangular.all('ps_priceLists').doPOST(item).then(function (data) {
                var collection = data.plain();
                def.resolve(collection);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsPricelistService.edit = function (item) {
            var def = $q.defer();

            Restangular.all('ps_priceLists').customPUT(item).then(function (data) {
                if (data.response) {
                    def.resolve(data.plain());
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsPricelistService.remove = function (item) {
            var def = $q.defer();

            Restangular.all('ps_priceLists').one(item.ID + '').remove().then(function (data) {
                if (data.response) {
                    var collection = cache.get('collection');
                    var idx = _.findIndex(collection, {ID: item.ID});
                    collection.splice(idx, 1);
                    cache.put('collection', collection);
                    $rootScope.$emit('ps_priceLists', collection);
                    def.resolve(collection);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        PsPricelistService.deleteIcon = function (priceListID) {
            var def = $q.defer();

            var resource = ['ps_priceLists'];
            resource.push('uploadIcon');

            Restangular.all(resource.join('/')).one(priceListID + '').remove().then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsPricelistService.devices = function(priceList) {
            var def = $q.defer();

            $http({
                url: $config.API_URL + ['ps_priceLists', priceList.ID, 'ps_priceListDevices'].join('/'),
                method: 'GET'
            }).success(function(data) {
                def.resolve(data);
            }, function(data) {
                def.reject(data);
            });

            return def.promise;
        }

        PsPricelistService.setDevices = function(pricelist, devices) {
            var def = $q.defer();

            $http({
                url: $config.API_URL + ['ps_priceLists', pricelist.ID, 'ps_priceListDevices'].join('/'),
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

        return PsPricelistService;

    });
