import { useEffect, useState } from 'react';
import axios from 'axios';

export default class PaymentService {

    private apiUrl: string;

    constructor(config) {
        this.apiUrl = config.API_URL;
    }

    getResource() {
        return ['payments', 'paymentsPublic'];
    }

    getAll(orderID: string): Promise<any> {
        const resource = [this.getResource(), orderID];
        
        return axios.get(this.apiUrl + resource.join('/'))
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }

    getCreditLimit(): Promise<any> {
        const resource = ['payments', 'creditLimit'];
        
        return axios.get(this.apiUrl + resource.join('/'))
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }
}