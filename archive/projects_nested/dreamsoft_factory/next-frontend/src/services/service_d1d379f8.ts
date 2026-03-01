import api from '@/lib/api';

class ModuleService {

    async editKey(moduleID: number, keyID: string | number, requestData: any): Promise<any> {
        const resource = 'module_keys'; // Define required variables before use
        const url = `${process.env.API_URL}/${resource}/${moduleID}/key/${keyID}`; // Use process.env for API_URL or import from config file

        try {
            const response = await api.patch(url, requestData);
            if (response.data.item) {
                return response.data.item;
            } else {
                throw new Error('Failed to edit key');
            }
        } catch (error) {
            throw error.response ? error.response.data : error; // Handle both error and response.error
        }
    }

    addKey = this.editKey;

    async removeKey(moduleID: number, keyID: string | number): Promise<any> {
        const resource = 'module_keys'; // Define required variables before use
        const url = `${process.env.API_URL}/${resource}/${moduleID}/key/${keyID}`; // Use process.env for API_URL or import from config file

        try {
            await api.delete(url);
            return { status: 'success' };
        } catch (error) {
            throw error.response ? error.response.data : error; // Handle both error and response.error
        }
    }

}

export default ModuleService;