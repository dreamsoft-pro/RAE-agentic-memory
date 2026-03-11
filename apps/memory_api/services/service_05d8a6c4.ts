import api from '@/lib/api';

class LangRootService {

    private resource: string = 'langroot';

    public async getAll(): Promise<any> {
        try {
            const response = await api.get(this.resource);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async getEmpty(): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/showEmpty`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default new LangRootService();