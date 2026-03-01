'use strict';

angular.module('digitalprint.services')
    .service('PsConfigAttributeNatureService', ['Restangular', '$cacheFactory', '$q', function (Restangular,
                                                                                              $cacheFactory, $q) {

        var resource = 'ps_attributenatures';

        var cache = $cacheFactory(resource);

        var PsConfigAttributeTypeService = {};


        PsConfigAttributeTypeService.getAll = function (force) {
            var def = $q.defer();

            if (cache.get('collection') && !force) {
                def.resolve(cache.get('collection'));
            } else {
                Restangular.all(resource).getList().then(function (data) {
                    cache.put('collection', data.plain());
                    def.resolve(data);
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        return PsConfigAttributeTypeService;

    }]);
