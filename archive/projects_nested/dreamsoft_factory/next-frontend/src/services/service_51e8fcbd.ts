import api from '@/lib/api';
import { NextApiRequest, NextApiResponse } from 'next';

class ModuleService {

    private apiUrl: string;

    constructor() {
        this.apiUrl = process.env.API_URL || '';
    }

    async addOption(moduleID: number | string, keyID: number | string, option: any): Promise<any> {
        try {
            const url = `${this.apiUrl}/${resource}/${moduleID}/module_keys/${keyID}/module_options`;
            
            // Ensure resource is defined before use
            if (!resource) throw new Error('Resource variable must be defined');

            const response = await api.patch(url, option);

            if (response.data.response) {
                return response.data.item;
            } else {
                throw new Error(response.data.message || 'Unknown error');
            }
        } catch (error) {
            console.error(error);
            throw error; // Re-throw to maintain promise rejection
        }
    }

    editOption = this.addOption;

    async removeOption(moduleID: number | string, keyID: number | string, optionID: number): Promise<void> {
        try {
            const url = `${this.apiUrl}/${resource}/${moduleID}/module_keys/${keyID}/module_options/${optionID}`;

            if (!resource) throw new Error('Resource variable must be defined');

            await api.delete(url);
            
            // No data is returned, so no need to handle it here
        } catch (error) {
            console.error(error);
            throw error; // Re-throw to maintain promise rejection
        }
    }

}

// Ensure resource is properly defined elsewhere in your application
export default ModuleService;