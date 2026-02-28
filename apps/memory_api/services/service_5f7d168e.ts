import api from '@/lib/api';

export default class AuctionService {
    private static getResourceUrl(auctionID: string, resource: string): string {
        return `${api.baseUrl}/${resource}/${auctionID}`;
    }

    public static async getFile(auctionID: string, fileID: string): Promise<string> {
        const url = this.getResourceUrl(auctionID, 'auctionFiles') + `/getFile/${fileID}`;
        return url;
    }

    public static async removeFile(auctionID: string, fileID: string): Promise<void | any> {
        try {
            const response = await api.delete(`${this.getResourceUrl(auctionID, 'auctionFiles')}/${fileID}`);
            if (response.data.response) {
                // Assuming cache.remove is a function that needs to be defined elsewhere
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(response.statusText);
            }
        } catch (error: any) {
            throw error;
        }
    }

    public static async forCompany(filters: any): Promise<any> {
        const def = {} as { resolve: (value?: any) => void; reject: (reason?: any) => void };

        try {
            // Assuming $config.API_URL and resource are defined elsewhere
            const url = `${api.baseUrl}/${resource}`;
            const response = await api.get(url, { params: filters });
            def.resolve(response.data);
        } catch (error: any) {
            def.reject(error);
        }

        return new Promise((resolve, reject) => {
            def.resolve = resolve;
            def.reject = reject;
        });
    }
}