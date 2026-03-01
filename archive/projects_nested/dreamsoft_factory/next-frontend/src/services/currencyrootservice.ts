javascript
import { BackendAPI } from '@/lib/api';
import _ from 'lodash';

const CurrencyRootService = {};

const resource = 'currencyroot';
const cache = new Map();

let getAllDef = null;

CurrencyRootService.getAll = function (force) {
    if (_.isNull(getAllDef) || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
        getAllDef = BackendAPI.defer();
        // [BACKEND_ADVICE] Fetch currency root data from backend
        BackendAPI.get(resource).then(response => {
            cache.set('all', response.data);
            getAllDef.resolve(response.data);
        }).catch(error => {
            getAllDef.reject(error);
        });
    }
    return getAllDef.promise;
};

export default CurrencyRootService;
