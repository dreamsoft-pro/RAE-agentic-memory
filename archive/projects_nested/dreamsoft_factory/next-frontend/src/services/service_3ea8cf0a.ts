import api from '@/lib/api';
import AuthService from '@/services/AuthService'; // Assuming this is the import for your auth service

class LoginPage {
    async handleFacebookLogin() {
        const response = await new Promise((resolve, reject) => {
            window.FB.login((response: any) => {
                if (response.authResponse) {
                    resolve(response);
                } else {
                    reject(new Error('User cancelled login or did not fully authorize.'));
                }
            }, { scope: 'email' });
        });

        const fields = ['name', 'email'];
        const data = await new Promise((resolve, reject) => {
            window.FB.api('/me?fields=' + fields.join(','), (response: any) => {
                if (!response.email || !response.name) {
                    reject(new Error('Missing required fields'));
                }
                resolve({
                    service: 'facebook',
                    email: response.email,
                    name: response.name.split(' ')[0],
                    lastName: response.name.split(' ').length > 1 ? response.name.split(' ')[1] : '',
                });
            });
        });

        try {
            await AuthService.loginWithFacebook(data);
            this.navigateToHome();
        } catch (error) {
            console.error('Login failed:', error);
        }
    }

    private navigateToHome() {
        // Assuming you have a method to trigger navigation or emit events
        // $rootScope.$emit('CreditLimit:reload', true);
        // $state.go('home');
    }
}