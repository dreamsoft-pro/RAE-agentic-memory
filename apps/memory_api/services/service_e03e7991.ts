import axios from '@/lib/api';
import { Cache } from 'your-cache-module'; // Assuming you have a cache module similar to what was used in the original code

class AuctionService {
    private cache: Cache; // Define cache as an instance property if needed

    public async updateResource(resource: string, offer: any): Promise<any> {
        const url = process.env.API_URL + resource;
        
        try {
            const response = await axios.put(url, offer);
            if (response.data.response) {
                this.cache.remove('collection'); // Ensure `cache` is properly initialized before use
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error; // Re-throw the caught error
        }
    }

    public async removeById(id: string): Promise<void> {
        const url = process.env.API_URL + id;

        try {
            await axios.delete(url);
        } catch (error) {
            throw error;
        }
    }
}

export default new AuctionService(); // Export the instance of your service