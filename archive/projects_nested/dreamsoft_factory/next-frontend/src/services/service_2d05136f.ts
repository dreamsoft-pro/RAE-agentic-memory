import api from "@/lib/api";

class MyClass {
    private logged: boolean = false;
    private auth2!: any;

    constructor() {
        this.logged = true; // Assuming $rootScope.logged is not needed in the class context.
    }

    public async myMethod(): Promise<void> {
        try {
            const response = await api.get('/some-url'); // Replace with actual API call
            const data = response.data;
            
            if (data.success) {
                console.log(data); // Resolve logic replaced by logging or further processing
            } else {
                throw new Error('Request failed');
            }
        } catch (err) {
            console.error(err);
        }

        try {
            await this.initGoogleAuth();
        } catch (error) {
            console.error(error);
        }
    }

    private async initGoogleAuth(): Promise<void> {
        const clientId = '345059472892-1fae8hutprcgcg3gk0i1dvdconjarcr0.apps.googleusercontent.com';
        const scopes = ['profile'];

        await this.loadAndInitGoogleAuth(clientId, scopes);
    }

    private async loadAndInitGoogleAuth(clientId: string, scopes: string[]): Promise<void> {
        return new Promise((resolve) => {
            gapi.load('auth2', () => {
                this.auth2 = gapi.auth2.init({ client_id: clientId, fetch_basic_profile: true, scope: scopes.join(' ') });
                
                if (this.auth2.isSignedIn.get()) {
                    resolve();
                } else {
                    throw new Error('User is not signed in');
                }
            });
        });
    }
}

// Usage:
const myClassInstance = new MyClass();
myClassInstance.myMethod().catch(console.error);