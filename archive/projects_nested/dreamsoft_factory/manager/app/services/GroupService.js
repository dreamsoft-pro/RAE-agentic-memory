angular.module('digitalprint.services')
  .service('GroupService', function($q, Restangular, $http, $config){

    var GroupService = {};

    GroupService.getAll = function(){
      var def = $q.defer();

      Restangular.all('groups').getList().then(function(data){
        def.resolve(data.plain());
      });

      return def.promise;
    }

    GroupService.create = function(group){
      var def = $q.defer();

      Restangular.all('groups').post(group).then(function(data){
        def.resolve(data.plain());
      });

      return def.promise;
    }

    GroupService.update = function(group){
      var def = $q.defer();

      Restangular.one('groups').customPUT(group).then(function(data){
        if(data.response){
          def.resolve(data.plain());
        }else{
          def.reject();
        }
      });

      return def.promise;
    }

    GroupService.remove = function(id, group){
      var def = $q.defer();

      Restangular.one('groups', id).doDELETE().then(function(data){
        def.resolve(data.plain());
      });

      return def.promise;
    }

    GroupService.getRoles = function(group) {
      var def = $q.defer();

      var resource = ['groups', group.ID, 'groupRoles'].join('/');
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

    GroupService.setRoles = function(group, items) {
      var def = $q.defer();

      var resource = ['groups', group.ID, 'groupRoles'].join('/');
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

    return GroupService;
  });
