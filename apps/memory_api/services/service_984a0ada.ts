import axios from '@/lib/api';
import { AxiosError } from 'axios';

class TypeDescriptionsService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public update(data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.put(`${process.env.API_URL}${this.resource}`, data)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }

    public getDescription(data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.get(`${process.env.API_URL}${this.resource}`, { params: data })
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}

export default TypeDescriptionsService;