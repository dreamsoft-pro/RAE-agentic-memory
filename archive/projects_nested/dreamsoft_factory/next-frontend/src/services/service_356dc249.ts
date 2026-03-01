import api from '@/lib/api';

class AuctionService {

    static async finishAuction(auctionID: string, resource: string): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${[resource, 'finishAuction', auctionID].join('/')}`;

        try {
            const response = await api.put(url);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response data is not valid');
            }
        } catch (error: any) {
            throw error.response ? error.response.data : error;
        }
    }

    static async order(auctionID: string, data: any): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${[data.resource, 'order', auctionID].join('/')}`;

        try {
            const response = await api.put(url, data);
            return response.data;
        } catch (error: any) {
            throw error.response ? error.response.data : error;
        }
    }

}

export default AuctionService;