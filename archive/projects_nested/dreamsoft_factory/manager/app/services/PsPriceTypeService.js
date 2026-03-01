angular.module('digitalprint.services')
  .service('PsPriceTypeService', function($q, $rootScope, $cacheFactory, Restangular) {

    var PsPriceTypeService = {};

    var cache = $cacheFactory('ps_pricetypes');

    PsPriceTypeService.getAll = function(force) {
      var def = $q.defer();

      if(cache.get('collection') && !force) {
        def.resolve(cache.get('collection'));
      } else {
        Restangular.all('ps_pricetypes').getList().then(function(data) {
          var collection = data.plain();
          cache.put('collection', collection);
          if(force) {
            $rootScope.$emit('ps_pricetypes', collection);
          }
          def.resolve(collection);
        }, function(data) {
          def.reject(data);
        });
      }

      return def.promise;
    }

    return PsPriceTypeService;

  });