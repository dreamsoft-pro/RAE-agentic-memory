import api from '@/lib/api';
import { setUserData } from './user'; // Assuming there's a function to set user data

class AuthService {
    static async loginWithGoogle(credentials: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.AUTH_URL}/login`, credentials, {
                params: {
                    domainName: window.location.hostname
                },
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });

            await setUserData(response.data);
            return response.data;
        } catch (error) {
            throw error; // Rethrow the error or handle it as needed
        }
    }

    private static async setUserData(data: any): Promise<boolean> {
        // Implementation of setting user data goes here.
        // For simplicity, let's assume this function returns true if successful.
        return new Promise((resolve) => resolve(true));
    }
}