import api from "@/lib/api";

export default class MarginsService {
    private resource: string;

    constructor() {
        this.resource = "margins"; // Example resource name
    }

    public async getMargins(): Promise<any> {
        try {
            const url = `/api/${this.resource}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch margins: ${error}`);
        }
    }
}