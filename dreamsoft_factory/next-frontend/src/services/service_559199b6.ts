import { useEffect, useState } from 'react';
import axios from 'axios';

class UserAddressService {
    private userID: string;
    private resource: string;

    constructor(userID: string) {
        this.userID = userID;
        this.resource = ['users', this.userID, 'address'].join('/');
    }

    public getAllAddresses = async (): Promise<any> => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/${this.resource}?type=1`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    };
}