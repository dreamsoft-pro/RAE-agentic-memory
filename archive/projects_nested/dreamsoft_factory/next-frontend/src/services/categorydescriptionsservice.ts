javascript
'use strict';

import { api } from '@/lib/api';
import { BACKEND_ADVICE } from './constants'; // Assuming a constants file for backend advice

const CategoryDescriptionsService = {};

const resource = getResource();

function getResource() {
    return 'categoriesDescriptions';
}

CategoryDescriptionsService.getAll = function (catID, lang) {
    const deferred = api.defer();
    api.get(`${api.config.API_URL}/${resource}?category_id=${catID}&lang=${lang}`)
        .then(response => {
            deferred.resolve(response.data);
        })
        .catch(error => {
            deferred.reject(error.response ? error.response.data : error.message);
        });

    return deferred.promise;
};

CategoryDescriptionsService.create = function (data, showLang) {
    const deferred = api.defer();
