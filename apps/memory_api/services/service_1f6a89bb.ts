import api from '@/lib/api';

class GroupService {
    static async add(item: any): Promise<any> {
        try {
            const response = await api.post('ps_groups', item);
            if (response.data.ID) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    static async edit(item: any): Promise<any> {
        try {
            const response = await api.put('ps_groups', item);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    static async remove(item: any): Promise<void> {
        try {
            await api.delete(`ps_groups/${item.id}`);
        } catch (error) {
            throw error;
        }
    }
}

export default GroupService;