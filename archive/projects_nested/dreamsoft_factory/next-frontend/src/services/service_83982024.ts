import api from '@/lib/api';

class UserService {

    private readonly apiUrl: string;
    private resource: string;

    constructor(resource: string) {
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL!;
        this.resource = resource;
    }

    async sendPasswordResetEmail(email: string): Promise<any> {
        try {
            const response = await api.post(`${this.apiUrl}/${this.resource}/passForget`, { email });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    async generateNewFtp(): Promise<any> {
        try {
            const response = await api.get(`${this.apiUrl}/${this.resource}/changeFtpPass`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}

export default UserService;