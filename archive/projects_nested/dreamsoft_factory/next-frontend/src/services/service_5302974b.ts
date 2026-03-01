import api from "@/lib/api";
import { Cache } from "@/utils/cache"; // Assuming cache functionality exists in this module

class SkillService {
    private resource: string;
    private url: string;

    constructor(resource: string) {
        this.resource = resource;
        this.url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
    }

    async create(data: any): Promise<any> {
        try {
            const response = await api.post(this.url, data);
            if (response.data.ID) {
                Cache.remove('collection');
                return response.data;
            } else {
                throw new Error("Failed to create resource");
            }
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async update(module: any): Promise<any> {
        try {
            const response = await api.put(this.url, module);
            if (response.data.response) {
                Cache.remove('collection');
                return response.data;
            } else {
                throw new Error("Failed to update resource");
            }
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async remove(id: string): Promise<any> {
        try {
            const response = await api.delete(`${this.url}/${id}`);
            if (response.status === 204 || response.data.success) { // Assuming 204 or success:true for successful delete
                Cache.remove('collection');
                return response;
            } else {
                throw new Error("Failed to remove resource");
            }
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default SkillService;