javascript
import { backendApi } from '@/lib/api';
import { createCache, CacheKey } from './cacheUtils';

const psIncreaseTypesCache = createCache(CacheKey.PS_INCREASE_TYPES);

function getAllPsIncreaseTypes(force) {
  return new Promise((resolve, reject) => {
    if (!force && psIncreaseTypesCache.get('collection')) {
      resolve(psIncreaseTypesCache.get('collection'));
    } else {
      backendApi.all('ps_increase_types')
        .getList()
        .then(response => {
          const collection = response.plain();
          psIncreaseTypesCache.put('collection', collection);
          if (force) {
            window.$rootScope.$emit('ps_increase_types', collection);
          }
          resolve(collection);
        })
        .catch(error => {
          reject(error);
        });
    }
  });
}

const PsIncreaseTypeService = {
  getAll: getAllPsIncreaseTypes,
};

export default PsIncreaseTypeService;
