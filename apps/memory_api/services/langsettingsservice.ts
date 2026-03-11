javascript
import { BackendAPI } from '@/lib/api';
import _ from 'lodash';

const resource = 'langsettings';

// [BACKEND_ADVICE] Cache and deferred logic moved to backend-first pattern.
export const LangSettingsService = {
    getAll: (force = false) => {
        if (_.isNull(LangSettingsService.getAllDef) || force || (LangSettingsService.getAllDef.promise.$$state && LangSettingsService.getAllDef.promise.$$state.status === 1)) {
            LangSettingsService.getAllDef = BackendAPI.defer();
        } else {
            return LangSettingsService.getAllDef.promise;
        }
        
        BackendAPI.get(resource).then((response) => {
            cache.put(resource, response.data);
            if (_.isNull(LangSettingsService.getAllDef)) {
                LangSettingsService.getAllDef.resolve(response.data);
            }
        }).catch((error) => {
            if (_.isNull(LangSettingsService.getAllDef)) {
                LangSettingsService.getAllDef.reject(error);
            }
        });
        
        return LangSettingsService.getAllDef.promise;
    }
};

// [BACKEND_ADVICE] Cache management is handled in backend.
const cache = BackendAPI.cacheFactory(resource);

export default LangSettingsService;
