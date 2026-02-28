'use strict';

angular.module('digitalprint.services')
  .service('OrderService', function($q, $config, $http, $cacheFactory){

    var OrderService = {};

    var resource = 'orders';

    var cache = $cacheFactory(resource);

    var getAllDef = null;

    OrderService.getAll = function(force){
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

    OrderService.ongoings = function(orderID) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, orderID, 'ongoings'].join("/")
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    OrderService.files = function(orderID) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, 'files', orderID].join("/")
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    OrderService.patchOngoings = function(orderID, ongoingID, data) {
      var def = $q.defer();

      $http({
        method: 'PATCH',
        url: $config.API_URL + [resource, orderID, 'ongoings', ongoingID].join("/"),
        data: data
      }).success(function(data) {
        if(data.stateChange && data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    OrderService.updateOngoings = function(orderID, ongoingID, elem) {
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + [resource, orderID, 'ongoings', ongoingID].join("/"),
        data: elem
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
    };

    OrderService.ongoingsLogs = function(orderID) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, orderID, 'ongoings', 'logs'].join("/")
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    OrderService.productCard = function(orderID) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, 'productCard', orderID].join("/")
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };


    OrderService.accept = function(orderID, accept) {
      var def = $q.defer();

      $http({
        method: 'PATCH',
        url: $config.API_URL + [resource, orderID].join('/'),
        data: {accept: accept}
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

    OrderService.noAccept = function(orderID, acceptInfo, acceptFiles) {
      var def = $q.defer();

      $http({
        method: 'PATCH',
        url: $config.API_URL + [resource, orderID].join('/'),
        data: {
          accept: -1,
          acceptInfo: acceptInfo,
          acceptFiles: acceptFiles
        }
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

    return OrderService;
  });
