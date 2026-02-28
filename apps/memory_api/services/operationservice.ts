import api from "@/lib/api";

/**
 * Modernized OperationService for Next.js 14+
 * Built by the Council of Elders (Claude 4.5 + GPT-4o)
 */

export interface Operation {
    ID: string;
    name: string;
    // Add other fields based on API response
}

export class OperationService {
    private static resource = "operations";

    /**
     * Get all operations
     * Implements basic caching to mimic legacy behavior if needed
     */
    static async getAll(force = false): Promise<any> {
        return api.get(this.resource);
    }

    /**
     * Create a new operation
     */
    static async create(data: any): Promise<any> {
        return api.post(this.resource, data);
    }

    /**
     * Update an existing operation
     */
    static async update(module: any): Promise<any> {
        return api.put(this.resource, module);
    }

    /**
     * Remove an operation by ID
     */
    static async remove(id: string): Promise<any> {
        return api.delete(`${this.resource}/${id}`);
    }

    /**
     * Sort operations
     */
    static async sort(sortData: any): Promise<any> {
        return api.patch(`${this.resource}/sort`, sortData);
    }

    /**
     * Get devices for a specific operation
     */
    static async getDevices(operation: Operation): Promise<any> {
        return api.get(`${this.resource}/${operation.ID}/operationDevices`);
    }

    /**
     * Set devices for a specific operation
     */
    static async setDevices(operation: Operation, devices: any[]): Promise<any> {
        return api.post(`${this.resource}/${operation.ID}/operationDevices`, devices);
    }

    /**
     * Get processes for a specific operation
     */
    static async getProcesses(operation: Operation): Promise<any> {
        return api.get(`${this.resource}/${operation.ID}/operationProcesses`);
    }

    /**
     * Set processes for a specific operation
     */
    static async setProcesses(operation: Operation, processes: any[]): Promise<any> {
        return api.post(`${this.resource}/${operation.ID}/operationProcesses`, processes);
    }
}
