angular.module('digitalprint.services')
  .service('PsConfigIncreaseTypeService', function($q, $rootScope, $cacheFactory, Restangular) {

    var PsIncreaseTypeService = {};

    var cache = $cacheFactory('ps_config_increaseTypes');

    PsIncreaseTypeService.getAll = function(force) {
      var def = $q.defer();

      if(cache.get('collection') && !force) {
        def.resolve(cache.get('collection'));
      } else {
        Restangular.all('ps_config_increaseTypes').getList().then(function(data) {
          var collection = data.plain();
          cache.put('collection', collection);
          if(force) {
            $rootScope.$emit('ps_config_increaseTypes', collection);
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