import axios from 'axios';
import { createPromiseCapability } from 'es6-collections';

class ReclamationService {
    static async getMyZone(params?: Record<string, any>) {
        params = params || {};

        try {
            const response = await axios.get(`${process.env.API_URL}/${resource}/myZone`, { params });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async getMyZoneCount(params?: Record<string, any>) {
        params = params || {};

        try {
            const response = await axios.get(`${process.env.API_URL}/${resource}/myZoneCount`, { params });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}