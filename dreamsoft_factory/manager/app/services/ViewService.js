'use strict';

angular.module('digitalprint.services')
  .service('ViewService', function($q, $config, $http) {

    var resource;

    var ViewService = function(routeID, viewID) {
      this.routeID = routeID;
      this.viewID = viewID;
    };

    ViewService.prototype.getResource = function() {
      return 'dp_views';
    };

    ViewService.prototype.getAll = function() {

      var def = $q.defer();
      var resource = this.getResource();

      $http({
        method: 'GET',
        url: $config.API_URL + resource + '?routeID=' + this.routeID
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.makeViewReplace = function(replaceID) {
      var def = $q.defer();
      var resource = this.getResource();
      var data = {
        replaceID: replaceID, 
        routeID: this.routeID
      };

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: data
      }).success(function(data) {
        if( data.response) {
          def.resolve(data)
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.getAllNestedViews = function() {

      var def = $q.defer();
      var resource = this.getResource();

      $http({
        method: 'GET',
        url: $config.API_URL + resource
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.getReplaceViews = function() {
      var def = $q.defer();
      var resource = this.getResource();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, 'mainVariables', this.routeID].join('/')
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.add = function(data) {
      data.routeID = this.routeID;
      var def = $q.defer();
      var resource = this.getResource();

      $http({
        method: 'POST',
        url: $config.API_URL + [resource, '?routeID=' + this.routeID].join('/'),
        data: data
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.edit = function(data) {

      var def = $q.defer();
      var resource = this.getResource();

      $http({
        method: 'PUT',
        url: $config.API_URL + [resource, '?routeID=', this.routeID].join('/'),
        data: data
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.remove = function(dataID) {

      var def = $q.defer();
      var resource = this.getResource();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, dataID].join('/')
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.sort = function(sort) {
      var def = $q.defer();
      var resource = this.getResource();
      var data = {
        orders: sort,
        routeID: this.routeID
      };

      $http({
        method: 'PATCH',
        url: $config.API_URL + [resource, 'sort'].join('/'),
        data: data
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

    // Variables

    ViewService.prototype.getAllVariables = function(viewID) {

    	var resource = this.getResource();
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, 'variables?viewID='+viewID].join('/')
      }).success(function(data) {
      	console.log(data);
        	def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;

    };

    ViewService.prototype.addVariable = function(data, viewID) {
      var def = $q.defer();
      var resource = this.getResource();

      $http({
        method: 'POST',
        url: $config.API_URL + [resource, 'variables'].join('/'),
        data: data
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.addViewTemplate = function(data) {

      var def = $q.defer();
      var resource = this.getResource();

      $http({
        method: 'PUT',
        url: $config.API_URL + resource,
        data: data
      }).success(function(data) {
        console.log(data);
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(dat);
      });

      return def.promise;
    };

    ViewService.prototype.editVariable = function(data) {

    	var resource = this.getResource();
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + [resource, 'variables'].join('/'),
        data: data
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    ViewService.prototype.removeVariable = function(variableID) {

    	var resource = this.getResource();
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, 'variables', variableID].join('/')
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    // End of Variables

    return ViewService;

  });