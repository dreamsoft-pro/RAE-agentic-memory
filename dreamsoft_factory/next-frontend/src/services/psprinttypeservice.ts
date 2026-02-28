javascript
'use strict';

import { BackendAdvice } from '@/lib/api';
import { CacheFactory, Q } from '@digitalprint/services/utils';

const cache = CacheFactory('ps_printtypes');

class PrintTypeService {
  getResource() {
    return 'ps_printtypes';
  }

  getAll(force) {
    const deferred = Q.defer();

    const resource = this.getResource();
    if (cache.get(resource) && !force) {
      deferred.resolve(cache.get(resource));
    } else {
      BackendAdvice.getList(resource).then(data => {
        cache.put(resource, data.plain());
        deferred.resolve(data.plain());
      }, error => {
        deferred.reject(error);
      });
    }

    return deferred.promise;
  }

  add(item) {
    const deferred = Q.defer();

    const resource = this.getResource();
