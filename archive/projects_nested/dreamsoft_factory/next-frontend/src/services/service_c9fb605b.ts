import { useEffect, useState } from 'react';
import axios from 'axios';

class AttributeFiltersService {
    private apiUrl: string;

    constructor(config: any) {
        this.apiUrl = config.API_URL;
    }

    getAttributeFilters(attrID: number): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.get(`${this.apiUrl}/attributeFilters/${attrID}`)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }

    getProductsUsingOptions(attrID: number): Promise<any> {
        return new Promise((resolve, reject) => {
            // Add your implementation here
        });
    }
}