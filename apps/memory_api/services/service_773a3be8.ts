import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class ProductFileService {
    private static instance: ProductFileService;

    private constructor() {}

    public static getInstance(): ProductFileService {
        if (!ProductFileService.instance) {
            ProductFileService.instance = new ProductFileService();
        }
        return ProductFileService.instance;
    }

    getUploadUrl(productId: string, fileId: string): string {
        // Implement your logic to generate the URL
        return `https://api.example.com/products/${productId}/files/${fileId}`;
    }

    async acceptFile(productId: string, fileId: string) {
        const response = await axios.patch(this.getUploadUrl(productId, fileId));
        return response.data;
    }

    async getAll(productId: string): Promise<any[]> {
        const response = await axios.get(this.getUrl(productId));
        return response.data;
    }

    getByList(orders: any[]): void {
        axios.post('https://api.example.com/orders', orders)
            .then(response => console.log(response.data))
            .catch(error => console.error(error));
    }

    private getUrl(productId: string): string {
        // Implement your logic to generate the URL
        return `https://api.example.com/products/${productId}/files`;
    }
}

export default ProductFileService.getInstance();