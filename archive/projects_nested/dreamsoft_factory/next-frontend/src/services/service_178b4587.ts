import axios from 'axios';
import { API_URL } from '../config'; // Adjust import based on your actual configuration setup

class AttributeFiltersService {
    static async createAttributeOption(data: any): Promise<any> {
        try {
            const response = await axios.post(API_URL + 'attributeOption', data);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }

    static async getRelativePapers(data: any): Promise<any> {
        try {
            const response = await axios.post(API_URL + 'getRelativePapers', data);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }
}