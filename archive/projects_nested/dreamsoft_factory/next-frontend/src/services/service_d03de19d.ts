import api from '@/lib/api';

class UserService {
    private static async changeMail(resource: string, data: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}/${resource}/changeMail`, data);
            if (response.data.response) {
                // cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    private static async getMyAccount(): Promise<any> {
        try {
            const response = await api.get(`${process.env.API_URL}/myaccount`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default UserService;

// Example usage:
// UserService.changeMail('users', { newEmail: 'new.email@example.com' })
//     .then(data => console.log(data))
//     .catch(error => console.error(error));

// UserService.getMyAccount()
//     .then(account => console.log(account))
//     .catch(error => console.error(error));