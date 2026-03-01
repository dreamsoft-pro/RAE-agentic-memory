angular.module('digitalprint.services')
  .factory('OperatorService', function($rootScope, $q, $http, $config, $cacheFactory, ApiCollection){

    var OperatorService = {};

    var resource = 'operators';

    var cache = $cacheFactory(resource);

    var getAllDef = null;

    OperatorService.getAll = function(force){
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
    };

    OperatorService.create = function(data){
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: data
      }).success(function(data) {
        if(data.ID) {
          cache.remove('collection');
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    OperatorService.update = function(module){
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + resource,
        data: module
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
    };

    OperatorService.remove = function(id){
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, id].join("/")
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
    };

    OperatorService.skills = function(operator) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, operator.ID, 'operatorSkills'].join('/')
      }).success(function(data) {
        def.resolve(data);
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    OperatorService.setSkills = function(operator, skills) {
      var def = $q.defer();

      $http({
        method: 'PATCH',
        url: $config.API_URL + [resource, operator.ID, 'operatorSkills'].join("/"),
        data: skills
      }).success(function(data) {
        console.log('success auth');
        if(data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        console.log('error auth');
        def.reject(data);
      });

      return def.promise;
    };

    OperatorService.logs = function(operator, config) {
      var res = [resource, operator.ID, 'operatorLogs'].join("/");

      config.count = res + '/count';
      var logsCtrl = new ApiCollection(res, config);
      return logsCtrl;

    };

    OperatorService.getOperator = function(operatorID) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, operatorID, 'getOperator'].join('/')
      }).success(function(data) {
        def.resolve(data);
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    };

    return OperatorService;
  });
