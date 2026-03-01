import api from '@/lib/api';

class TypeService {
    static async update(groupID: string | number, item: any): Promise<any> {
        try {
            const response = await api.put(`ps_groups/${groupID}/ps_types`, item);
            if (response.data.response) {
                cache.remove(`collection${groupID}`);
                return response.data;
            } else {
                throw new Error('Failed to update resource');
            }
        } catch (error) {
            throw error;
        }
    }

    static async remove(groupID: string | number, item: any): Promise<void> {
        try {
            await api.delete(`ps_groups/${groupID}/ps_types`, { data: item });
            cache.remove(`collection${groupID}`);
        } catch (error) {
            throw error;
        }
    }
}