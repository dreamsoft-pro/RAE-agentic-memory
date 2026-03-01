import api from '@/lib/api';

class TaxService {
    private resource: string;
    
    constructor(resource: string) {
        this.resource = resource;
    }

    public async fetchTaxForProduct(params: string): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${this.resource}/taxForProduct${params}`;
            const response = await api.get(url);
            return response.data; // assuming the data you want is in `response.data`
        } catch (error) {
            throw new Error(error.response?.data || error.message); // handle errors appropriately
        }
    }
}

// Usage example:
const taxServiceInstance = new TaxService('exampleResource');
taxServiceInstance.fetchTaxForProduct('?param=value')
    .then(data => console.log(data))
    .catch(err => console.error(err));