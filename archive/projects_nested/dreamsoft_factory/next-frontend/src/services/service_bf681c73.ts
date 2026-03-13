import api from '@/lib/api';

class DeviceService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async update(module: any): Promise<any> {
        try {
            const response = await api.put(`${process.env.API_URL}${this.resource}`, module);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    public async updateEfficiency(data: any): Promise<any> {
        try {
            const response = await api.put(`${process.env.API_URL}${this.resource}/deviceEfficiency`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    public async remove(id: string): Promise<any> {
        try {
            const response = await api.delete(`${process.env.API_URL}${this.resource}/${id}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}

export default DeviceService;