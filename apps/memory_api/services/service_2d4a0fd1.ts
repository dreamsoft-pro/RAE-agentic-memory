import api from '@/lib/api';

class OperationService {

    private cache: any;
    private force?: boolean;

    constructor(cache: any, force?: boolean) {
        this.cache = cache;
        this.force = force;
    }

    public async getAll(resource: string): Promise<any> {
        if (this.cache.get('collection') && !this.force) {
            return this.cache.get('collection');
        } else {
            try {
                const response = await api.get($config.API_URL + resource);
                this.cache.put('collection', response.data);
                return response.data;
            } catch (error) {
                throw error;
            }
        }
    }

    public create(data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            api.post($config.API_URL + 'resource', data)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}

export default OperationService;