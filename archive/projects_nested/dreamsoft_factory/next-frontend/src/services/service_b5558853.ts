import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async addEfficiencySpeedChange(optID: string, controllerID: string, data: any): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${[this.resource, optID, 'efficiency', controllerID, 'speedChanges'].join("/")}`;
            const response = await api.post(url, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error;
        }
    }

    public async deleteEfficiencySpeedChange(optID: string, controllerID: string, id: string): Promise<void> {
        try {
            const url = `${process.env.API_URL}/${[this.resource, optID, 'efficiency', controllerID, 'speedChanges', id].join("/")}`;
            await api.delete(url);
        } catch (error) {
            throw error;
        }
    }

    private getResource(): string {
        return this.resource;
    }
}