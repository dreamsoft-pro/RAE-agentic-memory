import api from '@/lib/api';

export default class ProductCardService {
    private resource: string = 'products'; // Assuming 'resource' is 'products'
    private url: string;

    constructor(private productID: number) {
        this.url = `${process.env.API_URL}/${this.resource}/generateXML/${this.productID}`;
    }

    public async fetchProductData(): Promise<any> {
        try {
            const response = await api.get(this.url);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data || 'Failed to fetch product data');
        }
    }
}