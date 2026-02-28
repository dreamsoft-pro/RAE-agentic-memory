import axios from 'axios';
import { API_URL } from '@/config'; // Adjust import based on your project setup

export class ProductFileService {
    static async getMiniature(fileID: string): Promise<any> {
        try {
            const response = await axios.get(`${API_URL}/productFiles/makeMiniature/${fileID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    static async acceptReport(productID: string, fileID: string): Promise<any> {
        try {
            const response = await axios.patch(`${API_URL}/dp_products/${productID}/productFiles/${fileID}/productReportFiles`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    static async rejectReport(productID: string, fileID: string, comment: string): Promise<any> {
        try {
            const response = await axios.patch(`${API_URL}/dp_products/${productID}/productFiles/${fileID}/productReportFiles`, { comment });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}