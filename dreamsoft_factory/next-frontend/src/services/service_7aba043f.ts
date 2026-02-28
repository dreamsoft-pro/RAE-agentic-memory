import api from "@/lib/api";

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async saveEfficiency(optID: string, controllerID: string, data: any): Promise<any> {
        try {
            const url = `${this.getResource()}/${optID}/efficiency/${controllerID}`;
            const response = await api.put(url, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response does not contain a valid "response" property');
            }
        } catch (error) {
            throw error;
        }
    }

    async getEfficiencySpeeds(optID: string, controllerID: string): Promise<any> {
        try {
            const url = `${this.getResource()}/${optID}/efficiency/${controllerID}`;
            return await api.get(url);
        } catch (error) {
            throw error;
        }
    }

    private getResource(): string {
        // Placeholder for the logic to get resource
        return this.resource; // Ensure you implement the actual logic here.
    }
}