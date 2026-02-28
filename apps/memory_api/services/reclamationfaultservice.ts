javascript
import { BackendApi } from '@/lib/api';

const ReclamationFaultService = {};

const resource = 'dp_reclamation_faults';

ReclamationFaultService.getFaults = () => {
    return BackendApi.get(resource).then(
        (response) => response.data,
        (error) => Promise.reject(error)
    );
};

// [BACKEND_ADVICE] Add heavy logic here if necessary.
ReclamationFaultService.addFault = (data) => {
    const def = $q.defer();
    
    $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: data
    }).then(
        (response) => def.resolve(response.data),
        (error) => def.reject(error)
    );
    
    return def.promise;
};

export { ReclamationFaultService };
