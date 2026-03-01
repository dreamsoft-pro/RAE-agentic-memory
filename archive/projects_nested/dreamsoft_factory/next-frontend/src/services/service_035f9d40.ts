import api from '@/lib/api';

export default class AuthService {

    static async logout() {
        const url = `${process.env.AUTH_URL}/logout`;
        try {
            const response = await api.get(url, {
                params: { domainName: window.location.hostname }
            });
            AuthService.logOutWithGoogle();
            AuthService.logOutWithFacebook();
            AuthDataService.destroyUserData();
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    static check() {
        const _this = this;
        // Assuming you want to use a Promise here instead of $q.defer()
        return new Promise((resolve, reject) => {
            AuthService.logout().then(resolve).catch(reject);
        });
    }

    // Mock implementations for the methods that are being called
    static logOutWithGoogle() {}
    static logOutWithFacebook() {}
    static destroyUserData() {}

}