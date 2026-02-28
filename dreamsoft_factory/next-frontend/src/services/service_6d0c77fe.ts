import api from '@/lib/api';
import { Dispatch } from 'redux';
import { StatusData } from '../types'; // Assuming you have a type defined for status data

class DpStatusService {
    private resource: string = 'dp_statuses';

    public async getAll(active?: boolean): Promise<StatusData[]> {
        let uri = [this.resource];
        if (active !== undefined) {
            uri.push('1');
        }

        try {
            const response = await api.get(`${process.env.API_URL}/${uri.join('/')}`);
            return response.data;
        } catch (error) {
            throw new Error(error.response ? error.response.statusText : 'Network Error');
        }
    }

    public async add(data: StatusData): Promise<StatusData> {
        try {
            const response = await api.post(`${process.env.API_URL}/${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw new Error(error.response ? error.response.statusText : 'Network Error');
        }
    }

    // Add other methods as needed
}

export default DpStatusService;