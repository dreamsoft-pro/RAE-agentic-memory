javascript
'use strict';

import { BackendApi } from '@/lib/api';
import { createDeferredPromise } from '@/utils/promise';

angular.module('digitalprint.services')
    .service('SubCategoryDescriptionService', function ($q, $http, $config) {

        const SubCategoryDescriptionService = {};

        SubCategoryDescriptionService.getAll = (subcategoryURL) => {
            // [BACKEND_ADVICE] Heavy logic here
            const deferred = createDeferredPromise($q);
            BackendApi.get(`/subcategoriesDescriptions/subcategoriesDescriptionsPublic?categoryURL=${subcategoryURL}`)
                .then(data => {
                    deferred.resolve(data);
                })
                .catch(error => {
                    deferred.reject(error);
                });

            return deferred.promise;
        };

        return SubCategoryDescriptionService;
    });
