import api from '@/lib/api';

class LangRootService {
    private resource: string = 'your-resource'; // Replace with actual resource path

    public async create(lang: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}${this.resource}`, lang);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async update(lang: any): Promise<any> {
        try {
            const response = await api.put(`${process.env.API_URL}${this.resource}`, lang);
            if (!response.data?.response) {
                throw new Error('Invalid response');
            }
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default LangRootService;

// Usage example
const service = new LangRootService();
service.create(langData).then(data => console.log(data)).catch(error => console.error(error));