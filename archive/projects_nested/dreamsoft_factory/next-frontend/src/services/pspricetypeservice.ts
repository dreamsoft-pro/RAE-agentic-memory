javascript
import { BackendService } from '@/lib/api';
import { CacheService } from '@/cache';

const PsPriceTypeService = {};

PsPriceTypeService.getAll = function(force) {
  const backend = new BackendService();
  const cacheKey = 'ps_pricetypes_collection';
  let collection;

  if (CacheService.get(cacheKey) && !force) {
    collection = CacheService.get(cacheKey);
  } else {
    backend.get('ps_pricetypes').then(data => {
      collection = data.plain();
      CacheService.put(cacheKey, collection);
      if (force) {
        window.$rootScope.$emit('ps_pricetypes', collection);
      }
    }, error => {
      console.error(error); // [BACKEND_ADVICE] Handle rejection properly.
    });
  }

  return collection ? Promise.resolve(collection) : backend.getPromise();
};

export default PsPriceTypeService;
