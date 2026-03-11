javascript
import { backendApi } from '@/lib/api';

angular.module('digitalprint.services')
    .factory('DpProductService', function ($q, $http, $config) {

        const DpProductService = {};

        const resource = 'dp_products';
        
        // [BACKEND_ADVICE] Heavy logic for fetching all products.
        DpProductService.getAll = () => {
            return backendApi.get(`${$config.API_URL}/${resource}`)
                .then(response => response.data)
                .catch(error => $q.reject(error));
        };

        // [BACKEND_ADVICE] Heavy logic for fetching base information of a product by id.
        DpProductService.baseInfo = (id) => {
            return backendApi.get(`${$config.API_URL}/${resource}/baseInfo/${id}`)
                .then(response => response.data)
                .catch(error => $q.reject(error));
        };

        return DpProductService;
    });
