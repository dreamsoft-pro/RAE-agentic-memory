javascript
import { BackendApi } from '@/lib/api';
import $cacheFactory from 'ng-cache';

class SettingService {
    constructor(module) {
        this.module = module;
        resource = ['settings', this.module].join('/');
    }

    setModule(module) {
        this.module = module;
    }

    getPublicSettings() {
        const def = Promise.defer();
        const cacheKey = `getPublicSettings:${this.module}`;

        BackendApi.get('settings/getPublicSettings/' + this.module, { cache: $cacheFactory.get(cacheKey) })
            .then(data => {
                def.resolve(data);
            }, data => {
                def.reject(data);
            });

        return def.promise;
    }
}

// [BACKEND_ADVICE] Heavier logic should be moved to the backend as per LEAN DESIGN principle.
export default function SettingServiceFactory($rootScope, $config) {
    return new SettingService('defaultModule');
}
