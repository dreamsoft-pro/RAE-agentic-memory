javascript
import { BackendApi } from '@/lib/api';
import { CacheService } from '@/services/cache';

const PsConfigIncreaseTypeService = {};

PsConfigIncreaseTypeService.getAll = function(force) {
  const def = Promise.resolve();

  // BACKEND_ADVICE: Heavy logic in fetching and caching data.
  if (CacheService.get('ps_config_increaseTypes') && !force) {
    return Promise.resolve(CacheService.get('ps_config_increaseTypes'));
  } else {
    BackendApi.psConfigIncreaseTypes.getList().then(data => {
      const collection = data.plain();
      CacheService.put('ps_config_increaseTypes', collection);
      if (force) {
        window.$rootScope.$emit('ps_config_increaseTypes', collection);
      }
      def.resolve(collection);
    }, error => {
      def.reject(error);
    });
  }

  return def.promise;
};

export { PsConfigIncreaseTypeService };
