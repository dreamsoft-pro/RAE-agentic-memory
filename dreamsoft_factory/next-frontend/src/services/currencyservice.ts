javascript
import { getApi } from '@/lib/api';
import _ from 'lodash';

const CurrencyService = {};

const resource = 'currency';
const cache = $cacheFactory(resource);
let getAllDef = null;

CurrencyService.getAll = function (force) {
    if (_.isNull(getAllDef) || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
        getAllDef = $q.defer();
        
        getApi(`${$config.apiUrl}/${resource}`)
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

export default CurrencyService;
