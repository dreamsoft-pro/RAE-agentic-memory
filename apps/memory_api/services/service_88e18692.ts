import axios from 'axios';

class ProductFileService {

    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    public async saveFileProps(productID: number, fileID: number, data: any): Promise<any> {
        try {
            const response = await axios.post(`${this.apiUrl}/dp_products/${productID}/productFiles/saveFileProps/${fileID}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    public async saveProductProps(productID: number, sendToFix: boolean): Promise<any> {
        try {
            const response = await axios.post(`${this.apiUrl}/dp_products/${productID}/productFiles/saveProductProps`, { sendToFix });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}