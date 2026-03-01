javascript
'use strict';

import Restangular from '@lib/api/restangular';
import { API_URL } from '@config/environment';
import { cacheFactory, defer } from '@lib/utils/qExtensions';
import PsPricelistService from './PsPricelistService';
import PsPrintTypeService from './PsPrintTypeService';
import PsWorkspaceService from './PsWorkspaceService';

const cache = cacheFactory('ps_options');

class PsConfigOption {
    constructor(attrID) {
        this.attrID = attrID;
    }

    getResource() {
        return `ps_attributes/${this.attrID}/ps_options`;
    }

    getUploadUrl() {
        const resource = `${this.getResource()}/uploadIcon`;
        return `${API_URL}${resource}`;
    }

    getAll(force = false) {
        const def = defer();
        const resource = this.getResource();

        // [BACKEND_ADVICE] Heavy logic should be here
        Restangular.one(resource).get({ force }).then(
            (data) => {
                cache.put(this.attrID, data);
                def.resolve(data);
            },
            (error) => {
                def.reject(error);
            }
        );

        return def.promise;
    }
}

export default PsConfigOption;
