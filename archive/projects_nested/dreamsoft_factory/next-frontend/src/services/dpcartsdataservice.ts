javascript
import { apiGet, apiPost } from '@/lib/api';

angular.module('digitalprint.services')
    .factory('DpCartsDataService', function ($q, $http, $config) {

        const DpCartsDataService = {};

        const resource = 'dp_carts_data';

        // [BACKEND_ADVICE] Consider moving heavy logic to the backend.
        DpCartsDataService.get = (id) => apiGet(`${$config.API_URL}/${resource}/${id}`);

        DpCartsDataService.add = (carts) => apiPost($config.API_URL + resource, carts);

        return DpCartsDataService;
    });
