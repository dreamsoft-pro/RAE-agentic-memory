import api from "@/lib/api";

class OperationService {
    private static cache: any; // Assuming some caching mechanism

    public static async postResource(resource: string, data: object): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
            const response = await api.post(url, data);
            
            if (response.data.ID) {
                OperationService.cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    public static async update(module: string): Promise<any> {
        try {
            // Assuming some logic to get data or construct request
            const resource = 'someResource'; // Example, replace with actual logic
            const data = {}; // Example data object
            
            return await OperationService.postResource(resource, data);
        } catch (error) {
            throw error;
        }
    }
}

export default OperationService;