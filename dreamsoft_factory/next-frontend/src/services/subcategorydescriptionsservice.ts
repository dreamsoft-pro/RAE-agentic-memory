javascript
'use strict';

import { BackendApi } from '@/lib/api';
import { BACKEND_ADVICE } from './constants'; // Assuming a constants file for backend advice

const SubcategoryDescriptionsService = {};

// [BACKEND_ADVICE] - Resource name should be configurable or dynamic based on requirements.
function getResource() {
    return 'subcategoriesDescriptions';
}

SubcategoryDescriptionsService.getAll = (catID, lang) => {
    const api = new BackendApi();
    const url = `${api.getBaseUrl()}${getResource()}?subcategory_id=${catID}&lang=${lang}`;

    return api.get(url).then(
        (data) => data,
        (error) => Promise.reject(error)
    );
};

SubcategoryDescriptionsService.create = (data, showLang) => {
    const def = Promise.defer();
