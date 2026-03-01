angular.module('digitalprint.services')
  .service('PsIncreaseTypeService', function($q, $rootScope, $cacheFactory, Restangular) {

    var PsIncreaseTypeService = {};

    var cache = $cacheFactory('ps_increase_types');

    PsIncreaseTypeService.getAll = function(force) {
      var def = $q.defer();

      if(cache.get('collection') && !force) {
        def.resolve(cache.get('collection'));
      } else {
        Restangular.all('ps_increase_types').getList().then(function(data) {
          var collection = data.plain();
          cache.put('collection', collection);
          if(force) {
            $rootScope.$emit('ps_increase_types', collection);
          }
          def.resolve(collection);
        }, function(data) {
          def.reject(data);
        });
      }

      return def.promise;
    }

    return PsIncreaseTypeService;

  });