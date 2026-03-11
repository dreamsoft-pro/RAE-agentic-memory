import api from '@/lib/api';

class CurrencyService {

    static async update(lang: string) {
        const resource = 'your-resource-name-here'; // Replace with actual resource name

        try {
            const response = await api.post(`${process.env.API_URL}/${resource}`, lang);
            if (response.data.ID) {
                // Assuming cache is defined somewhere in your project
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error; // Rethrow the error for further handling
        }
    }

}

export default CurrencyService;