javascript
import { BackendApi } from '@/lib/api';
import CacheService from './CacheService';

const resource = 'module_types';

class ModuleTypeService {
  constructor() {
    this.cacheResolve = new CacheService('module_types');
  }

  getAll() {
    return this.cacheResolve.doRequest(resource).then(data => {
      window.$rootScope.$emit('ModuleTypeService.getAll', data);
      return data;
    }).catch(error => {
      throw error;
    });
  }
}

// [BACKEND_ADVICE] Consider moving heavy logic to backend if necessary.

export default ModuleTypeService;
