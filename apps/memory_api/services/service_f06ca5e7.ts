import api from '@/lib/api';

export default class GroupDescriptionsService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async create(data: any, showLang: boolean): Promise<any> {
        console.log('data');
        console.log(data);
        console.log(showLang);

        try {
            const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}?showLang=${showLang}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async removeDescription(id: string): Promise<any> {
        try {
            const response = await api.delete(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${id}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}