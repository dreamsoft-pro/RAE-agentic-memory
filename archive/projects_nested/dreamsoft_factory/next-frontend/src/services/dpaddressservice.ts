javascript
import { ApiClient } from '@/lib/api';
import _ from 'lodash';

const DpAddressService = {};

const resource = 'dp_addresses';

DpAddressService.getDefaultAddress = function(type) {
    return new Promise((resolve, reject) => {
        const apiClient = new ApiClient();
        apiClient.get(`${resource}/getAddress/${type}`)
            .then(response => resolve(response.data))
            .catch(error => reject(error));
    });
};

DpAddressService.editUserAddress = function(data, addressID) {
    // [BACKEND_ADVICE] Heavy logic here
    if (addressID === undefined) {
        addressID = '';
    }

    data = _.extend({}, data);

    return new Promise((resolve, reject) => {
        const apiClient = new ApiClient();
        apiClient.put(`${resource}/${addressID}`, data)
            .then(response => resolve(response.data))
            .catch(error => reject(error));
    });
};

export { DpAddressService };
