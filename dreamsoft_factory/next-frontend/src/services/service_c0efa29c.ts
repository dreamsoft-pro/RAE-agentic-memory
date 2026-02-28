import axios from 'axios';
import { API_URL } from './config'; // Assuming you have a config file with the API URL

class AttributeFiltersService {
    static async getProductsUsingOptions(attrID: string): Promise<any> {
        try {
            const response = await axios.get(`${API_URL}/productsUsingOptions/${attrID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    static async getOptions(attrID: string): Promise<any> {
        try {
            const response = await axios.get(`${API_URL}/attributeOptions/${attrID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    // Assuming 'data' is not used in the original snippet and this function was unfinished.
    static getOption(data: any): Promise<any> {
        const def = new Promise((resolve, reject) => {
            axios.get(`${API_URL}/path/to/option`, { params: data })
                .then(response => resolve(response.data))
                .catch(error => reject(error.response ? error.response.data : error));
        });
        return def;
    }
}