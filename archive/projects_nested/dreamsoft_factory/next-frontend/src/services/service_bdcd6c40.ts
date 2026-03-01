import api from "@/lib/api";
import { AxiosError } from "axios";

export default class LangSettingsService {
    private resource: string;
    private urlBase: string;

    constructor(resource: string) {
        this.resource = resource;
        this.urlBase = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
    }

    async update(id: string, lang: any): Promise<any> {
        try {
            const response = await api.put(`${this.urlBase}/${id}`, lang);
            return response.data;
        } catch (error) {
            throw new Error((error as AxiosError).response?.data || error.message);
        }
    }

    async remove(id: string): Promise<void> {
        try {
            await api.delete(`${this.urlBase}/${id}`);
        } catch (error) {
            throw new Error((error as AxiosError).response?.data || error.message);
        }
    }
}