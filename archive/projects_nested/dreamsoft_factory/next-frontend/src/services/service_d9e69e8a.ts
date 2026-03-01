import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class SettingService {
    private apiBaseUrl: string;

    constructor(apiBaseUrl: string) {
        this.apiBaseUrl = apiBaseUrl;
    }

    signToNewsletter(email: string): Promise<any> {
        const data = { email };
        return axios.post(`${this.apiBaseUrl}/settings/newsletter`, data).then(response => response.data)
            .catch(error => Promise.reject(error));
    }

    confirmNewsletter(token: string): Promise<any> {
        const data = { token };
        return axios.post(`${this.apiBaseUrl}/settings/confirmNewsletter`, data).then(response => response.data)
            .catch(error => Promise.reject(error));
    }
}

export default SettingService;