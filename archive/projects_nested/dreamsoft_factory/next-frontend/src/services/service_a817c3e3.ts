import api from '@/lib/api';

export default class PsConfigOption {
    private getResource: () => string;

    constructor(getResource: () => string) {
        this.getResource = getResource;
    }

    async saveOptionDescriptions(optID: string, items: any[]): Promise<any> {
        const resource = `${this.getResource()}/${optID}/optionDescriptions`;
        try {
            const response = await api.put(`${process.env.API_URL}${resource}`, items);
            return response.data;
        } catch (error) {
            throw error.response ? error : new Error('An unexpected error occurred');
        }
    }

    async getOperations(optID: string, controllerID: string): Promise<any> {
        const resource = `${this.getResource()}/${optID}/optionOperations/${controllerID}`;
        try {
            const response = await api.get(`${process.env.API_URL}${resource}`);
            return response.data;
        } catch (error) {
            throw error.response ? error : new Error('An unexpected error occurred');
        }
    }
}