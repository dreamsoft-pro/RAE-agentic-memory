angular.module('digitalprint.services')
  .service('PsPreflightFolderService', function($rootScope, $q, $http, $config, $cacheFactory){

    var PsPreflightFolderService = {};

    var cache = $cacheFactory('ps_preflightFolder');

    var getAllDef = null;

    PsPreflightFolderService = function(formatID) {
      this.formatID = formatID;
      this.resource = 'ps_preflightFolder';
      this.getAllResource = 'ps_preflightFolder?formatID='+formatID;
    }

    PsPreflightFolderService.prototype.getAll = function(force){
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'GET',
        url: $config.API_URL + _this.getAllResource,
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    PsPreflightFolderService.prototype.getAllCache = function(force){
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
          url: $config.API_URL + _this.getAllResource,
        }).success(function(data) {
          cache.put(_this.categoryID, data);
          getAllDef.resolve(data);
        }).error(function(data) {
          getAllDef.reject(data);
        });
      }

      return getAllDef.promise;
    }

    PsPreflightFolderService.prototype.add = function(item){
      var _this = this;
      var def = $q.defer();
      item.formatID = this.formatID;

      $http({
        method: 'POST',
        url: $config.API_URL + [_this.resource, _this.formatID].join('/'),
        data: item
      }).success(function(data) {
        if(data.response) {
          cache.remove(_this.formatID);
          def.resolve(data.item);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });



      return def.promise;
    }


    PsPreflightFolderService.prototype.edit = function(item) {
      var _this = this;
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + _this.resource,
        data: item
      }).success(function(data) {
        if(data.response) {
          cache.remove(_this.categoryID);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      });
      return def.promise;
    }

    // remove by ID
    PsPreflightFolderService.prototype.remove = function(item){
      console.log(item)
      var _this = this;
      var def = $q.defer();
      $http({
        method: 'DELETE',
        url: $config.API_URL + [_this.resource, item.ID].join('/')
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
    }

    return PsPreflightFolderService;
  });
