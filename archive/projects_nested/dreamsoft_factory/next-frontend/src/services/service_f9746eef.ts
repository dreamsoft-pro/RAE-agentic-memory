import { useEffect } from 'react';
import api from '@/lib/api'; // Custom API module

declare global {
    interface Window {
        gapi: any;
    }
}

interface AuthState {
    userAuth?: any;
}

class AuthDataService {

    private auth2?: any;
    private userAuth?: any;

    constructor() {}

    async checkGoogle(): Promise<void> {
        if (window.gapi) {
            this.auth2 = window.gapi.auth2.init({
                client_id: '345059472892-1fae8hutprcgcg3gk0i1dvdconjarcr0.apps.googleusercontent.com',
                fetch_basic_profile: true,
                scope: 'profile'
            });

            await this.auth2.then(() => {
                const userAuth = this.auth2.currentUser.get();
                this.userAuth = userAuth;
            }).catch((e) => {
                console.error('Google Auth Error:', e);
            });
        }
    }

    signOutFromGoogle(): void {
        if (this.auth2 && this.auth2.currentUser) {
            this.auth2.signOut().then(() => {
                // Handle signing out logic here
                this.userAuth = undefined;
            }).catch((e) => {
                console.error('Sign Out Error:', e);
            });
        }
    }

    signInWithGoogle(): void {
        if (!window.gapi) {
            const script = document.createElement('script');
            script.src = 'https://apis.google.com/js/platform.js';
            script.async = true;
            script.onload = () => window.gapi.load('auth2', this.initializeAuth);
            document.head.appendChild(script);
        } else {
            this.initializeAuth();
        }
    }

    private initializeAuth(): void {
        if (window.gapi) {
            this.auth2 = window.gapi.auth2.init({
                client_id: '345059472892-1fae8hutprcgcg3gk0i1dvdconjarcr0.apps.googleusercontent.com',
                fetch_basic_profile: true,
                scope: 'profile'
            });

            this.auth2.then(() => {
                const googleUser = this.auth2.currentUser.get();
                if (googleUser) {
                    // Handle successful sign-in logic here
                    console.log('Google User:', googleUser);
                }
            }).catch((e) => {
                console.error('Auth Initialization Error:', e);
            });
        }
    }

    checkLogedInOutsideServices(): void {
        this.checkGoogle();
    }
}

export default AuthDataService;