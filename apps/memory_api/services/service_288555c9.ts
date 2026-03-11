import api from '@/lib/api';

class PauseService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async update(data: any): Promise<any> {
        try {
            const response = await api.patch(`${process.env.API_URL}${this.resource}`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Failed to patch');
            }
        } catch (error) {
            throw error;
        }
    }

    async remove(id: string): Promise<any> {
        try {
            const response = await api.delete(`${process.env.API_URL}${this.resource}/${id}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    sort(sort: any) {
        return new Promise((resolve, reject) => {
            api.patch(`${process.env.API_URL}${this.resource}`, { sort })
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}

export default PauseService;