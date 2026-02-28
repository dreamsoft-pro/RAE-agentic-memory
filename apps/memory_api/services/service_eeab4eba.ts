import api from '@/lib/api';
import { useEffect, useState } from 'react';

class MetaTagService {

    private resource: string;

    constructor() {
        this.resource = 'dp_mainMetaTags';
    }

    public getUploadUrl(resource?: string): string {
        return `${process.env.NEXT_PUBLIC_API_URL}/${resource || this.resource}/uploadImage`;
    }

    public async get(ID: number | string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${ID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async add(metaTag: any, routeID?: string): Promise<void | any> {
        try {
            await api.post(this.resource, { metaTag, routeID });
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    // Add other methods similarly...
}

export default MetaTagService;