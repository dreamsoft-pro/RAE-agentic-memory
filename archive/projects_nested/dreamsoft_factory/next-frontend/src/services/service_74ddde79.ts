import api from '@/lib/api';

class OperationService {
    static setDevices(operation: any, devices: any): Promise<any> {
        return api.post(`${resource}/${operation.ID}/operationDevices`, devices)
            .then((response) => {
                if (response.data.response) {
                    return response.data;
                } else {
                    throw response.data;
                }
            })
            .catch((error) => {
                throw error;
            });
    }

    static processes(operation: any): Promise<any> {
        return api.get(`${resource}/${operation.ID}/processes`)
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                throw error;
            });
    }
}

// Assuming 'resource' is defined somewhere in the context or passed as a prop
let resource = ''; // Replace with actual logic to define resource

export default OperationService;