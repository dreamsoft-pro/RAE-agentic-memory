javascript
import { BackendApi } from '@/lib/api';

angular.module('digitalprint.services')
    .service('CustomProductService', function ($q, $http, $config) {
        const resource = 'dp_customProducts';
        const api = new BackendApi($http, $config.API_URL);

        const CustomProductService = {};

        CustomProductService.getUploadUrl = (customProductID) => {
            return `${$config.API_URL}/${resource}/files/${customProductID}`;
        };

        CustomProductService.add = (data) => {
            const def = $q.defer();

            api.post(resource, data)
                .then((response) => {
                    def.resolve(response.data);
                })
                .catch((error) => {
                    def.reject(error);
                });

            return def.promise;
        };

        // [BACKEND_ADVICE] Consider moving heavy logic to the backend.

        return CustomProductService;

    });
