import api from '@/lib/api';

export default class ModuleService {
    public static async deleteResource(resource: string, id: number): Promise<void> {
        try {
            const response = await api.delete(`${resource}/${id}`);
            if (response.data.response) {
                return;
            } else {
                throw new Error('Delete operation failed');
            }
        } catch (error) {
            throw error;
        }
    }

    public static async getKeys(module: { ID: number; }): Promise<any> {
        try {
            const response = await api.get(`${resource}/${module.ID}/module_keys`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    public static async addKey(moduleID: number, requestData: any): Promise<void> {
        try {
            const response = await api.post(`${resource}/${moduleID}/add_key`, requestData);
            if (response.data.response) {
                return;
            } else {
                throw new Error('Add key operation failed');
            }
        } catch (error) {
            throw error;
        }
    }

    // Ensure 'resource' is defined before use
    private static resource: string = '';  // Define this appropriately based on your application logic
}