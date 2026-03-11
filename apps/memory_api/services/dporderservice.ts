javascript
import { BackendApi } from '@/lib/api';

angular.module('digitalprint.services')
    .factory('DpOrderService', function ($q, $http, $config) {

        const DpOrderService = {};

        const resource = 'dp_orders';
        
        // [BACKEND_ADVICE] Consider moving heavy logic to backend services
        DpOrderService.getAll = () => {
            return new Promise((resolve, reject) => {
                $http({
                    method: 'GET',
                    url: $config.API_URL + resource
                }).then(response => resolve(response.data), error => reject(error));
            });
        };

        // [BACKEND_ADVICE] Consider moving heavy logic to backend services
        DpOrderService.get = (id) => {
            return new Promise((resolve, reject) => {
                $http({
                    method: 'GET',
                    url: $config.API_URL + [resource, id].join('/')
                }).then(response => resolve(response.data), error => reject(error));
            });
        };

        return DpOrderService;
    });
