import api from '@/lib/api';

class PsWorkingHourService {
    private apiUrl: string = process.env.NEXT_PUBLIC_API_URL as string; // Assuming NEXT_PUBLIC_API_URL is set in your environment

    public async updateResource(resource: string, data: any): Promise<any> {
        const url = `${this.apiUrl}/${resource}`;
        
        try {
            const response = await api.patch(url, data);
            
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response is not as expected');
            }
        } catch (error: any) {
            throw error; // rethrow the error
        }
    }

    public static getWorkingHourService(): PsWorkingHourService {
        return new PsWorkingHourService();
    }
}

export default PsWorkingHourService;