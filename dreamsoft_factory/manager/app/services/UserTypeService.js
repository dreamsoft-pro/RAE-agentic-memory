angular.module('digitalprint.services')
  .service('UserTypeService', function($q, Restangular, $http, $config){

    var UserTypeService = {};

    UserTypeService.getAll = function(){
      var def = $q.defer();

      Restangular.all('userTypes').getList().then(function(data){
        def.resolve(data.plain());
      });

      return def.promise;
    }

    UserTypeService.create = function(type){
      var def = $q.defer();

      Restangular.all('userTypes').post(type).then(function(data){
        def.resolve(data.plain());
      });

      return def.promise;
    }

    UserTypeService.update = function(type){
      var def = $q.defer();

      Restangular.one('userTypes').customPUT(type).then(function(data){
        if(data.response){
          def.resolve(data.plain());
        }else{
          def.reject();
        }
      });

      return def.promise;
    }

    UserTypeService.remove = function(id, type){
      var def = $q.defer();

      Restangular.one('userTypes', id).doDELETE().then(function(data){
        def.resolve(data.plain());
      });

      return def.promise;
    }

    UserTypeService.getTypeRoles = function(type) {
      var def = $q.defer();

      var resource = ['userTypes', 'userTypeRoles', type.ID].join('/');
      $http({
        method: 'GET',
        url: $config.API_URL + resource
      }).success(function(data) {
        if(data.response) {
          def.resolve(data.items);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    UserTypeService.setTypeRoles = function(type, items) {
      var def = $q.defer();

      var resource = ['userTypes', 'userTypeRoles', type.ID].join('/');
      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: items
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

    UserTypeService.getTypeGroups = function(type) {
      var def = $q.defer();

      var resource = ['userTypes', 'userTypeGroups', type.ID].join('/');

      $http({
        method: 'GET',
        url: $config.API_URL + resource
      }).success(function(data) {
        if(data.response) {
          def.resolve(data.items);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    UserTypeService.setTypeGroups = function(type, items) {
      var def = $q.defer();

      var resource = ['userTypes', 'userTypeGroups', type.ID].join('/');

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: items
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

    return UserTypeService;
  });
