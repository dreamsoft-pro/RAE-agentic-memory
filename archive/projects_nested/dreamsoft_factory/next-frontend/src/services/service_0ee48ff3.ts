import api from "@/lib/api";

class MyApiHandler {
    private resource: string;
    private url: string;

    constructor(resource: string) {
        this.resource = resource;
        this.url = `/api/${resource}`;
    }

    async fetchData(): Promise<void> {
        try {
            const response = await api.get(this.url);
            console.log(response.data); // Handle data as needed
        } catch (error) {
            console.error("Failed to fetch data:", error);
        }
    }

    async sendData(data: any): Promise<void> {
        try {
            await api.post(this.url, data);
            console.log(`Data sent successfully`);
        } catch (error) {
            console.error("Failed to send data:", error);
        }
    }
}

// Usage example
const myApiHandler = new MyApiHandler('exampleResource');
myApiHandler.fetchData();