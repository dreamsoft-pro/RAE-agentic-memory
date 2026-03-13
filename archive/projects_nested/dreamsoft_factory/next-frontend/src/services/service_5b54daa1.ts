import api from '@/lib/api';

export default class ModuleService {
    async deleteModuleOption(resource: string, moduleID: number, keyID: number, optionID: number): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, moduleID, 'module_keys', keyID, 'module_options', optionID].join("/")}`;

        try {
            const response = await api.delete(url);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Data does not contain "response"');
            }
        } catch (error: any) {
            throw error.response ? error.response : error;
        }
    }

    // Constructor or other methods can go here as needed
}