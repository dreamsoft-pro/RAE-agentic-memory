javascript
import { createApiCall } from '@/lib/api';

DpStatusService.update = function (data) {
    const def = $q.defer();

    createApiCall('PUT', `${$config.API_URL}${resource}`, data)
        .then(response => {
            if (response.response) {
                def.resolve(response);
            } else {
                def.reject(response);
            }
        })
        .catch(error => {
            def.reject(error);
        });

    return def.promise;
};
