import { NextApiRequest, NextApiResponse } from 'next';
import axios, { AxiosPromise } from 'axios';
import { ISettingService } from './interfaces'; // Assuming you have an interface for typing

const SettingService = class {
    private module: string;
    private apiUrl: string;

    constructor(module?: string) {
        this.module = module || '';
        this.apiUrl = process.env.API_URL; // You should handle environment variables properly in your actual implementation
    }

    setModule(module: string): void {
        this.module = module;
    }

    getPublicSettings(): AxiosPromise<any> {
        const url = `${this.apiUrl}/settings/getPublicSettings/${this.module}`;
        return axios.get(url);
    }
};

export default SettingService;