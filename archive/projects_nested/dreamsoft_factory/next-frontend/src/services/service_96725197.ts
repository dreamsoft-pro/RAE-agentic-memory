import api from '@/lib/api';

class TypeService {
    static async getRealizationTimes(groupID: number, typeID: number, force?: boolean): Promise<any> {
        const resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_rt_details`;
        
        try {
            const response = await api.get(resource);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch realization times: ${error.message}`);
        }
    }

    static async setRealizationTime(groupID: number, typeID: number, item: any): Promise<void> {
        const resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_rt_details`;
        
        try {
            await api.post(resource, item);
        } catch (error) {
            throw new Error(`Failed to set realization time: ${error.message}`);
        }
    }
}

export default TypeService;