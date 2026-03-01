javascript
import { BackendService } from '@/lib/api';
import _ from 'lodash';

const resource = 'devices';

export const DeviceService = {
    getAll: function(force) {
        if (_.isNull(this.getAllDef) || force || this.getAllDef.promise.$$state.status === 1) {
            this.getAllDef = Promise.defer();
        } else {
            return this.getAllDef.promise;
        }

        BackendService.get(resource)
            .then((data) => {
                cache.put('collection', data);
                this.getAllDef.resolve(data);
            })
            .catch((error) => {
                this.getAllDef.reject(error);
            });

        return this.getAllDef.promise;
    }
};

const cache = $cacheFactory(resource);

DeviceService.getAllDef = null; // Initialize deferred object
