import axios from 'axios';

class UserAddressService {

    private apiUrl: string;

    constructor(private config: { API_URL: string }) {
        this.apiUrl = config.API_URL;
    }

    public async update(resource: string, data: any): Promise<any> {
        try {
            const response = await axios.put(`${this.apiUrl}${resource}`, data);
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    public async remove(resource: string, data: any): Promise<any> {
        try {
            // Assuming you need to implement the removal logic here
            // For now, this is just a placeholder and should be adjusted according to your requirements.
            const response = await axios.delete(`${this.apiUrl}${resource}`, { data });
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error);
        }
    }
}