javascript
import { API } from '@/lib/api';
import { LeanDesignAdvice } from '@/advice/lean-design';

export class PsPrintTypeWorkspaceService {
    static resource = 'ps_printTypeWorkspaces';

    static getAll(printTypeID, formatID) {
        return new Promise((resolve, reject) => {
            API.get(`${PsPrintTypeWorkspaceService.resource}/${printTypeID}?formatID=${formatID}`)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}

// [BACKEND_ADVICE] Heavy logic should be handled in the backend as per BACKEND-FIRST rule.
