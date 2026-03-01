import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    getResource(): string {
        // Implement this method as per your application logic
        return 'your_resource';
    }

    async doPOST(item: any): Promise<any> {
        try {
            const response = await api.post(this.resource, item);
            
            if (response.data.ID) {
                cache.remove(this.resource);
                return response;
            } else {
                throw new Error('Data rejection');
            }
        } catch (error) {
            cache.remove(this.resource);
            throw error;
        }
    }

    async edit(item: any): Promise<any> {
        try {
            const response = await api.put(this.resource, item);
            
            if (response.data.response) {
                cache.remove(this.resource);
                return response;
            } else {
                throw new Error('Data rejection');
            }
        } catch (error) {
            cache.remove(this.resource);
            throw error;
        }
    }

    // Implement the getResource method as needed
}