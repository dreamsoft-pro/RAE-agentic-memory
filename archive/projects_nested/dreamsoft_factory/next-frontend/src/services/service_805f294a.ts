import api from '@/lib/api';

export default class DepartmentService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async create(data: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}/${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async update(module: any): Promise<any> {
        try {
            const response = await api.put(`${process.env.API_URL}/${this.resource}`, module);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async remove(id: string): Promise<void> {
        try {
            await api.delete(`${process.env.API_URL}/${this.resource}/${id}`);
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}