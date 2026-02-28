angular.module('digitalprint.services')
  .factory('ModuleTypeService', function($rootScope, $q, $http, CacheService){

    var ModuleTypeService = {};

    var cacheResolve = new CacheService('module_types');

    var resource = 'module_types';

    ModuleTypeService.getAll = function() {
      var def = $q.defer();

      cacheResolve.doRequest(resource).then(function(data){
        $rootScope.$emit('ModuleTypeService.getAll', data);
        def.resolve(data);
      }, function(data){
        def.reject(data);
      });

      return def.promise;
    }

    return ModuleTypeService;
  });
