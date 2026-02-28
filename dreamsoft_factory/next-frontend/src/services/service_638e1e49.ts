import api from '@/lib/api';

class ProcessService {

    private static async update(module: string, data: any): Promise<any> {
        const resource = module; // Ensure 'resource' is defined before use

        try {
            const response = await api.post($config.API_URL + resource, data);
            if (response.data.ID) {
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    // Example usage of the update method
    public static async performUpdate(module: string, data: any): Promise<void> {
        try {
            const result = await ProcessService.update(module, data);
            console.log('Result:', result);
        } catch (error) {
            console.error('Error during update:', error);
        }
    }
}

// Assuming $config and cache are defined elsewhere in your application.