import api from '@/lib/api';

class GroupDescriptionsService {
    private resource: string;
    private url: string;

    constructor(resource: string) {
        this.resource = resource;
        this.url = `${process.env.API_URL}/${this.resource}`;
    }

    public async editDescription(data: any): Promise<any> {
        try {
            const response = await api.put(this.url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async getDescription(data?: any): Promise<any> {
        try {
            const response = await api.get(this.url, { params: data });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public sort(data: any): void {
        // Assuming the sorting function should be async as well
        this.editDescription(data).then(() => {
            console.log('Sorting completed');
        }).catch(error => {
            console.error('Error during sorting:', error);
        });
    }
}

export default GroupDescriptionsService;