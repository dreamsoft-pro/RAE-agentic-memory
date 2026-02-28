import { NextApiRequest, NextApiResponse } from "next";
import api from "@/lib/api";

export default class ConfigService {
    private static async resetDomain(force?: boolean): Promise<void> {
        const resource = 'resetDomain';
        try {
            await api.patch(`${process.env.API_URL}/${resource}`);
        } catch (error) {
            throw error;
        }
    }

    private static async createCompany(form: any): Promise<void> {
        const resource = 'createCompany';
        try {
            await api.post(`${process.env.API_URL}/${resource}`, form);
        } catch (error) {
            throw error;
        }
    }

    // Add other methods here as needed
}