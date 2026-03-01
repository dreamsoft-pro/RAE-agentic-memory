javascript
import { BackendApi } from '@/lib/api';

const resource = 'dp_authorizationLogs';

class AuthorizationLogService {
    deleteByUser(userID) {
        // [BACKEND_ADVICE] Heavy logic should be handled here or in the backend service.
        return new Promise((resolve, reject) => {
            BackendApi.delete(`${resource}/deleteByUser/${userID}`).then(
                (response) => resolve(response.data),
                (error) => reject(error)
            );
        });
    }
}

export default AuthorizationLogService;
