'use strict';

angular.module('digitalprint.services')
  .factory('PsStaticPrice', function($q, $http, $config, $cacheFactory) {

    var cache = $cacheFactory('ps_static_prices')

    var StaticPrice = function(groupID, typeID, formatID) {
      this.groupID = groupID;
      this.typeID = typeID;
      this.formatID = formatID;
      this.resource = 'ps_groups/'+groupID+'/ps_types/'+typeID+'/ps_formats/'+formatID+'/ps_static_prices';
    }


    StaticPrice.prototype.getAll = function(force) {
      var def = $q.defer();
      var _this = this;

      if(cache.get(this.resource) && !force) {
        def.resolve(cache.get(this.resource));
      } else {
        $http({
          method: 'GET',
          url: $config.API_URL + _this.resource
        }).success(function(data) {
          cache.put(_this.resource, data);
          def.resolve(data);
        }).error(function(data) {
          def.reject(data);
        });
      }

      return def.promise;
    }

    StaticPrice.prototype.set = function(item) {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'PATCH',
        url: $config.API_URL + _this.resource,
        data: item
      }).success(function(data) {
        if(data.response) {
          cache.remove(_this.resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    StaticPrice.prototype.remove = function(id) {
      var def = $q.defer();
      var _this = this;
      
      $http({
        method: 'DELETE',
        url: $config.API_URL + [_this.resource, id].join("/")
      }).success(function(data) {
        if(data.response) {
          cache.remove(_this.resource);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;

    }

    StaticPrice.prototype.export = function() {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'GET',
        url: $config.API_URL + [_this.resource, 'export'].join("/")
      }).success(function(data) {
        if(data.response) {
          def.resolve(data);
        }
        def.reject(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }


    return StaticPrice;

  });