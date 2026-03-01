import api from "@/lib/api";

class TemplateService {
    private static async post(resource: string, data: any): Promise<any> {
        try {
            const response = await api.post($config.API_URL + resource, data);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }

    private static async put(resource: string, data: any): Promise<any> {
        try {
            const response = await api.put($config.API_URL + resource, data);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }

    public static edit(data: any): void {
        TemplateService.put(resource, data).catch((err: any) => console.error(err));
    }
}