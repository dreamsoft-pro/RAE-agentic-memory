import { useEffect, useState } from 'react';
import axios from '@/lib/api';

class PsConfigAttribute {
    static async copy(attrID: string): Promise<any> {
        try {
            const collection = cache.get('collection');
            const response = await axios.get(`${resource}/copy/${attrID}`);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    static async getCustomNames(typeID: string): Promise<any> {
        try {
            const collection = cache.get('collection');
            const response = await axios.get(`${resource}/customnames/${typeID}`);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }
}

// Assuming cache and resource are defined elsewhere in your application
let cache = {
    get: (key: string) => {}
};

const resource = ''; // Define this variable before using it

export default PsConfigAttribute;