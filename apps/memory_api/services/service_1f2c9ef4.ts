import api from '@/lib/api';
import { useEffect, useState } from 'react';

// Assuming some utility functions are needed for lodash functionality
function isObject(obj: any): boolean {
    return obj && typeof obj === 'object' && !Array.isArray(obj);
}

function isEmpty(obj: any): boolean {
    if (isObject(obj)) {
        return Object.keys(obj).length === 0;
    }
    return true;
}

class AuthDataService {
    private getAccessToken(): string | null {
        // Implement your logic to retrieve the access token
        return localStorage.getItem('access_token') || null; // Example implementation
    }

    private getCurrentUser(): any {
        // Implement your logic to retrieve the current user data
        return JSON.parse(localStorage.getItem('user_data') || '{}'); // Example implementation
    }

    public async isLoggedIn(): Promise<boolean> {
        const token = this.getAccessToken();
        if (token) {
            const currentUser = await api.get('/api/current-user');
            return isObject(currentUser) && !isEmpty(currentUser);
        }
        return false;
    }

    public checkGoogle() {
        const def = { resolve: () => {}, reject: () => {} } as Promise<void>; // Simulating Q.defer()

        useEffect(() => {
            try {
                window.gapi.load('auth2', function () {
                    const auth2 = window.gapi.auth2.init({
                        client_id: '345059472892-1fae8hutprcgcg3gk0i1dvdconjarcr0.apps.googleusercontent.com',
                        fetch_basic_profile: true,
                        scope: 'profile',
                    });
                });
            } catch (error) {
                def.reject(error);
            }
        }, []);

        return new Promise<void>((resolve, reject) => {
            def.resolve = resolve;
            def.reject = reject;
        });
    }
}

export default AuthDataService;