import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default class TypePatternService {
    private apiUrl: string;
    private resource: string = 'ps_patterns';

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    getUploadUrl(): string {
        return `${this.apiUrl}/${this.resource}`;
    }

    async getList(typeID: number, descID: number): Promise<any> {
        const params = { typeID, descID };
        try {
            const response = await axios.get(`${this.apiUrl}/${this.resource}/patternsPublic`, { params });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}