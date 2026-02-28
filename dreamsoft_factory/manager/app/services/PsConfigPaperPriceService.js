'use strict';

angular.module('digitalprint.services')
  .service('PsPaperPriceService', function($cacheFactory, $q, $config, $http){

    var cache = $cacheFactory('ps_paperPrice');
    var resource;

    var PsConfigPaperPrice = function(attrID, optID) {
      //console.log(attrID);
      this.attrID = attrID;
      this.optID = optID;
      this.setResource();
    }
    var getAllDef = null;

    PsConfigPaperPrice.prototype.getResource = function() {
      return resource;
    }

    PsConfigPaperPrice.prototype.setResource = function() {
      resource =  ['ps_attributes', this.attrID, 'ps_options', this.optID, 'paperPrice'].join('/');
      return true;
    }

    // jeżeli attrID == 0 to pobiera wszystkie
    PsConfigPaperPrice.prototype.getAll = function(force){
      if(_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      if(cache.get(resource) && !force) {
        getAllDef.resolve(cache.get(resource));
      } else {
        $http({
          method: 'GET',
          url: $config.API_URL + resource
        }).success(function(data) {
          cache.put(resource, data);
          getAllDef.resolve(data);
        }).error(function(data) {
          getAllDef.reject(data);
        });
      }

      return getAllDef.promise;
    }

    PsConfigPaperPrice.prototype.set = function(paperPrice) {
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: {amount: paperPrice.amount, expense: paperPrice.expense, price: paperPrice.price}
      }).success(function(data) {
        if(data.response) {
          cache.remove(resource);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      })

      return def.promise;
    }

    PsConfigPaperPrice.prototype.remove = function(id) {
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, id].join('/')
      }).success(function(data) {
        if(data.response) {
          cache.remove(resource);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      })

      return def.promise;
    }

    return PsConfigPaperPrice;

  })