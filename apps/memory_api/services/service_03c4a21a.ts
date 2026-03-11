import api from '@/lib/api';
import { API_URL } from 'path/to/config'; // Adjust this import as necessary

class UserService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async updateImportantData(data: any): Promise<any> {
        try {
            const response = await api.patch(`${API_URL}/${this.resource}/importantData`, data);
            return response.data; // Assuming the API returns a JSON object
        } catch (error) {
            throw error.response?.data ?? error;
        }
    }

    public static async initializeUserService(resource: string): Promise<UserService> {
        const userService = new UserService(resource);
        return userService;
    }
}

export default UserService;