import { NextApiRequest, NextApiResponse } from 'next';
import api from '@/lib/api';

class AuthService {
    private fb: any;
    private gapiAuth2?: any;

    public async logOutWithFacebook(): Promise<void> {
        if (this.fb) {
            const response = await this.fb.getLoginStatus();
            if (response.status === 'connected') {
                await new Promise((resolve, reject) => {
                    this.fb.logout(() => resolve());
                });
            } else {
                throw new Error('Nie był zalogowany');
            }
        } else {
            throw new Error('FB not exists');
        }
    }

    public async logOutWithGoogle(): Promise<void> {
        if (typeof gapi === 'undefined') {
            return;
        }

        await new Promise((resolve, reject) => {
            gapi.load('auth2', () => {
                gapi.auth2.init({
                    client_id: '345059472892-1fae8hutprcgcg3gk0i1dvdconjarcr0.apps.googleusercontent.com',
                    fetch_basic_profile: true,
                    scope: 'profile'
                }).then(() => {
                    if (gapi.auth2.getAuthInstance().isSignedIn.get()) {
                        gapi.auth2.getAuthInstance().signOut();
                        resolve();
                    } else {
                        reject('Not signed in');
                    }
                });
            });
        });
    }

    public static async handleLogout(req: NextApiRequest, res: NextApiResponse) {
        try {
            await new AuthService().logOutWithFacebook();
            await new AuthService().logOutWithGoogle();
            res.status(200).json({ message: 'Logged out successfully' });
        } catch (error) {
            res.status(400).json({ error: error.message });
        }
    }
}

export default AuthService;