import api from '@/lib/api';
import { Cache } from 'path-to-your-cache-module'; // Assuming you have a cache module

class OperatorService {
    private resource: string;
    private url: string;

    constructor(resource: string) {
        this.resource = resource;
        this.url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
    }

    async create(data: any): Promise<any> {
        try {
            const response = await api.post(this.url, data);
            if (response.data.ID) {
                Cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    async update(module: any): Promise<any> {
        try {
            const response = await api.put(this.url, module);
            if (response.data.response) {
                Cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    async remove(id: string): Promise<any> {
        try {
            await api.delete(`${this.url}/${id}`);
            Cache.remove('collection');
        } catch (error) {
            throw error;
        }
    }
}

export default OperatorService;

// Usage Example:
const operator = new OperatorService('your-resource-name');

operator.create({ /* your data */ })
  .then(data => console.log(data))
  .catch(error => console.error(error));

operator.update({ /* your module */ })
  .then(data => console.log(data))
  .catch(error => console.error(error));

operator.remove('123')
  .then(() => console.log('Removed'))
  .catch(error => console.error(error));