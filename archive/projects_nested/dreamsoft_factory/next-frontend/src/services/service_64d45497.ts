import api from '@/lib/api';

class AdminHelpService {
    private resource: string = 'admin'; // Assuming 'resource' is always 'admin'

    public async updateKey(moduleName: string, key: any): Promise<any> {
        try {
            const response = await api.put(`${this.resource}/${moduleName}/helpKeys`, key);
            return response.data.response ? response.data.item : Promise.reject(response.data);
        } catch (error) {
            throw error;
        }
    }

    public async removeKey(moduleName: string, keyID: number): Promise<any> {
        try {
            const response = await api.delete(`${this.resource}/${moduleName}/helpKeys/${keyID}`);
            return response.data.response ? response.data.item : Promise.reject(response.data);
        } catch (error) {
            throw error;
        }
    }
}

export default new AdminHelpService();