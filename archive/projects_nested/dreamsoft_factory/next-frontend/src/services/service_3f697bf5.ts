import api from '@/lib/api';
import { useState } from 'react';

interface FacebookLoginResponse {
    status: string;
}

interface UserInfoResponse {
    name: string;
    email: string;
}

async function getFacebookUserInfo(): Promise<UserInfoResponse> {
    return await api.get('/me', { params: { fields: 'name,email' } });
}

export default function LoginPage() {
    const [loginStatus, setLoginStatus] = useState<FacebookLoginResponse>();

    async function handleFBLogin() {
        // Simulate the FB.getLoginStatus response
        if (loginStatus?.status !== 'connected') {
            try {
                await new Promise<void>((resolve) => setTimeout(resolve, 500)); // Mock login delay

                const { name, email } = await getFacebookUserInfo();
                const firstName = name.split(' ')[0];
                const lastName = name.split(' ').length > 1 ? name.split(' ')[1] : '';

                const data: any = {
                    service: 'facebook',
                    email,
                    name: firstName,
                    lastName
                };

                // Assuming AuthService.loginWithFacebook is a function that returns a promise.
                await api.post('/auth/login/facebook', data);

                // Simulate navigation and reload event
                console.log('Login successful, navigating to home.');
            } catch (error) {
                console.error('Failed to login with Facebook:', error);
            }
        }
    }

    return (
        <div>
            {loginStatus?.status === 'connected' ? (
                <p>You are already connected.</p>
            ) : (
                <button onClick={handleFBLogin}>Log In with Facebook</button>
            )}
        </div>
    );
}