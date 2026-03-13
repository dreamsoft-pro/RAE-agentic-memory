javascript
'use strict';

import { BackendApi } from '@/lib/api';
import { CACHE_FACTORY } from '@/services/cache-factory';

const cacheFactory = new CACHE_FACTORY('ps_increases');
const backendApi = new BackendApi();

class IncreaseService {
    constructor(groupID, typeID) {
        this.groupID = groupID;
        this.typeID = typeID;
        this.resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_increases`;
    }

    getAll(typeID, force) {
        // [BACKEND_ADVICE] Fetch all increases based on the provided parameters.
        const cachedData = cacheFactory.get(`${this.resource}/${typeID}`);
        if (cachedData && !force) {
            return Promise.resolve(cachedData);
        }
        
        return backendApi.get(`${this.resource}/${typeID}`).then(response => {
            cacheFactory.put(`${this.resource}/${typeID}`, response.data);
            return response.data;
        });
    }
}

export default function PsIncreaseService() {
    return new IncreaseService;
}
