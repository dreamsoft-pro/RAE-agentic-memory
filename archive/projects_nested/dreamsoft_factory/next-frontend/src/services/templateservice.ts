javascript
import { BackendApi } from '@/lib/api';

const resource = 'local_templates';

class TemplateService {
    static getAll() {
        return new Promise((resolve, reject) => {
            BackendApi.get(resource).then(
                response => resolve(response.data),
                error => reject(error)
            );
        });
    }

    static add(data) {
        const def = $q.defer();

        // [BACKEND_ADVICE] Consider moving heavy logic to the backend.
        $http({
            method: 'POST',
            url: $config.API_URL + resource,
            data: data
        }).success(function (data) {
            def.resolve(data);
        }).error(function (data, status) {
            def.reject({ data, status });
        });

        return def.promise;
    }
}

export default TemplateService;
