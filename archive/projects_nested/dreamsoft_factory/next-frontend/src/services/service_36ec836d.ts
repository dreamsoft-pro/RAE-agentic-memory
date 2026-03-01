import api from '@/lib/api';

export class ConnectOptionService {
    static async remove(id: string) {
        try {
            const response = await api.delete(`${process.env.NEXT_PUBLIC_API_URL}/${resource}/${id}`);
            if (response.data.response) {
                return Promise.resolve(response.data);
            } else {
                return Promise.reject(response.data);
            }
        } catch (error) {
            return Promise.reject(error.response ? error.response.data : error.message);
        }
    }

    static async addToGroup(option: { connectID: string }) {
        try {
            const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${resource}`, option, {
                params: { connectID: option.connectID },
            });
            return Promise.resolve(response.data);
        } catch (error) {
            return Promise.reject(error.response ? error.response.data : error.message);
        }
    }

    // Make sure to define 'resource' and other variables before use
    static resource = '';  // Define this as needed in your application context.
}