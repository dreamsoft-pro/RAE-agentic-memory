import api from '@/lib/api';

class ModuleValueService {
    resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async fetch(params?: any): Promise<any> {
        try {
            const response = await api.get(`${$config.API_URL}${this.resource}`, { params });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async update(courier: any): Promise<any> {
        try {
            const response = await api.patch(`${$config.API_URL}${this.resource}`, courier);
            if ('response' in response.data) {
                cache.remove(this.module); // assuming `cache` and `module` are defined elsewhere
                return response.data;
            } else {
                throw response.data; // reject the promise with error data
            }
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    get module(): string {
        // Implement or define this property as per your application logic.
        return 'defaultModuleValue';
    }
}