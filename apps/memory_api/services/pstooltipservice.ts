javascript
'use strict';

import { BackendService } from '@/lib/api';
import { CacheManager } from '@/utils/cache-manager'; // Assuming a cache manager utility

const DEFAULT_CACHE_KEY = 'ps_tooltips';

class TooltipService {
    constructor(groupID, typeID) {
        this.groupID = groupID;
        this.typeID = typeID;
        this.resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_tooltips`;
    }

    getAll(force = false) {
        const cacheKey = this.resource;

        if (!force && CacheManager.has(cacheKey)) {
            return $q.resolve(CacheManager.get(cacheKey));
        } else {
            BackendService.get(this.resource).then(data => {
                CacheManager.put(cacheKey, data.plain());
                $q.resolve(data.plain());
            }, error => {
                $q.reject(error);
            });
        }
    }
}

angular.module('digitalprint.services').factory('PsTooltipService', TooltipService);

// [BACKEND_ADVICE] Consider refactoring getAll to use backend service directly for better separation of concerns.
