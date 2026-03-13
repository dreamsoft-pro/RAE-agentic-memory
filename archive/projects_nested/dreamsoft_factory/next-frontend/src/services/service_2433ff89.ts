import { useRouter } from 'next/router';
import api from '@/lib/api';

class AuthService {
    static async loginWithGoogle(data: { id_token: string; email: string; service: string; name?: string; lastName?: string }) {
        try {
            const response = await api.post('/login', data);
            return response.data;
        } catch (error) {
            throw new Error('Failed to log in with Google');
        }
    }

    static handleLoginSuccess() {
        // Implement your logic here for handling the success of login
        // This could be navigation or emitting events
    }

    static handleError(error: any) {
        console.error('Error during login:', error);
    }
}

const Home = () => {
    const router = useRouter();
    
    const handleGoogleLoginSuccess = async (id_token: string, email: string, name?: string, lastName?: string) => {
        try {
            await AuthService.loginWithGoogle({
                id_token,
                email,
                service: 'google',
                name,
                lastName
            });
            // Assuming you want to navigate to the home page on success
            router.push('/home');
        } catch (error) {
            AuthService.handleError(error);
        }
    };

    return (
        <div>
            {/* Your component JSX goes here */}
            {/* Example: */}
            <button onClick={() => handleGoogleLoginSuccess('your_id_token', 'example@example.com', 'John', 'Doe')}>Sign in with Google</button>
        </div>
    );
};

export default Home;