import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    getResource(): string {
        return this.resource;
    }

    async getExclusions(optID: string): Promise<any> {
        const url = `${this.getResource()}/${optID}/exclusions`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async saveExclusions(optID: string, exclusions: any): Promise<any> {
        const url = `${this.getResource()}/${optID}/exclusions`;
        try {
            const response = await api.patch(url, exclusions);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}