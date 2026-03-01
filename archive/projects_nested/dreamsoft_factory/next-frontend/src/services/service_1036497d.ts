import api from '@/lib/api';

class PsConfigOption {
    private getResource: () => string;

    constructor(getResource: () => string) {
        this.getResource = getResource;
    }

    public async getPaperIncreases(optID: string): Promise<any[]> {
        const resource = `${this.getResource()}/${optID}/increaseControllers/0/ps_config_increases`;

        try {
            const response = await api.get(resource);
            return response.data; // Assuming the API returns plain data
        } catch (error) {
            throw error;
        }
    }

    public async saveRelatedIncreases(optID: string, controllerId: number, increases: any[]): Promise<any[]> {
        const resource = `${this.getResource()}/${optID}/increaseControllers/${controllerId}/ps_config_related_increases_list`;

        try {
            const response = await api.patch(resource, increases);
            return response.data; // Assuming the API returns plain data
        } catch (error) {
            throw error;
        }
    }
}