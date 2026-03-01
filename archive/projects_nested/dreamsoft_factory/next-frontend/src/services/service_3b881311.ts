import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class ProductFileService {
    private apiUrl: string = process.env.API_URL as string;

    public async deleteProductReportFile(productID: number, fileID: number, comment: string): Promise<void> {
        try {
            const response = await axios.delete(`${this.apiUrl}/dp_products/${productID}/productFiles/${fileID}/productReportFiles`, {
                data: {comment},
                headers: {
                    "Content-Type": "application/json"
                }
            });
            return Promise.resolve(response.data);
        } catch (error) {
            return Promise.reject(error.response?.data || error.message);
        }
    }

    public getReportsUploadUrl(productID: number, fileID: number): string {
        return `${this.apiUrl}/dp_products/${productID}/productFiles/${fileID}/productReportFiles`;
    }
}

export default ProductFileService;