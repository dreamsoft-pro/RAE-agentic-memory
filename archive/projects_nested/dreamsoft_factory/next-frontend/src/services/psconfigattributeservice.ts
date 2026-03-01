javascript
'use strict';

import { Restangular, $cacheFactory, $q } from '@/lib/api';
const resource = 'ps_attributes';

const cache = $cacheFactory.get('$default') || $cacheFactory('$default');

const PsConfigAttribute = {};

PsConfigAttribute.getAll = function (force) {
    return new Promise((resolve, reject) => {
        if (!force && cache.get('collection')) {
            resolve(cache.get('collection'));
        } else {
            Restangular.all(resource).getList().then(data => {
                const plainData = data.plain();
                cache.put('collection', plainData);
                resolve(plainData);
            }, error => {
                reject(error);
            });
        }
    });
};

export default PsConfigAttribute;
