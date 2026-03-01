import api from '@/lib/api';

export default class UserService {
    private resource: string;
    private url: string;

    constructor() {
        this.resource = 'users';
        this.url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
    }

    public async addUser(credentials: { email: string; name: string; lastName: string }): Promise<void> {
        try {
            await api.post(this.url, {
                user: credentials.email,
                name: credentials.name,
                lastname: credentials.lastName
            });
        } catch (error) {
            console.error('Failed to add user:', error);
        }
    }

    public async login(credentials: { email: string; password: string }): Promise<void> {
        try {
            await api.post(`${process.env.NEXT_PUBLIC_AUTH_URL}/login`, {
                data: new URLSearchParams({
                    email: credentials.email,
                    password: credentials.password
                }).toString(),
                params: {
                    domainName: window.location.hostname
                },
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });
        } catch (error) {
            console.error('Failed to log in:', error);
        }
    }
}