angular.module('digitalprint.services')
  .factory('SkillService', function($rootScope, $q, $http, $config, $cacheFactory){

    var SkillService = {};

    var resource = 'skills';

    var cache = $cacheFactory(resource);

    var getAllDef = null;

    SkillService.getAll = function(force){
      if(_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      if(cache.get('collection') && !force) {
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

    SkillService.devices = function(skill) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, skill.ID, 'skillDevices'].join('/')
      }).success(function(data) {
        def.resolve(data);
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    SkillService.setDevices = function(skill, devices) {
      var def = $q.defer();

      $http({
        method: 'PATCH',
        url: $config.API_URL + [resource, skill.ID, 'skillDevices'].join("/"),
        data: devices
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

    SkillService.create = function(data){
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: data
      }).success(function(data) {
        if(data.ID) {
          cache.remove('collection');
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    SkillService.update = function(module){
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + resource,
        data: module
      }).success(function(data) {
        if(data.response) {
          cache.remove('collection');
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
    SkillService.remove = function(id){
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, id].join("/")
      }).success(function(data) {
        if(data.response) {
          cache.remove('collection');
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    return SkillService;
  });
