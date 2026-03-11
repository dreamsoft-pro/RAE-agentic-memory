javascript
import { BackendApi } from '@/lib/api';

const LabelImpositionService = {};

LabelImpositionService.getForType = function (typeID) {
    // [BACKEND_ADVICE] Heavy logic should be handled in the backend.
    return new Promise((resolve, reject) => {
        BackendApi.get(`labelImposition/${typeID}`)
            .then(response => resolve(response.data))
            .catch(errorResponse => reject(errorResponse));
    });
};

export { LabelImpositionService };
