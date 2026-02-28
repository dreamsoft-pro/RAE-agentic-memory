import axios from '@/lib/api';
import { TemplateVariablesService } from './templateVariablesService'; // Adjust import according to your project structure

class TemplateVariablesService {
    private readonly API_URL: string;

    constructor() {
        this.API_URL = process.env.NEXT_PUBLIC_API_URL; // Assuming you have an environment variable for API_URL
    }

    public async create(resource: string, data: any): Promise<any> {
        try {
            const response = await axios.post(`${this.API_URL}/${resource}`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response failed');
            }
        } catch (error) {
            throw error;
        }
    }

    public async edit(id: string | number, resource: string, data: any): Promise<any> {
        try {
            const response = await axios.put(`${this.API_URL}/${resource}/${id}`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response failed');
            }
        } catch (error) {
            throw error;
        }
    }
}

export default TemplateVariablesService;

// Usage example:
const service = new TemplateVariablesService();
service.create('your-resource', { /* your data */ })
  .then(response => console.log(response))
  .catch(error => console.error(error));

service.edit(1, 'your-resource', { /* your updated data */ })
  .then(response => console.log(response))
  .catch(error => console.error(error));