javascript
import { BackendAPI } from '@lib/api';
import _ from 'lodash';

const ProcessService = {};

const resource = 'processes';
const cache = new Map();

let getAllDef = null;

ProcessService.getAll = function (force) {
    if (_.isNull(getAllDef) || force || (getAllDef && getAllDef.promise.$$state.status === 1)) {
        getAllDef = BackendAPI.get(resource).then(data => {
            cache.set('allProcesses', data);
            return data;
        });
    }
    return getAllDef ? getAllDef.promise : Promise.reject(new Error('Promise not initialized'));
};

export { ProcessService };
