import api from '@/lib/api';

class AuctionService {

    static async getAuctionData(url: string): Promise<any> {
        const response = await api.get($config.API_URL + url);
        return response.data;
    }

    static async uploadFile(auctionID: number, file: File): Promise<void> {
        const formData = new FormData();
        formData.append('auctionFile', file);

        const response = await fetch(`${$config.API_URL}/${resource}/${auctionID}/auctionFiles`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Failed to upload file, status code: ${response.status}`);
        }
    }

    static async getAuctionFiles(auctionID: number): Promise<any> {
        const response = await api.get($config.API_URL + [resource, auctionID, 'auctionFiles'].join('/'));
        return response.data;
    }
}