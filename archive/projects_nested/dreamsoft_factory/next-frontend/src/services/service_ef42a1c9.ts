import api from '@/lib/api';

class GroupService {
    static async removeGroupItem(itemID: string): Promise<void> {
        try {
            const response = await api.delete(`ps_groups/${itemID}`);
            if (response.data) {
                return;
            } else {
                throw new Error('Failed to delete group item');
            }
        } catch (error) {
            throw error;
        }
    }

    static async getRealizationTimes(groupID: string, force?: boolean): Promise<any[]> {
        const resource = `ps_groups/${groupID}/ps_rt_details`;
        try {
            const response = await api.get(resource);
            return response.data || [];
        } catch (error) {
            throw error;
        }
    }
}

export default GroupService;