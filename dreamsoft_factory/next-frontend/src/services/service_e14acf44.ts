import api from '@/lib/api';
import { useEffect, useState } from 'react';

export default class UserService {
    private resource: string;
    private userID: number;

    constructor(resource: string, userID: number) {
        this.resource = resource;
        this.userID = userID;
    }

    public async getCurrency(): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/getCurrency/${this.userID}`);
            return response.data;
        } catch (error) {
            throw new Error(error);
        }
    }

    public async getImportantData(): Promise<any> {
        try {
            const response = await api.get([this.resource, 'importantData'].join('/'));
            return response.data;
        } catch (error) {
            throw new Error(error);
        }
    }

    public async editImportantData(data: any): Promise<void> {
        try {
            await api.put(`${this.resource}/editImportantData`, data);
        } catch (error) {
            throw new Error(error);
        }
    }
}