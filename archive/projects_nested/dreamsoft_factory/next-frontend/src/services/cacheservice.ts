javascript
import { BackendAPI } from '@/lib/api';

class CacheService {
    constructor($config) {
        this.$config = $config;
    }

    doRequest(restangularPromise, options, method) {
        const defer = restangularPromise || new Promise((resolve, reject) => resolve());
        let url;

        if (options && options.url) {
            url = options.url;
        } else {
            url = this.$config.API_URL + '/' + method;
        }

        return BackendAPI.request({
            method: 'GET',
            url,
            successCallback: data => onSuccess(method, data),
            errorCallback: onError
        }).then(responseData => {
            return responseData;
        });
    }

    // [BACKEND_ADVICE] Implement onSuccess and onError methods as per application logic.
    onSuccess(defer, data) {
        // Implementation here
    }

    onError(error) {
        // Error handling implementation here
    }

    getList(restangularPromise, options) {
        return this.doRequest(restangularPromise, options, 'getList');
    }

    get(restangularPromise, options) {
        return this.doRequest(restangularPromise, options, 'get');
    }
}

export default CacheService;
