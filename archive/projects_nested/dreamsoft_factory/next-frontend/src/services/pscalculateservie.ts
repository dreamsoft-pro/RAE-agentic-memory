javascript
'use strict';

import { BackendApi } from '@/lib/api';
import { CACHE_FACTORY } from '@/lib/cache';

const cacheFactory = CACHE_FACTORY('ps_calculate');

class CalculateService {
    constructor(groupID, typeID) {
        this.groupID = groupID;
        this.typeID = typeID;
        this.resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_calculate`;
    }

    request(method, endpoint, data) {
        const def = Promise.defer();
        const url = `${process.env.API_URL}${this.resource}${endpoint ? '/' + endpoint : ''}`;
        
        // [BACKEND_ADVICE] Heavy logic should be handled in the backend.
        BackendApi.request(method, url, data)
            .then(response => {
                cacheFactory.remove(this.resource);  // Invalidate cache on request
                def.resolve(response.data);
            })
            .catch(error => {
                def.reject(error);
            });

        return def.promise;
    }
}

export default CalculateService;
