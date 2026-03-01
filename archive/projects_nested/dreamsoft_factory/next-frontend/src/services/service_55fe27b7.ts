import { User } from '@your-module/user'; // Adjust import according to your module structure
import api from '@/lib/api';

class AuthController {
    async authenticateUser(user: User) {
        console.log('AUTH2.c');
        const auth2 = /* Ensure this is properly initialized or imported */;
        
        if (!auth2) throw new Error('Auth2 instance not found');

        const id_token = user.getAuthResponse().id_token;
        const email = user.getBasicProfile().getEmail();
        const name = user.getBasicProfile().getGivenName();
        const lastName = user.getBasicProfile().getFamilyName();

        if (!id_token || !email || !name || !lastName) {
            throw new Error('Incomplete authentication data');
        }

        const data = {
            id_token: id_token,
            email: email,
            service: 'google',
            name: name,
            lastName: lastName
        };

        try {
            await api.loginWithGoogle(data);
            // Handle success or add more logic as required
        } catch (error) {
            console.error('Failed to authenticate user:', error);
            throw error;
        }
    }
}