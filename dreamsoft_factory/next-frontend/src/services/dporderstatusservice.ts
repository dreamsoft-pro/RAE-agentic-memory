javascript
import { ApiService } from '@/lib/api';

const DpOrderStatusService = {};

DpOrderStatusService.getAll = function(active) {
    const deferred = $q.defer();

    ApiService.get('dp_statuses/forClient')
        .then(response => {
            deferred.resolve(response.data);
        })
        .catch(error => {
            deferred.reject(error);
        });

    return deferred.promise;
};

export default DpOrderStatusService;
