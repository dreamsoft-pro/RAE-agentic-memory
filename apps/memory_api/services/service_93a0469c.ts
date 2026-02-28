import api from '@/lib/api';

class AuthDataService {
    static accessTokenName: string;

    static getCookie(cname: string): string {
        const name = `${cname}=`;
        const decodedCookie = decodeURIComponent(document.cookie);
        const ca = decodedCookie.split(';');
        
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }

        return "";
    }

    static async getAccessToken(): Promise<string> {
        const accessTokenName: string = this.accessTokenName;
        const tokenCookieValue = this.getCookie(accessTokenName);
        
        if (!tokenCookieValue) {
            throw new Error(`No ${accessTokenName} found in cookies.`);
        }
        
        return tokenCookieValue;
    }

    static setAccessToken(domainHost: string, accessToken: string): void {
        let domainName = domainHost;

        if (domainHost === 'localhost') {
            domainName = 'localhost';
        }

        // Set your cookie logic here based on the domainName and accessToken
        document.cookie = `${this.accessTokenName}=${accessToken}; path=/; domain=${domainName}`;
    }
}

// Example usage:
AuthDataService.accessTokenName = 'your_access_token_name';

export default AuthDataService;