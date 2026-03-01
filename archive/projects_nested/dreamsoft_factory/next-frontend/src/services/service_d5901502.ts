import api from '@/lib/api';

class ReclamationStatusService {
    private resource: string;

    constructor() {
        this.resource = 'dp_reclamations_statuses';
    }

    public async getAll(active?: boolean): Promise<any[]> {
        let url = [this.resource];
        
        if (active !== undefined) {
            url.push('1');
        }
        
        try {
            const response = await api.get(url.join('/'));
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error(JSON.stringify(error));
        }
    }

    public async add(data: any): Promise<any> {
        let url = this.resource;

        try {
            const response = await api.post(url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error(JSON.stringify(error));
        }
    }
}

export default ReclamationStatusService;