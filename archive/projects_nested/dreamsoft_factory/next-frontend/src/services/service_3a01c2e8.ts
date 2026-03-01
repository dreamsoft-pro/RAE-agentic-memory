import api from '@/lib/api';

class GroupService {

    static async setRealizationTime(groupID: string, item: any): Promise<any> {
        const resource = `ps_groups/${groupID}/ps_rt_details`;

        try {
            const response = await api.patch(resource, item);
            if (response.data.response) {
                return response;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error;
        }
    }

    static async removeRealizationTime(groupID: string, item: any): Promise<void> {
        const resource = `ps_groups/${groupID}/ps_rt_details`;

        if (!item.details) {
            throw new Error('Details are required');
        }

        try {
            await api.delete(resource);
        } catch (error) {
            throw error;
        }
    }
}