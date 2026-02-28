import api from '@/lib/api';

export default class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    getResource(): string {
        return this.resource;
    }

    async getEfficiencySpeed(optID: number, controllerID: number): Promise<any> {
        try {
            const response = await api.get(`${$config.API_URL}/${[this.getResource(), optID, 'efficiency', controllerID, 'speeds'].join('/')}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async addEfficiencySpeed(optID: number, controllerID: number, speedData: any): Promise<any> {
        try {
            const response = await api.post(`${$config.API_URL}/${[this.getResource(), optID, 'efficiency', controllerID, 'speeds'].join('/')}`, speedData);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid data received');
            }
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}