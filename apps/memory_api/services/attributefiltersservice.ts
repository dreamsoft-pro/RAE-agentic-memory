javascript
import { axiosInstance } from '@/lib/api';

AttributeFiltersService.addAttributeOption = function (data) {
    const promise = axiosInstance.post($config.API_URL + 'attributeOption', data)
        .then(response => response.data)
        .catch(error => Promise.reject(error));

    return promise;
};

AttributeFiltersService.getRelativePapers = function (data) {
    const promise = axiosInstance.post($config.API_URL + 'getRelativePapers', data)
        .then(response => response.data)
        .catch(error => Promise.reject(error));

    return promise;
};
