import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async deleteSpeedChange(optID: number, controllerID: number, id: number): Promise<any> {
        const url = `${process.env.API_URL}/${[this.getResource(), optID, 'efficiency', controllerID, 'speedChanges', id].join('/')}`;

        try {
            const response = await api.delete(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async getEfficiencySideRelations(optID: number, controllerID: number): Promise<any> {
        const url = `${process.env.API_URL}/${[this.getResource(), optID, 'efficiency', controllerID, 'sideRelations'].join('/')}`;

        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    private getResource(): string {
        // Implement the logic to get the resource here
        return '';  // Placeholder, replace with actual implementation
    }
}