javascript
import { api } from '@/lib/api';

const ReclamationService = {};

const faultsResource = 'dp_reclamation_faults';
const resource = 'dp_reclamations';
const messagesResource = 'dp_reclamations_messages';

// [BACKEND_ADVICE] Fetching faults data
ReclamationService.getFaults = () => {
    return api.get(`${faultsResource}`)
        .then(response => response.data)
        .catch(error => Promise.reject(error));
};

ReclamationService.getUploadUrl = (reclamationID) => {
    // [BACKEND_ADvice] Construct the URL for file upload
    return `${resource}/files/${reclamationID}`;
};
