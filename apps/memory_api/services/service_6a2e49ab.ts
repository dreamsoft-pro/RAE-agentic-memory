import api from '@/lib/api';
import { useEffect, useState } from 'react';

class UserService {
    private static async addSimple(userData: { user: string; name: string; lastname: string }) {
        const response = await api.post('/add-simple', userData);
        return response.data;
    }

    public login(credentials: { email: string; name: string; lastName: string }) {
        UserService.addSimple({
            user: credentials.email,
            name: credentials.name,
            lastname: credentials.lastName
        }).then(async (data) => {
            try {
                const loginResponse = await api.post(`${process.env.AUTH_URL}/login`, credentials, {
                    params: { domainName: window.location.hostname },
                    headers: { "Content-Type": "application/x-www-form-urlencoded" }
                });
                
                this.setUserData(loginResponse.data).then(confirm => {
                    // Handle success
                }).catch(error => {
                    // Handle error
                });
            } catch (error) {
                console.error('Login failed:', error);
            }
        }).catch(error => {
            console.error('Adding simple user failed:', error);
        });
    }

    private setUserData(data: any): Promise<void> {
        return new Promise((resolve, reject) => {
            // Implementation for setting user data
            resolve();
        });
    }
}

const App = () => {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        if (userData !== null) {
            console.log('User data:', userData);
        }
    }, [userData]);

    const userService = new UserService();

    // Example usage
    userService.login({ email: 'user@example.com', name: 'John', lastName: 'Doe' });

    return <div>User data will be logged here</div>;
};