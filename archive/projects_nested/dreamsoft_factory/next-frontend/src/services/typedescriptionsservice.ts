javascript
'use strict';

import { Api } from '@/lib/api';
import { BACKEND_ADVICE } from './constants'; // [BACKEND_ADVICE]

const resourcePath = 'ps_typeDescriptions';

export const TypeDescriptionsService = {
    getAll: (groupID, typeID, lang) => {
        return new Promise((resolve, reject) => {
            Api.get(`${resourcePath}?tid=${typeID}&lang=${lang}`)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    },
    
    create: (data, showLang) => {
        return new Promise((resolve, reject) => {
            // [BACKEND_ADVICE] Heavy logic should be moved to backend.
            Api.post(resourcePath, data)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
};
