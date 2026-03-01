import { useEffect, useState } from 'react';
import axios from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async deleteEfficiencySpeed(optID: string, controllerID: string, id: string): Promise<void> {
        const url = `${this.getResource()}/${optID}/efficiency/${controllerID}/speeds/${id}`;
        try {
            await axios.delete(url);
        } catch (error) {
            throw error;
        }
    }

    public async getEfficiencySpeedChanges(optID: string, controllerID: string): Promise<void> {
        const url = `${this.getResource()}/${optID}/efficiency/${controllerID}/speed_changes`;
        try {
            await axios.get(url);
        } catch (error) {
            throw error;
        }
    }

    private getResource(): string {
        return this.resource; // Implement the logic to get resource here
    }
}

export default PsConfigOption;