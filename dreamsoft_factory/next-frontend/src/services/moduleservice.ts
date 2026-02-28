javascript
import { BackendApi } from '@/lib/api';
import _ from 'lodash';

const ModuleService = {};

const resource = 'modules';
const cache = $cacheFactory(resource);

let getAllDef = null;

ModuleService.getAll = function (force) {
    if (_.isNull(getAllDef) || force || (getAllDef && getAllDef.promise.$$state.status === 1)) {
        getAllDef = $q.defer();
        const fetchModules = () => BackendApi.get(resource).then(response => response.data);
        fetchModules().then(data => {
            cache.put(resource, data);
            getAllDef.resolve(data);
        }).catch(error => {
            getAllDef.reject(error);
        });
    }
    return getAllDef ? getAllDef.promise : $q.when([]);
};

export { ModuleService };
