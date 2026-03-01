import api from '@/lib/api';
import { PsConfigOption } from './types'; // Assuming types are defined elsewhere

class TsPsConfigOption extends PsConfigOption {
    private getResource(): string {
        return this.resource; // This should be implemented based on your context
    }

    public async getAttributesForIncreases(): Promise<any> {
        const resource = `${this.getResource()}//increaseControllers//ps_config_related_increases`;
        try {
            const response = await api.get(resource);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async getRelatedIncreases(optID: string, controllerId: string): Promise<any> {
        const resource = `${this.getResource()}/${optID}/increaseControllers/${controllerId}/ps_config_related_increases_list`;
        try {
            const response = await api.get(resource);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default TsPsConfigOption;