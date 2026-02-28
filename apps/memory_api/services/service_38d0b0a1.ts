import api from '@/lib/api';

class LabelImpositionService {
    static async update(data: any): Promise<any> {
        let resource = 'your_resource'; // Ensure this variable is defined before use

        if (data.ID) {
            try {
                const response = await api.put(`${resource}/${data.ID}`, data);
                return response;
            } catch (error) {
                return Promise.reject(error.response || error);
            }
        } else {
            try {
                const response = await api.post(resource, data);
                return response;
            } catch (error) {
                return Promise.reject(error.response || error);
            }
        }
    }
}

export default LabelImpositionService;