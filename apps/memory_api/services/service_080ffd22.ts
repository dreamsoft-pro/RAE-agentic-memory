import api from "@/lib/api";

class CurrencyService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async update(lang: any): Promise<any> {
        try {
            const response = await api.put(`${process.env.API_URL}${this.resource}`, lang);
            if (response.response) {
                return response;
            } else {
                throw new Error(JSON.stringify(response));
            }
        } catch (error) {
            throw error;
        }
    }

    async remove(id: string): Promise<any> {
        try {
            const response = await api.delete(`${process.env.API_URL}${this.resource}/${id}`);
            if (response.response) {
                return response;
            } else {
                throw new Error(JSON.stringify(response));
            }
        } catch (error) {
            throw error;
        }
    }
}

export default CurrencyService;