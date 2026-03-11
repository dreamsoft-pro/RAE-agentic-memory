import api from "@/lib/api";

class TypeDescriptionsService {
    private resource: string;
    private showLang: string;

    constructor(resource: string, showLang: string) {
        this.resource = resource;
        this.showLang = showLang;
    }

    async addDescription(data: any): Promise<any> {
        try {
            const response = await api.post(
                `${process.env.API_URL}/${this.resource}?showLang=${this.showLang}`,
                data
            );
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async removeDescription(id: string): Promise<any> {
        try {
            const response = await api.delete(`${process.env.API_URL}/${this.resource}/${id}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async editDescription(data: any, id?: string): Promise<any> {
        let url = `${process.env.API_URL}/${this.resource}`;

        if (id) {
            url += `/${id}`;
        }

        try {
            const response = await api.put(url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default TypeDescriptionsService;