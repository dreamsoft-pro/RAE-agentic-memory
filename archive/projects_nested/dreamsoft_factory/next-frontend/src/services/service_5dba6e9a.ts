import api from '@/lib/api';

export default class UserService {
    private resource: string = 'users'; // Assuming this is the resource name for users

    public async get(uID: string): Promise<any> {
        try {
            const response = await api.get(`${process.env.API_URL}/${this.resource}?ID=${uID}`);
            if (response.data.length === 1) {
                return response.data[0];
            } else {
                throw new Error('Unexpected data length');
            }
        } catch (error) {
            throw error;
        }
    }

    public async remove(uID: string): Promise<any> {
        try {
            const response = await api.delete(`${process.env.API_URL}/${this.resource}/${uID}`);
            return response.data[0];
        } catch (error) {
            throw error;
        }
    }
}