javascript
'use strict';

const api = require('@/lib/api');
const { createDeferred } = require('@/lib/utils');

angular.module('digitalprint.services')
    .service('PsTypeDescriptionService', function ($q, $http, $config) {

        const TypeDescriptionService = {};

        TypeDescriptionService.getAll = (groupID, typeID) => {
            // [BACKEND_ADVICE] Consider moving this logic to the backend if it becomes complex.
            const deferred = createDeferred($q);
            $http({
                method: 'GET',
                url: api.buildUrl('ps_typeDescriptions/typeDescriptionsPublic', { groupID, typeID }, $config.API_URL)
            }).then(
                (response) => {
                    deferred.resolve(response.data);
                },
                (error) => {
                    deferred.reject(error);
                }
            );

            return deferred.promise;
        };

        return TypeDescriptionService;
    });
