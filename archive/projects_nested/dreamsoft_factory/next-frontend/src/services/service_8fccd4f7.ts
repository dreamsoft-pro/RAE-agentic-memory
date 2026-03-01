import api from '@/lib/api';

class ViewService {
    private getResource(): string {
        // Placeholder for getting the resource path
        return 'path/to/resource';
    }

    public async postRequest(data: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}${this.getResource()}`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response error');
            }
        } catch (error) {
            throw error;
        }
    }

    public async getAllNestedViews(): Promise<any> {
        try {
            const resource = this.getResource();
            const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}${resource}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    public getReplaceViews() {
        return this.postRequest({}).catch((error: any) => {
            throw new Error('Error in fetching replace views');
        });
    }
}

export default ViewService;