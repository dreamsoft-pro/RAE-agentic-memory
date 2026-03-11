javascript
import { BackendApi } from '@/lib/api';

angular.module('digitalprint.services')
    .factory('PlanningService', function ($rootScope, $q, $http, $config, $cacheFactory) {
        
        const resource = 'schedule';
        const cache = $cacheFactory(resource);

        class PlanningService {

            getData(sort) {
                return new Promise((resolve, reject) => {
                    $http({
                        method: 'PATCH',
                        url: $config.API_URL + [resource, 'sort'].join('/'),
                        data: sort
                    }).success(responseData => {
                        resolve(responseData);
                    }).error(errorData => {
                        reject(errorData);
                    });
                });
            }
        }

        // [BACKEND_ADVICE] Consider moving the logic to the backend if it becomes complex.
        return new PlanningService();
    });
