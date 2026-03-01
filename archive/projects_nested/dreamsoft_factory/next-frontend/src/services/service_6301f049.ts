import api from '@/lib/api';

class PauseService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async post(data: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}/${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    async update(module: any): Promise<any> {
        try {
            const response = await api.put(`${process.env.API_URL}/${this.resource}`, module);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    async updateReportSheets(data: any): Promise<void> {
        try {
            await this.post(data);  // Assuming post and updateReportSheets are similar
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}

export default PauseService;

// Usage example in a Next.js page or component:
// const pauseService = new PauseService('your-resource-name');