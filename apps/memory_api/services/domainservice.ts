javascript
import { BackendService } from '@/lib/api';
import _ from 'lodash';

const resource = 'domains';
const cache = new Map();

let getAllDef = null;

export const DomainService = {
    getAll: function (force) {
        if (_.isNull(getAllDef) || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
            getAllDef = BackendService.defer();
            // [BACKEND_ADVICE] Heavy logic should be handled here.
            BackendService.get(resource, {}, cache).then(
                response => {
                    getAllDef.resolve(response.data);
                },
                error => {
                    getAllDef.reject(error);
                }
            );
        } else {
            return getAllDef.promise;
        }
    }
};
