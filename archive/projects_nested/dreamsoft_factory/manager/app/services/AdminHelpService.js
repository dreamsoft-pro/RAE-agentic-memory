angular.module('digitalprint.services')
  .factory('AdminHelpService', function($rootScope, $q, $http, $config, $cacheFactory){

    var AdminHelpService = {};

    var resource = 'adminHelps';

    var cache = $cacheFactory(resource);

    var getAllDef = null;

    AdminHelpService.getAll = function(force){
      if(_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      
      if(cache.get('collection') && !force) {
        console.log('from cache')
        getAllDef.resolve(cache.get('collection'));
      } else {
        $http({
          method: 'GET',
          url: $config.API_URL + resource
        }).success(function(data) {
          cache.put('collection', data);
          getAllDef.resolve(data);
        }).error(function(data) {
          getAllDef.reject(data);
        });
      }

      return getAllDef.promise;
    }

    AdminHelpService.getModule = function(module) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, module, 'helpKeys'].join('/'),
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    AdminHelpService.create = function(data){
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: data
      }).success(function(data) {
        if(data.response) {
          cache.remove('collection');
          def.resolve(data.item);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    AdminHelpService.update = function(module){
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + resource,
        data: module
      }).success(function(data) {
        if(data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    // remove by ID
    AdminHelpService.remove = function(id){
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, id].join("/")
      }).success(function(data) {
        if(data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    AdminHelpService.getKeys = function(moduleName) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, moduleName, 'helpKeys'].join('/')
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      })

      return def.promise;
    }

    AdminHelpService.addKey = function(moduleName, key) {
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + [resource, moduleName, 'helpKeys'].join('/'),
        data: key
      }).success(function(data) {
        if(data.response){
          def.resolve(data.item);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      })
      return def.promise;
    }

    AdminHelpService.editKey = function(moduleName, key) {
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + [resource, moduleName, 'helpKeys'].join('/'),
        data: key
      }).success(function(data) {
        if(data.response){
          def.resolve(data.item);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      })
      return def.promise;
    }

    AdminHelpService.removeKey = function(moduleName, keyID) {
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, moduleName, 'helpKeys', keyID].join('/')
      }).success(function(data) {
        if(data.response){
          def.resolve(data.item);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      })
      return def.promise;
    }

    return AdminHelpService;
  });
