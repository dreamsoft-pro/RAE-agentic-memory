import api from '@/lib/api';

class AuthClass {
    private resource = 'auth'; // Assuming this is the default resource for auth endpoints

    constructor(private url: string) {}

    private async loginGoogle(): Promise<void> {
        const response = await api.post(`${this.url}/google`, {}, { withCredentials: true });
        console.log('Logged in via Google');
    }

    private async loginFacebook(): Promise<void> {
        const response = await api.post(`${this.url}/facebook`, {}, { withCredentials: true });
        console.log('Logged in via Facebook');
    }

    public getMethods() {
        return {
            loginGoogle: this.loginGoogle.bind(this),
            loginFacebook: this.loginFacebook.bind(this)
        };
    }
}

export default AuthClass;