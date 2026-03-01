javascript
'use strict';

import { BackendService } from '@/lib/api';
const resource = getResource();

class TypeDescriptionsFormatsService {
    static getAll(descID) {
        return new Promise((resolve, reject) => {
            BackendService.get(`${resource}?dID=${descID}`)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }

    static setFormats(descID, formats) {
        const postData = { descID, formats };
        return new Promise((resolve, reject) => {
            BackendService.post(resource, postData)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}

function getResource() {
    return 'ps_typeDescriptionsFormats';
}

export default TypeDescriptionsFormatsService;
