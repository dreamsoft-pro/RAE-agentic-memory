import axios from 'axios';
import { Config } from './config'; // Assuming your configuration is in a separate file

class SettingService {

    private apiUrl: string;

    constructor(config: Config) {
        this.apiUrl = config.API_URL;
    }

    public async getSkinName(): Promise<string> {
        try {
            const response = await axios.get(`${this.apiUrl}/settings/getSkinName`);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data || 'Failed to fetch skin name');
        }
    }

    public async sendMessage(key: string, data: any): Promise<any> {
        try {
            const response = await axios.post(`${this.apiUrl}/settings/sendMessage/${key}`, data);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data || 'Failed to send message');
        }
    }

}