'use strict';

angular.module('digitalprint.services')
    .service('PsConfigAttributeService', ['Restangular', '$cacheFactory', '$q', '$http', '$config', function (Restangular, $cacheFactory, $q, $http, $config) {

        var resource = 'ps_attributes';

        var cache = $cacheFactory(resource);

        var PsConfigAttribute = {};


        PsConfigAttribute.getAll = function (force) {
            var def = $q.defer();

            if (cache.get('collection') && !force) {
                def.resolve(cache.get('collection'));
            } else {
                Restangular.all(resource).getList().then(function (data) {
                    var plain = data.plain();
                    cache.put('collection', plain);
                    def.resolve(plain);
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        PsConfigAttribute.getOne = function (attrID) {
            var def = $q.defer();

            Restangular.one(resource + '/' + attrID).get().then(function (data) {
                if (data.ID) {
                    def.resolve(data.plain());
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };


        PsConfigAttribute.add = function (item) {
            var def = $q.defer();

            Restangular.all(resource).doPOST(item).then(function (data) {
                if (data.ID) {
                    cache.remove('collection');
                    def.resolve(data);
                }
                def.reject(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        PsConfigAttribute.edit = function (item) {
            var def = $q.defer();

            Restangular.all(resource).customPUT(item).then(function (data) {
                if (data.response) {
                    cache.remove('collection');
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigAttribute.remove = function (item) {
            var def = $q.defer();

            Restangular.all(resource).one(item.ID + '').remove().then(function (data) {
                if (data.response) {
                    cache.remove('collection');
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        PsConfigAttribute.sort = function (sortList) {
            var def = $q.defer();

            Restangular.all(resource).one('sortAttr').patch(sortList).then(function (data) {
                if (data.response === true) {
                    def.resolve(data);
                }
                def.reject(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigAttribute.countProducts = function (force) {
            var def = $q.defer();

            if (cache.get('countProducts') && !force) {
                def.resolve(cache.get('countProducts'));

            } else {
                Restangular.one('ps_product_options_count').get().then(function (data) {
                    cache.put('countProducts', data.plain());
                    def.resolve(data.plain());

                }, function (data) {
                    def.reject(data);
                })
            }

            return def.promise;

        };

        PsConfigAttribute.copy = function (attrID) {
            var def = $q.defer();

            var collection = cache.get('collection');

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'copy', attrID].join('/')
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

        PsConfigAttribute.getCustomNames = function (typeID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'checkCustomNames', typeID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigAttribute.getAttributeSettings = function (typeID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getAttributeSettings', typeID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };


        PsConfigAttribute.getFilterConfig = function (attrID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + ['attributeFilters' , attrID  ].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigAttribute.getOptions = function (attrID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + ['attributeOptions' , attrID  ].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };
     function getResource() {
            return ['ps_attributes'];
        }

        PsConfigAttribute.getUploadUrl = function () {
            var resource = getResource();
            resource.push('uploadIcon');
            return $config.API_URL + resource.join('/');
        };

        PsConfigAttribute.deleteIcon = function (categoryID) {
            var def = $q.defer();

            var resource = getResource();
            resource.push('uploadIcon');
            resource.push(categoryID);

            $http({
                method: 'DELETE',
                url: $config.API_URL + resource.join('/')
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            });
            return def.promise;
        };

        return PsConfigAttribute;
    }]);
