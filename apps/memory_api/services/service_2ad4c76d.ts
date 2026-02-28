import api from '@/lib/api';

class AuthService {

    private setUserData(data: any): Promise<void> {
        // Implement this method based on your requirements.
        return new Promise((resolve, reject) => {
            resolve();  // Placeholder for actual implementation.
        });
    }

    public async socialLogin(data: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.AUTH_URL}/socialLogin`, $.param(data), {
                params: { domainName: window.location.host },
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            });

            await this.setUserData(response.data);
            return response.data;
        } catch (error) {
            throw error;  // Handle the error appropriately as needed.
        }
    }

    public async cleanSession(params?: any): Promise<void> {
        try {
            // Assuming that the backend endpoint for cleaning session is different and needs to be called here.
            await api.post(`${process.env.AUTH_URL}/cleanSession`, params);  // Adjust URL as per your actual API.
            return; 
        } catch (error) {
            throw error;
        }
    }

}