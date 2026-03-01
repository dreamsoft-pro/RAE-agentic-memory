import api from '@/lib/api';

class CurrencyRootService {
    private resource: string;
    
    constructor(resource: string) {
        this.resource = resource;
    }

    async postRequest(lang: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}${this.resource}`, lang);
            
            if (response.data.ID) {
                // Assuming cache is a global object or imported
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error: any) {
            throw error;
        }
    }

    static async update(lang: any): Promise<any> {
        const def = { resolve: null as ((value: any) => void), reject: null as ((reason?: any) => void) };

        try {
            const response = await api.post(`${process.env.API_URL}/update`, lang);
            
            if (response.data.ID) {
                // Assuming cache is a global object or imported
                cache.remove('collection');
                def.resolve = (value) => value;
                return def.resolve(response.data);
            } else {
                def.reject = (reason) => reason;
                throw def.reject(new Error(JSON.stringify(response.data)));
            }
        } catch (error: any) {
            def.reject(error);
            throw error;
        }

        return new Promise((resolve, reject) => {
            def.resolve = resolve;
            def.reject = reject;
        });
    }
}

export default CurrencyRootService;