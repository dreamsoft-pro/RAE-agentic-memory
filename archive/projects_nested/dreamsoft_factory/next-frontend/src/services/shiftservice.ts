javascript
import { backendApi } from '@/lib/api';
import $cacheFactory from 'ng-cache';

const resource = 'shifts';
const deviceResource = 'deviceShift';
const cache = $cacheFactory(resource);

function ShiftService($rootScope, $q, $http, $config) {
    let getAllDef = null;

    const getAll = (force = false) => {
        if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
            getAllDef = $q.defer();
        } else {
            return getAllDef.promise;
        }

        backendApi($http, 'GET', `${$config.API_URL}${resource}`)
            .then((data) => {
                cache.put('collection', data);
                getAllDef.resolve(data);
            })
            .catch((error) => {
                getAllDef.reject(error);
            });

        return getAllDef.promise;
    };

    return { getAll };
}

export default ShiftService;
