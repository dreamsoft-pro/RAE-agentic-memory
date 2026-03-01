import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class ComplexService {
    private API_URL: string;

    constructor(API_URL: string) {
        this.API_URL = API_URL;
    }

    public getAllPublic(): Promise<any> {
        const resource = this.getResource();

        return axios.get(`${this.API_URL}/${resource}/complexPublic`).then(response => response.data).catch(error => {
            throw error.response ? error.response : error;
        });
    }

    public add(baseID: number, typeID: number, complexGroupID: number): Promise<any> {
        const resource = this.getResource();

        return axios.post(`${this.API_URL}/${resource}`, { baseID, typeID, complexGroupID }).then(response => response.data).catch(error => {
            throw error.response ? error.response : error;
        });
    }

    private getResource(): string {
        // Implement the logic to get the resource
        return "example-resource";
    }
}

export default ComplexService;