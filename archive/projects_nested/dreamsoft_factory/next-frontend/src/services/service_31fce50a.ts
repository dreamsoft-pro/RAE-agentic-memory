import { useEffect, useState } from 'react';
import api from '@/lib/api';

class PsConfigOption {

    private resource: string;

    constructor() {
        this.resource = ''; // Initialize the resource variable here or set it in a method
    }

    getResource(): string {
        return this.resource; // Implement logic to return the appropriate resource path
    }

    getOne(optID: string): Promise<any> {
        const url = `${this.getResource()}/${optID}`;

        return api.get(url).then((response) => {
            if (response.data.ID) {
                return response.data;
            } else {
                throw new Error('Failed to retrieve data');
            }
        }).catch(error => {
            throw error;
        });
    }

    add(item: any): Promise<any> {
        const url = this.getResource();

        return api.post(url, item).then((response) => {
            return response.data;
        }).catch(error => {
            throw error;
        });
    }
}

export default PsConfigOption;