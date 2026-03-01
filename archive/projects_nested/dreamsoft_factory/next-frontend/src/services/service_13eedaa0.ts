import axios from '@/lib/api'; // Assumes this import correctly references an Axios instance

class MyComponent {
    private resource: string; // Ensure 'resource' is defined before use
    private optID: number;
    private controllerID: string;

    constructor(resource: string, optID: number, controllerID: string) {
        this.resource = resource;
        this.optID = optID;
        this.controllerID = controllerID;
    }

    public async fetchSpeedChanges(): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${this.getResource()}/${this.optID}/efficiency/${this.controllerID}/speedChanges`;
            const response = await axios.get(url);
            return response.data;
        } catch (error) {
            throw error; // Ensure the error is properly propagated
        }
    }

    private getResource(): string {
        // Implement your logic to get resource here
        return this.resource;
    }
}