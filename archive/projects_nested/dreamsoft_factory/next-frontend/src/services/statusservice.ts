javascript
'use strict';

angular.module('digitalprint.services')
  .factory('StatusService', function($rootScope, $q, $http, $config, $cacheFactory) {
    var StatusService = {};

    const resource = 'statuses';
    const cache = $cacheFactory(resource);
    
    let getAllDef = null;

    StatusService.getAll = function(force) {
      if (_.isNull(getAllDef) || force || (getAllDef && getAllDef.promise.$$state.status === 1)) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      // [BACKEND_ADVICE] Check cache and HTTP request logic
      if (cache.get('collection') && !force) {
        getAllDef.resolve(cache.get('collection'));
      } else {
        $http({
          method: 'GET',
          url: $config.API_URL + resource
        }).then(
          function success(response) {
            const data = response.data;
            cache.put('collection', data);
            getAllDef.resolve(data);
          },
          function error(errorResponse) {
            getAllDef.reject(errorResponse);
          }
        );
      }

      return getAllDef.promise;
    };

    return StatusService;
  });
