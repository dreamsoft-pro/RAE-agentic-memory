import axios from 'axios';
import { AxiosResponse } from 'axios';

class AttributeFiltersService {

    static async search(attrID: string, filter: any): Promise<any> {
        try {
            const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/attributeFilters/${attrID}`, filter);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    static async downloadPDF(data: any): Promise<any> {
        try {
            const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/attributeOptionPDF/${data.optID}`, data);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

}

export default AttributeFiltersService;