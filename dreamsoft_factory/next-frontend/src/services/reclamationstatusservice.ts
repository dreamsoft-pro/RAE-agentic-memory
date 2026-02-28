javascript
import { BackendApi } from '@/lib/api';

const ReclamationStatusService = {};

const resource = 'dp_reclamations_statuses';

ReclamationStatusService.getAll = (active) => {
    const uriParts = [resource];
    if (active !== undefined) {
        uriParts.push('1');
    }
    const url = `${BackendApi.BASE_URL}/${uriParts.join('/')}`;

    return BackendApi.get(url).then(
        (data) => data,
        (error) => Promise.reject(error)
    );
};

ReclamationStatusService.add = (data) => {
    // [BACKEND_ADVICE] Add the logic to handle adding a new reclamation status
    const url = `${BackendApi.BASE_URL}/${resource}`;
    
    return BackendApi.post(url, data).then(
        (response) => response,
        (error) => Promise.reject(error)
    );
};
