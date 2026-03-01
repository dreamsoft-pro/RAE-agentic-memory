'use strict';

angular.module('digitalprint.services')
  .service('PsPrintTypeService', function($q, Restangular, $cacheFactory, $http, $config) {

    var cache = $cacheFactory('ps_printtypes');

    var PrintTypeService = {};

    PrintTypeService.getResource = function() {
      return 'ps_printtypes';
    }

    PrintTypeService.getAll = function(force) {
      var def = $q.defer();

      var resource = this.getResource();

      if(cache.get(resource) && !force) {
        def.resolve(cache.get(resource));
      } else {
        Restangular.all(resource).getList().then(function(data) {
          cache.put(resource, data.plain()); // nie zwracamy plain bo potrzebujemy obiekt do put
          def.resolve(data.plain());
        }, function(data) {
          def.reject(data);
        });
      }

      return def.promise;
    }

    PrintTypeService.add = function(item) {
      var def = $q.defer();

      var resource = this.getResource();

      Restangular.all(resource).doPOST(item).then(function(data) {
        if(data.ID) {
          cache.remove(resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    PrintTypeService.edit = function(item) {
      var def = $q.defer();

      var resource = this.getResource();

      Restangular.all(resource).customPUT(item).then(function(data) {
        if(data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;

    }

    PrintTypeService.remove = function(item) {
      var def = $q.defer();
      
      var resource = this.getResource();
      
      Restangular.all(resource).one(item.ID+'').remove().then(function(data) {
        if(data.response) {
          cache.remove(resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;

    }

    PrintTypeService.devices = function(printtype) {
      var def = $q.defer();

      $http({
        url: $config.API_URL + [this.getResource(), printtype.ID, 'ps_printtypeDevices'].join('/'),
        method: 'GET'
      }).success(function(data) {
        def.resolve(data);
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    PrintTypeService.setDevices = function(printtype, devices) {
      var def = $q.defer();

      $http({
        url: $config.API_URL + [this.getResource(), printtype.ID, 'ps_printtypeDevices'].join('/'),
        method: 'PATCH',
        data: devices
      }).success(function(data) {
        if(data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    return PrintTypeService;
  });
