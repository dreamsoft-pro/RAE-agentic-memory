javascript
import { BackendApi } from '@/lib/api';
import { CACHE_KEY_MODULE_VALUE } from '@/constants/cacheKeys';

const cache = {}; // Simulate $cacheFactory

class ModuleValueService {
    constructor(module) {
        this.module = module;
        this.resource = ['modules', this.module, 'module_values'].join('/');
        this.getAllDef = null; // [BACKEND_ADVICE]
    }

    getAll(force) {
        if (!this.getAllDef || force) {
            this.getAllDef = { promise: BackendApi.get(this.resource).then(response => response.data) };
            cache[CACHE_KEY_MODULE_VALUE] = this.getAllDef.promise;
        }
        return cache[CACHE_KEY_MODULE_VALUE];
    }
}

export default function ModuleValueServiceFactory($rootScope, $q, $http, $config, $cacheFactory) {
    const serviceInstance = new ModuleValueService('defaultModule'); // Placeholder for actual module
    return serviceInstance;
}
