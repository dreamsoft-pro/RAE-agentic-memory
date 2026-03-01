javascript
'use strict';

import { backendApi } from '@/lib/api';
import { $cacheFactory, $q } from 'angular';

const resource = 'ps_attributetypes';
const cache = $cacheFactory(resource);

export const PsConfigAttributeTypeService = {
    getAll: function (force) {
        const def = $q.defer();

        if (!force && cache.get('collection')) {
            def.resolve(cache.get('collection'));
        } else {
            backendApi
                .getBackendResource(resource)
                .getList()
                .then((data) => {
                    cache.put('collection', data.plain());
                    def.resolve(data);
                })
                .catch((errorData) => {
                    def.reject(errorData);
                });
        }

        return def.promise;
    },
};
