import api from '@/lib/api';
import { useState } from 'react';

class AuthService {
    static async signOut() {
        try {
            await api.post('/auth/sign-out');
            // Perform cleanup or additional actions if needed.
        } catch (error) {
            console.error('Sign out failed:', error);
        }
    }

    static async login(credentials: { username: string; password: string }) {
        try {
            const response = await api.post('/auth/login', credentials);
            if (!response.data.success) {
                throw new Error(response.data.message || 'Login failed');
            }
            // Perform additional actions after successful login.
        } catch (error) {
            console.error('Login failed:', error);
        }
    }

    static async processLogoutOnError() {
        try {
            const response = await api.get('/some-resource');  // Assuming this is the resource fetching operation
            if (!response.data.ok) {  // Assuming 'ok' indicates a specific state
                await AuthService.signOut();
            }
        } catch (error) {
            console.error('Error processing logout:', error);
        }
    }

    static async someOtherMethod() {
        try {
            const response = await api.get('/another-resource');  // Example resource fetching operation
            if (!response.data.ok) {  // Assuming 'ok' indicates a specific state
                return Promise.reject(new Error('Some other method failed'));  // Return rejection for error handling in callers
            }
            // Proceed with successful operations
        } catch (error) {
            console.error('Error in someOtherMethod:', error);
            return Promise.reject(error);  // Re-throw the error if needed for caller's error handling
        }
    }
}

// Example usage in a Next.js component
const MyComponent = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const handleLogin = async (credentials) => {
        try {
            await AuthService.login(credentials);
            setIsLoggedIn(true);
        } catch (error) {
            console.error('Failed to login:', error);
        }
    };

    const handleSignOut = async () => {
        try {
            await AuthService.signOut();
            setIsLoggedIn(false);
        } catch (error) {
            console.error('Failed to sign out:', error);
        }
    };

    return (
        <div>
            {isLoggedIn ? (
                <>
                    <p>You are logged in.</p>
                    <button onClick={handleSignOut}>Sign Out</button>
                </>
            ) : (
                <>
                    <p>Please log in.</p>
                    <input type="text" placeholder="Username" />
                    <input type="password" placeholder="Password" />
                    <button onClick={() => handleLogin({ username: 'user', password: 'pass' })}>Log In</button>
                </>
            )}
        </div>
    );
};

export default MyComponent;