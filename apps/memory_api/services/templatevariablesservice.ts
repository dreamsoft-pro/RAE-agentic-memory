javascript
import { apiGet } from '@/lib/api';

const resource = 'templateVariables';

export class TemplateVariablesService {
    static getAll() {
        return apiGet(`${resource}`);
    }

    static getTemplates() {
        return new Promise((resolve, reject) => {
            // [BACKEND_ADVICE] Add heavy logic here if needed
            $http({
                method: 'GET',
                url: $config.API_URL + `${resource}/templates`
            }).then(
                response => resolve(response.data),
                error => reject(error)
            );
        });
    }
}
