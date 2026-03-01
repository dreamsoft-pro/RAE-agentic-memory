javascript
import { BackendService } from '@/lib/api';
import _ from 'lodash';

const LangSettingsRootService = {};

const resource = 'langsettingsroot';
const cache = $cacheFactory(resource);

let getAllDef = null;

LangSettingsRootService.getAll = function (force) {
    if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
        BackendService.get(`${resource}`, { cache: !force })
            .then(response => {
                cache.put(resource, response.data);
                getAllDef.resolve(response.data);
            })
            .catch(error => {
                getAllDef.reject(error);
            });
    }
    return getAllDef.promise;
};

export default LangSettingsRootService;
