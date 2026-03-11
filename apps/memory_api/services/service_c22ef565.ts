import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor() {
        this.resource = ''; // Ensure to define the resource or initialize it somewhere in your class.
    }

    public getResource(): string {
        return this.resource; // This method should be implemented based on how you determine the resource path.
    }

    public async saveIncreases(optID: number, controllerID: number, item: any): Promise<any> {
        const url = `${this.getResource()}/${optID}/increaseControllers/${controllerID}/ps_config_increases`;

        try {
            const response = await api.patch(url, item);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error; // Handle errors accordingly
        }
    }

    public async removeIncrease(optID: number, controllerID: number, item: any): Promise<void> {
        const url = `${this.getResource()}/${optID}/increaseControllers/${controllerID}/ps_config_increases`;

        try {
            await api.delete(url); // Assuming the 'item' parameter is not required for delete operation.
        } catch (error) {
            throw error.response ? error.response : error; // Handle errors accordingly
        }
    }

    private getResource(): string { 
        return ''; // Implement this method based on your specific logic to get resource path.
    }
}