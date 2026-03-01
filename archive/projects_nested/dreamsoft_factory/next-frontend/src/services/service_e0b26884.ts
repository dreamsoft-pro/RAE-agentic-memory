import api from '@/lib/api';

class NewsletterService {
    private resource: string = 'your-resource-name'; // Define your resource here

    public async exportData(): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/export`;
            const response = await api.get(url);
            
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response data is not valid');
            }
        } catch (error: any) {
            throw error;
        }
    }
}

export default NewsletterService;