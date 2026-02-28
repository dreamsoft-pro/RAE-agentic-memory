import api from '@/lib/api';
import { useState, useEffect } from 'react';

class AuthService {
    private accessTokenName: string;

    constructor(config: any) {
        this.accessTokenName = config.ACCESS_TOKEN_NAME;
    }

    public setUserData(data: any): Promise<boolean> {
        const username = data.user?.firstname ?? '';
        localStorage.setItem('user', JSON.stringify(data.user));
        this.setAccessToken(data.token || data[this.accessTokenName]);

        const expectedToken = this.getAccessToken();
        if (data.token === expectedToken) {
            return Promise.resolve(true);
        } else {
            return Promise.reject(false);
        }
    }

    private setAccessToken(token: string): void {
        localStorage.setItem('accessToken', token);
    }

    public getAccessToken(): string {
        return localStorage.getItem('accessToken') ?? '';
    }
}

export default new AuthService({
    ACCESS_TOKEN_NAME: 'token'
});