import api from '@/lib/api';

class CookieManager {
    private readonly domainHost: string;

    constructor(domainHost: string) {
        this.domainHost = domainHost;
    }

    getCookie(cname: string): string {
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

    async setCookie(name: string, value: string, days: number): Promise<void> {
        const expiration_date = new Date();
        expiration_date.setTime(expiration_date.getTime() + (days * 24 * 60 * 60 * 1000));

        const domainName = this.domainHost === 'localhost' ? 'localhost' : '';
        
        document.cookie = `${name}=${value}; expires=${expiration_date.toUTCString()}; path=/; domain=${domainName}`;
    }
}

export default CookieManager;