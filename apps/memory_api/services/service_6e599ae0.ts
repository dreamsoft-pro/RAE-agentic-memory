import api from '@/lib/api';

class PsConfigAttribute {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async checkCustomNames(typeID: number): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${[this.resource, 'checkCustomNames', typeID].join('/')}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async getAttributeSettings(typeID: number): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${[this.resource, 'getAttributeSettings', typeID].join('/')}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async getFilterConfig(attrID: number): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${[this.resource, 'getFilterConfig', attrID].join('/')}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}