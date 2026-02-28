import api from '@/lib/api';

export default class NewsletterService {

    private resource: string = 'dp_newsletter';
    
    async getAll(): Promise<any> {
        try {
            const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async export() : Promise<void> {
        // Your implementation for the export method goes here.
        // For now, it's left as a placeholder since you didn't provide specific requirements for this function.
        
        try {
            const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`);
            console.log(response.data);  // Example action with fetched data
        } catch (error) {
            throw error;
        }
    }

}