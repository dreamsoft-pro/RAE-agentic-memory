'use strict';

angular.module('digitalprint.services')
  .factory('MailContentService', function($q, $http, $config, $cacheFactory) {

    var cache = $cacheFactory('mailContents');

    var MailContentService = function(mailTypeID) {
      this.mailTypeID = mailTypeID;
    }

    MailContentService.prototype.getResource = function() {
      return ['mailTypes', this.mailTypeID, 'mailContents'].join('/');
    }

    MailContentService.prototype.getAll = function(force) {
      var def = $q.defer();

      var resource = this.getResource();

      if(cache.get(resource) && !force) {
        def.resolve(cache.get(resource));
      } else {
        $http({
          method: 'GET',
          url: $config.API_URL + resource
        }).success(function(data){
          cache.put(resource, data);
          def.resolve(data);
        }).error(function(data) {
          def.reject(data);
        });
      }

      return def.promise;
    }

    /*MailContentService.prototype.add = function(item) {
      var def = $q.defer();

      var resource = this.getResource();

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: item
      }).success(function(data) {
        if(data.response) {
          cache.remove(resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });
      
      return def.promise;
    }*/

    MailContentService.prototype.edit = function(item) {
      var def = $q.defer();

      var resource = this.getResource();

      $http({
        method: 'PATCH',
        url: $config.API_URL + resource,
        data: item
      }).success(function(data) {
        if(data.response) {
          cache.remove(resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;

    }

    /*MailContentService.prototype.remove = function(item) {
      var def = $q.defer();
      
      var resource = this.getResource();
      
      $http({
        method: 'DELETE',
        url: $config.API_URL + resource,
        data: item
      }).success(function(data) {
        if(data.response) {
          cache.remove(resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;

    }*/

    return MailContentService;
  });