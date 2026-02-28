import api from '@/lib/api';

export default class GroupService {

    static async get(id: number): Promise<any> {
        try {
            const response = await api.get(`ps_groups/${id}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async getOneForView(url: string): Promise<any> {
        try {
            const response = await api.get(`ps_groups/getOneForView/${url}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async add(item: any): Promise<any> {
        try {
            const response = await api.post('ps_groups', item);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}