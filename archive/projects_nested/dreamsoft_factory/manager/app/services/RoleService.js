angular.module('digitalprint.services')
  .service('RoleService', function($q, Restangular){

    var RoleService = {};

    RoleService.getAll = function(){
      var def = $q.defer();

      Restangular.all('roles').getList().then(function(data){
        def.resolve(data.plain());
      })

      return def.promise;
    }

    RoleService.getRolePerms = function(id){
      var def = $q.defer();

      Restangular.one('roles', id).one('rolePerms').get().then(function(data){
        def.resolve(data.plain());
      })

      return def.promise;
    }

    RoleService.updateSelectedRolePerms = function(id, selected){
      var def = $q.defer();

      Restangular.one('roles', id).post('rolePerms', selected).then(function(data){
        if(data.response){
          def.resolve(data.plain());
        }else{
          def.reject();
        }
      })

      return def.promise;
    }

    RoleService.create = function(group){
      var def = $q.defer();

      Restangular.all('roles').post(group).then(function(data){
        def.resolve(data.plain());
      });

      return def.promise;
    }

    RoleService.update = function(group){
      var def = $q.defer();

      Restangular.one('roles').customPUT(group).then(function(data){
        if(data.response){
          def.resolve(data.plain());
        }else{
          def.reject();
        }
      });

      return def.promise;
    }

    RoleService.remove = function(id, group){
      var def = $q.defer();

      Restangular.one('roles', id).doDELETE().then(function(data){
        def.resolve(data.plain());
      });

      return def.promise;
    }

    return RoleService;
  });
