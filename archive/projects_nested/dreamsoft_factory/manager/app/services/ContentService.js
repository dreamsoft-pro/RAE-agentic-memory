angular.module('digitalprint.services')
  .service('ContentService', function($rootScope, $q, $http, $config, $cacheFactory){

    var cache = $cacheFactory('mainContents');

    var getAllDef = null;

    var ContentService = function(routeID) {
      this.routeID = routeID;
      this.resource = ['routes', routeID, 'mainContents'].join('/');
    };

    ContentService.prototype.getAll = function(force){
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'GET',
        url: $config.API_URL + _this.resource
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ContentService.prototype.getAllCache = function(force){
      var _this = this;

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
          url: $config.API_URL + _this.resource
        }).success(function(data) {
          cache.put(_this.routeID, data);
          getAllDef.resolve(data);
        }).error(function(data) {
          getAllDef.reject(data);
        });
      }

      return getAllDef.promise;
    };

    ContentService.prototype.move = function() {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + _this.resource
      }).success(function(data) {
        cache.remove(_this.routeID);
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ContentService.prototype.create = function(content){
      var _this = this;
      var def = $q.defer();
      $http({
        method: 'POST',
        url: $config.API_URL + _this.resource,
        data: content
      }).success(function(data) {
        if(data.response) {
          cache.remove(_this.routeID);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };


    ContentService.prototype.edit = function(content) {
      var _this = this;
      var def = $q.defer();

      content.action = "edit";

      $http({
        method: 'patch',
        url: $config.API_URL + [_this.resource, content.ID].join('/'),
        data: content
      }).success(function(data) {
        if(data.response) {
          cache.remove(_this.routeID);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      });
      return def.promise;
    };

    // remove by ID
    ContentService.prototype.remove = function(content){
      var _this = this;
      var def = $q.defer();
      $http({
        method: 'DELETE',
        url: $config.API_URL + [_this.resource, content.ID].join('/')
      }).success(function(data) {
        if(data.response) {
          cache.remove(_this.contentID);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    return ContentService;
  });
