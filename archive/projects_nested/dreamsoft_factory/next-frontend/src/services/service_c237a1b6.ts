import api from '@/lib/api';

class PsConfigOption {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    getResource(): string {
        return this.resource;
    }

    async getRelativeOptions(optID: number): Promise<any> {
        try {
            const url = `${import.meta.env.VITE_API_URL}/${this.getResource()}/${optID}/relativeOptions`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async search(attrID: number, filter: any): Promise<any> {
        try {
            const url = `${import.meta.env.VITE_API_URL}/attributeFilters/${attrID}`;
            const response = await api.post(url, filter);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async saveRelativeOptionsFilter(optID: number, data: any): Promise<any> {
        try {
            const url = `${import.meta.env.VITE_API_URL}/${this.getResource()}/${optID}/relativeOptions`;
            const response = await api.post(url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

}

export default PsConfigOption;