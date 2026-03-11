import axios from '@/lib/api'; // Assuming this is a custom wrapper for axios

class UserService {
    private cache: any; // You should define type properly based on actual implementation.
    private config: { API_URL: string };

    constructor(cache: any, config: { API_URL: string }) {
        this.cache = cache;
        this.config = config;
    }

    async getAll(force?: boolean): Promise<any> {
        if (this.cache.get('collection') && !force) {
            return this.cache.get('collection');
        } else {
            try {
                const response = await axios.get(this.config.API_URL + this.resource);
                this.cache.put('collection', response.data);
                return response.data;
            } catch (error) {
                throw error; // or handle the error as needed
            }
        }
    }

    async add(data: any): Promise<any> {
        try {
            const response = await axios.post(this.config.API_URL + this.resource, data);
            return response.data;
        } catch (error) {
            throw error; // or handle the error as needed
        }
    }
}

// Example instantiation and usage
const userService = new UserService(cacheInstance, configInstance);

userService.getAll().then(data => console.log('Data:', data)).catch(error => console.error('Error:', error));
userService.add({ /* some data */ }).then(result => console.log('Result:', result)).catch(error => console.error('Error:', error));