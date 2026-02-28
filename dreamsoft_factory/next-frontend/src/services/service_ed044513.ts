import api from "@/lib/api";

class PsConfigOption {
    private getResource(): string {
        // Implement or mock this method as needed
        return "config/resource";
    }

    public async getOptionDescriptions(optID: string): Promise<any> {
        const resource = `${this.getResource()}/${optID}/optionDescriptions`;

        try {
            const response = await api.get(resource);
            return response.data;
        } catch (error) {
            throw new Error(error.message || "An unknown error occurred");
        }
    }
}