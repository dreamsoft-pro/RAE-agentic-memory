import api from '@/lib/api';

class ModuleService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async getExtendedData(type: string, func: string): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${this.resource}/extended`;
            const response = await api.get(url, { params: { type, func } });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async create(module: any): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${this.resource}`;
            const response = await api.post(url, module);
            if (response.data.ID) {
                // Cache handling logic here
                return response.data;
            } else {
                throw new Error('Failed to create module');
            }
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

}

export default ModuleService;