import api from '@/lib/api';

export default class MyClass {
    private async postOrder(auctionID: string, resource: string, data: any): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, 'order', auctionID].join('/')}`;

        try {
            const response = await api.post(url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}