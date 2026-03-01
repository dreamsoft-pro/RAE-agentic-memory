angular.module('digitalprint.services')
  .service('PermissionService', function($q, Restangular, $http, $config){

    var PermissionService = {};

    PermissionService.getAll = function(){
      var def = $q.defer();

      Restangular.all('aclPermissions').getList().then(function(data){
        def.resolve(data.plain());
      })

      return def.promise;
    }

    PermissionService.create = function(permission) {
      var def = $q.defer();

      var resource = 'aclPermissions'
      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: permission
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    PermissionService.update = function(permission) {
      var def = $q.defer();

      var resource = 'aclPermissions'
      $http({
        method: 'PUT',
        url: $config.API_URL + resource,
        data: permission
      }).success(function(data) {
        if(data.response){
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    PermissionService.remove = function(id) {
      var def = $q.defer();

      var resource = ['aclPermissions', id].join("/");
      $http({
        method: 'DELETE',
        url: $config.API_URL + resource
      }).success(function(data) {
        if(data.response){
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    return PermissionService;
  });
