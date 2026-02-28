'use strict';

angular.module('digitalprint.services')
  .factory('StatusService', function($rootScope, $q, $http, $config, $cacheFactory){

    var StatusService = {};

    var resource = 'statuses';

    var cache = $cacheFactory(resource);

    var getAllDef = null;

    StatusService.getAll = function(force){
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

    StatusService.create = function(data){
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

    StatusService.update = function(module){
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

    StatusService.remove = function(id){
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

    return StatusService;
  });
