import api from "@/lib/api";

class OperationService {
    private static async update(resource: string, module: any): Promise<any> {
        try {
            const response = await api.put($config.API_URL + resource, module);
            if (response.data.response) {
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error("Failed to update");
            }
        } catch (error: any) {
            throw error;
        }
    }

    private static async remove(id: string): Promise<void> {
        try {
            await api.delete($config.API_URL + id);
        } catch (error: any) {
            throw error;
        }
    }

    // Example of how to use the methods
    public static async performOperations() {
        const resource = "exampleResource";
        const module = { /* some data */ };

        try {
            await this.update(resource, module);
            console.log("Update successful");
            
            const idToRemove = "12345";
            await this.remove(idToRemove);
            console.log("Remove successful");
        } catch (error: any) {
            console.error("Error occurred:", error.message);
        }
    }
}

export default OperationService;