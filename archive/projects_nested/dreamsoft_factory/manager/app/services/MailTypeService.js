angular.module('digitalprint.services')
  .factory('MailTypeService', function($rootScope, $q, $http, $config, $cacheFactory) {

    var MailTypeService = {};

    var resource = 'mailTypes';

    var cache = $cacheFactory(resource);

    var getAllDef = null;

    MailTypeService.getAll = function(force) {
      if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      if (cache.get('collection') && !force) {
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

    MailTypeService.get = function(id) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, id].join('/'),
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }


    MailTypeService.variables = function(mailTypeID, data) {
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + [resource, mailTypeID, 'mailVariables'].join('/'),
        data: data
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    MailTypeService.removeVariable = function(mailTypeID, variableID) {
      var def = $q.defer();
      console.log(variableID);
      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, mailTypeID, 'mailVariables', variableID].join('/')
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    MailTypeService.editVariable = function(mailTypeID, data) {
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + [resource, mailTypeID, 'mailVariables'].join('/'),
        data: data
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    MailTypeService.getVariables = function(mailTypeID) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, mailTypeID, 'mailVariables'].join('/'),
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    MailTypeService.create = function(data) {
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: data
      }).success(function(data) {
        if (data.ID) {
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

    MailTypeService.update = function(offer) {
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + resource,
        data: offer
      }).success(function(data) {
        if (data.response) {
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

    // remove by ID
    MailTypeService.remove = function(id) {
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, id].join("/")
      }).success(function(data) {
        if (data.response) {
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

    return MailTypeService;
  });