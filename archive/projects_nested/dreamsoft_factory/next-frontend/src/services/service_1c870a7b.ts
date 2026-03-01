import api from '@/lib/api';

class ConnectOptionService {
    private resource: string = 'your-resource-name'; // Define your resource here

    public async add(item: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}/${this.resource}`, item);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    public async edit(item: any): Promise<any> {
        try {
            const response = await api.put(`${process.env.API_URL}/${this.resource}`, item);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }
}

export default ConnectOptionService;