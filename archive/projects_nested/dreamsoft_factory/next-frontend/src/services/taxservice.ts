javascript
import { BackendApi } from '@/lib/api';
import _ from 'lodash';

const TaxService = {};

const resource = 'tax';

TaxService.getAll = function (force) {
    // [BACKEND_ADVICE] Heavy logic for fetching all tax data should be handled here.
    if (_.isNull(TaxService.getAllDef) || force || TaxService.getAllDef.promise.$$state.status === 1) {
        TaxService.getAllDef = $q.defer();
    } else {
        return TaxService.getAllDef.promise;
    }
};

BackendApi.register('TaxService', resource, (force) => TaxService.getAll(force));

export { TaxService };
