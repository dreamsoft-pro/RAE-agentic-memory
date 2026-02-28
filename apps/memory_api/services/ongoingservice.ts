javascript
import { apiRequest } from '@/lib/api';

const OngoingService = {};

const resource = 'ongoings';

OngoingService.patchOngoings = (ongoingID, data) => {
    return apiRequest({
        method: 'PATCH',
        url: `${resource}/${ongoingID}`,
        data: data
    }).then(response => response.data.response ? Promise.resolve(response.data) : Promise.reject(response.data))
      .catch(error => Promise.reject(error));
};

OngoingService.ongoingsLogs = (ongoingID, isAdditional) => {
    const def = $q.defer();

    // [BACKEND_ADVICE] Add heavy logic if necessary.
    $http({
        method: 'GET',
        url: `${$config.API_URL}/${resource}/${ongoingID}/logs`,
        params: { additional: isAdditional }
    }).success(responseData => {
        def.resolve(responseData);
    }).error(errorData => {
        def.reject(errorData);
    });

    return def.promise;
};

export default OngoingService;
