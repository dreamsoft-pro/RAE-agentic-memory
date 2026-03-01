javascript
import { BackendApi } from '@/lib/api';
import { createDeferred, rejectPromise, resolvePromise } from '@/utils/promiseHelpers';

export const ConfigService = {
    resetDomain: (force) => {
        // [BACKEND_ADVICE] This function should handle the logic to reset domain based on force flag
        return BackendApi.patch('resetDomain')
            .then((data) => resolvePromise(data))
            .catch((error) => rejectPromise(error));
    },

    createCompany: (form) => {
        // [BACKEND_ADVICE] This function should handle creating a company from form data
        return BackendApi.post('createCompany', form)
            .then((data) => resolvePromise(data))
            .catch((error) => rejectPromise(error));
    },
};
