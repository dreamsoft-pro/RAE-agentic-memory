import api from '@/lib/api';

export default class DpOrderStatusService {

    private resource: string = 'dp_statuses';

    public async getAll(active?: boolean): Promise<any> {
        try {
            const response = await api.get([this.resource, 'forClient'].join('/'));
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}