javascript
import { BackendApi } from '@/lib/api';

angular.module('digitalprint.services')
  .factory('OperatorService', function($rootScope, $q, $http, $config, $cacheFactory) {
    const resource = 'operators';
    const cache = $cacheFactory(resource);
    
    let getAllDef = null;

    // [BACKEND_ADVICE] Heavy logic for fetching and caching operators.
    OperatorService.getAll = function(force) {
      if(_.isNull(getAllDef) || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      if(cache.get('collection') && !force) {
        getAllDef.resolve(cache.get('collection'));
      } else {
        BackendApi.get(resource)
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

    return OperatorService;
  });
