javascript
import { backendApiRequest as api } from '@/lib/api';
import _ from 'lodash';

const resource = 'discounts';
const cache = $cacheFactory(resource);
let getAllDef = null;

export const discountService = {
    getAll: (force) => {
        if (_.isNull(getAllDef) || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
            getAllDef = $q.defer();
            api.get(`${resource}`, { cache, force }).then(
                response => {
                    cache.put(resource, response.data);
                    getAllDef.resolve(response.data);
                },
                error => {
                    getAllDef.reject(error);
                }
            );
        }
        return getAllDef.promise;
    }
};

// [BACKEND_ADVICE] Heavy logic should be offloaded to backend services.
