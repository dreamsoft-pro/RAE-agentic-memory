import axios from '@/lib/api';
import { Cache } from '@/utils/cache'; // Assuming cache utilities are here

export default class RouteService {
    static async remove(state: string): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${state}`;
        
        try {
            const response = await axios.delete(url);
            
            if (response.data.response) {
                Cache.remove('collection');
                return response.data;
            } else {
                throw new Error(response.data.error); // Or any error handling mechanism you prefer
            }
        } catch (error) {
            throw error; // Handle error appropriately in calling code or add more details to the exception
        }
    }
}