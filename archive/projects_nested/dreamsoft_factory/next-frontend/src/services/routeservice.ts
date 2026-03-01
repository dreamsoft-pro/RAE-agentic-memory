javascript
import { backendApi } from '@/lib/api';
import $cacheFactory from 'ng-cache-factory';

angular.module('digitalprint.services')
  .factory('RouteService', function($rootScope, $q, $http, $config) {
    const resource = 'routes';
    const cache = $cacheFactory(resource);

    let getAllDef = null;

    const getAll = (force = false) => {
      if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      if (cache.get('collection') && !force) {
        getAllDef.resolve(cache.get('collection'));
      } else {
        backendApi($http, { method: 'GET', url: `${$config.API_URL}${resource}` })
          .then(data => {
            cache.put('collection', data);
            getAllDef.resolve(data);
          })
          .catch(error => {
            getAllDef.reject(error);
          });
      }

      return getAllDef.promise;
    };

    return { getAll };
  });

// [BACKEND_ADVICE] Consider refactoring the API call to a separate service for better maintainability.
