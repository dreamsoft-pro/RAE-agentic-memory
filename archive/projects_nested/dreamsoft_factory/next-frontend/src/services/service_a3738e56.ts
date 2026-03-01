import api from '@/lib/api';

class CalcFileService {
    private apiUrl: string;

    constructor() {
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL || ''; // Ensure API_URL is defined or configure it in environment variables
    }

    public async createGuestSet(typeID: number): Promise<any> {
        try {
            const response = await api.get(`${this.apiUrl}/dp_products/${typeID}/calcFilesUploaderGuestSet`);
            return response.data;
        } catch (error) {
            throw new Error(error);
        }
    }

    public async setImageBW(fileID: string): Promise<any> {
        try {
            const response = await api.post(`${this.apiUrl}/calcFilesUploader/setImageBW/${fileID}`);
            return response.data;
        } catch (error) {
            throw new Error(error);
        }
    }
}