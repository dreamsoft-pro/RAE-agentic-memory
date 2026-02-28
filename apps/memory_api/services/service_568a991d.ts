import api from '@/lib/api';

class PsConfigAttribute {
    static async getFilters(attrID: string): Promise<any> {
        const resource = 'attributeFilters';
        const url = `${process.env.API_URL}/${resource}/${attrID}`;
        
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async getOptions(attrID: string): Promise<any> {
        const resource = 'attributeOptions';
        const url = `${process.env.API_URL}/${resource}/${attrID}`;
        
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static getResource(): string[] {
        return ['ps_attributes'];
    }
}