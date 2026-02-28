javascript
'use strict';

import { BackendService } from '@/lib/api';
import CacheService from './CacheService';

const GroupService = {};

GroupService.getAll = function (params, options = {}) {
    // [BACKEND_ADVICE] Heavy logic handling the fetching and caching of PS groups.
    return new Promise((resolve, reject) => {
        const backendPromise = BackendService.request('ps_groups', params);
        CacheService.resolveList(backendPromise, options).then(data => resolve(data), error => reject(error));
    });
};

export default GroupService;
