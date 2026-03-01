import axios, { AxiosPromise } from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class ProductFileService {
    private static API_URL: string;

    public static initialize(apiUrl: string): void {
        this.API_URL = apiUrl;
    }

    public static async getProductListFiles(orders: string[]): Promise<any> {
        const url = `${this.API_URL}/productFiles/productListFiles/${orders.join(',')}`;
        return axios.get(url).then(response => response.data);
    }

    public static removeFile(productID: string, fileID: string): AxiosPromise<any> {
        const url = this.getUrl(productID) + '/' + fileID;
        return axios.delete(url);
    }

    private static getUrl(productID: string): string {
        return `${this.API_URL}/productFiles/${productID}`;
    }
}

export default ProductFileService;

// Usage Example:
ProductFileService.initialize('https://your-api-url.com');