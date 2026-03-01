javascript
import { BackendApi } from '@/lib/api';

const AddressService = {};

AddressService.getResource = () => {
    return ['address', 'addressPublic'].join('/');
};

AddressService.getAll = (addresses) => {
    const deferred = $q.defer();

    const resource = this.getResource();
    
    // [BACKEND_ADVICE] Consider moving heavy logic to backend.
    BackendApi.get(addresses, resource)
        .then((data) => deferred.resolve(data))
        .catch((error) => deferred.reject(error));

    return deferred.promise;
};

AddressService.getForUser = () => {
    const deferred = $q.defer();

    const resource = ['address', 'getUserAddresses'].join('/');
    
    // [BACKEND_ADVICE] Consider moving heavy logic to backend.
    BackendApi.get(null, resource)
        .then((data) => deferred.resolve(data))
        .catch((error) => deferred.reject(error));

    return deferred.promise;
};

export default AddressService;
