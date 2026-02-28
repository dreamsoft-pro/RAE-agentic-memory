angular.module('digitalprint.services')
  .factory('RouteService', function($rootScope, $q, $http, $config, $cacheFactory){

    var RouteService = {};

    var resource = 'routes';

    var cache = $cacheFactory(resource);

    var getAllDef = null;

    RouteService.getAll = function(force){
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

    RouteService.getOne = function(routeID) {
      var def = $q.defer();
      console.log(routeID)
      $http({
        method: 'GET',
        url: $config.API_URL + [resource, 'one', routeID].join('/')
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    RouteService.move = function() {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, 'move'].join('/')
      }).success(function(data) {
        cache.remove('collection');
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    RouteService.create = function(data){
      var def = $q.defer();
      console.log (data)
      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: data
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

     RouteService.edit = function(elem) {
      var def = $q.defer();
      elem.action = "edit";

      elem.langNames = _.extend({}, elem.langNames);
      elem.langUrls = _.extend({}, elem.langUrls);

      console.log( elem );

      $http({
        method: 'PATCH',
        url: $config.API_URL + [resource, elem.ID].join('/'),
        data: elem
      }).success(function(data) {
        if(data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      });
      return def.promise;
    }

   RouteService.level = function(state) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, 'level', state].join('/'),
      }).success(function(data) {
        def.resolve(data);
      });
      return def.promise;
    }

    // remove by ID
    RouteService.remove = function(state){
      var def = $q.defer();
      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, state].join("/")
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

    return RouteService;
  });
