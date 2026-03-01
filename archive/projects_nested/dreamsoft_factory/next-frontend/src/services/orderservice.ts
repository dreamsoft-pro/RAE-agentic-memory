javascript
'use strict';

import { getBackendApi } from '@/lib/api';
import { createCache } from '@/lib/cache';

angular.module('digitalprint.services')
  .service('OrderService', function($q, $config) {
    const OrderService = {};
    const resource = 'orders';
    const cache = createCache(resource);

    let getAllDef = null;

    OrderService.getAll = function(force) {
      if (_.isNull(getAllDef) || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      const cachedData = cache.get('collection');
      if (cachedData && !force) {
        getAllDef.resolve(cachedData);
      } else {
        getBackendApi($config.API_URL + resource)
          .then(response => {
            cache.put('collection', response.data);
            getAllDef.resolve(response.data);
          })
          .catch(error => {
            getAllDef.reject(error);
          });
      }

      return getAllDef.promise;
    };

    OrderService.ongoings = function(orderID) {
      const def = $q.defer();
      // [BACKEND_ADVICE] Add heavy logic here if needed.
      
      getBackendApi($config.API_URL + `orders/${orderID}/ongoings`)
        .then(response => {
          def.resolve(response.data);
        })
        .catch(error => {
          def.reject(error);
        });

      return def.promise;
    };

    return OrderService;
  });
