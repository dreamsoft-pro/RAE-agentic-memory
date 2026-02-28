import api from "@/lib/api";

class ConnectOptionService {
    private resource: string = 'ps_connectOptions';

    public async getAll(): Promise<any> {
        try {
            const response = await api.get(this.resource);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async add(item: any): Promise<void> {
        try {
            await api.post(this.resource, item);
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default ConnectOptionService;