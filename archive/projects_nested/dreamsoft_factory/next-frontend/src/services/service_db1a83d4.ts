import api from "@/lib/api";

class DpStatusService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async post(data: any): Promise<any> {
        try {
            const response = await api.post(`${$config.API_URL}/${this.resource}`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response error');
            }
        } catch (error) {
            throw error;
        }
    }

    public async update(data: any): Promise<any> {
        try {
            const response = await api.put(`${$config.API_URL}/${this.resource}`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response error');
            }
        } catch (error) {
            throw error;
        }
    }

}