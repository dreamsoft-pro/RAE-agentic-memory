import api from "@/lib/api";

class AuthDataService {

    private static readonly apiUrl: string = '/api/user'; // Example URL, adjust as needed

    static async destroyUserData(): Promise<boolean> {
        const resource = await this.getCurrentUser();
        if (resource) {
            delete (window as any).username;  // Assuming window.username is a global variable
            await this.deleteAccessToken();   // Ensure this method exists and returns a promise
            localStorage.removeItem('user');  // Use native API for consistency
        }
        return true;
    }

    static async logout(): Promise<void> {
        await this.destroyUserData();
    }

    static getCurrentUser(): any | null {  // Adjust the type according to your actual data structure
        return localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null;
    }

    private static deleteAccessToken(): Promise<void> {
        const url = `${this.apiUrl}/token`;  // Example URL, adjust as needed
        return api.delete(url);
    }
}

// Export the class or use it directly in your application based on your architecture.
export default AuthDataService;