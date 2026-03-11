import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor() {
        // Ensure the resource variable is defined before use
        this.resource = '';
    }

    getResource(): string {
        return this.resource;
    }

    async getIncreases(optID: number, controllerID: number): Promise<any[]> {
        const url = `${this.getResource()}/${optID}/increaseControllers/${controllerID}/ps_config_increases`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async getRelatedIncreaseCount(optID: number, controllerID: number): Promise<number> {
        const url = `${this.getResource()}/${optID}/increaseControllers/${controllerID}/ps_config_related_increases_count`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}