import api from '@/lib/api';

class AuthDataService {
    private accessTokenName: string;
    private domainHost: string;

    constructor(accessTokenName: string, domainHost: string) {
        this.accessTokenName = accessTokenName;
        this.domainHost = domainHost;
    }

    async updateAccessToken(accessToken: string): Promise<void> {
        const expirationDate = new Date();
        expirationDate.setFullYear(expirationDate.getFullYear() + 1);

        document.cookie = `${this.accessTokenName}=${accessToken}; domain=${this.domainHost || 'localhost'}; path=/; expires=${expirationDate.toUTCString()}`;
    }

    async deleteAccessToken(): Promise<void> {
        const domainName = this.domainHost === 'localhost' ? 'localhost' : '';

        document.cookie = `${this.accessTokenName}=; domain=${domainName}; path=/; expires=-1`;
    }
}

export default AuthDataService;