import { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL; // Ensure this is set in your environment

class PsComplexService {
    private groupID: string | number;
    private typeID: string | number;

    constructor(groupID: string | number, typeID: string | number) {
        this.groupID = groupID;
        this.typeID = typeID;
    }

    getResource(): string {
        return `ps_groups/${this.groupID}/ps_types/${this.typeID}/ps_complex`;
    }

    async getAll(): Promise<any> {
        const resource = this.getResource();
        try {
            const response = await axios.get(`${API_URL}${resource}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}

export default PsComplexService;